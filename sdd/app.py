"""SDD HTTP adapter implementing contracts/http.md; local prototype only."""
import argparse
import hmac
from http.cookies import SimpleCookie, CookieError
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import domain
import views

DB = ROOT / 'data' / 'campus.sqlite3'
ATTEMPTS = domain.ATTEMPTS

def connect():
    return domain.Store(DB).connection()

def initialize():
    domain.Store(DB).initialize()

class App(BaseHTTPRequestHandler):
    def respond(self, content='', status=200, location=None, mime='text/html'):
        encoded = content.encode('utf-8') if isinstance(content, str) else content
        self.send_response(status)
        headers = {'Content-Type': mime + '; charset=utf-8', 'Content-Length': str(len(encoded)),
            'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'same-origin',
            'Content-Security-Policy': "default-src 'self'; style-src 'self'; script-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"}
        if hasattr(self, 'session'):
            headers['Set-Cookie'] = f'circle_session={self.session["token"]}; HttpOnly; SameSite=Strict; Path=/; Max-Age={domain.LIFETIME}'
        if location:
            headers['Location'] = location
        for name, value in headers.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(encoded)

    def resolve(self):
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get('Cookie', ''))
        except CookieError:
            cookie = SimpleCookie()
        token = cookie['circle_session'].value if 'circle_session' in cookie else ''
        self.store = domain.Store(DB)
        self.session = self.store.resolve_session(token)

    def render(self, path, status=200, error=''):
        if path in ('/register', '/login'):
            content = views.auth(self.session, path == '/register')
        elif path == '/':
            content = views.home(self.session, self.store.feed())
        else:
            content = '<h1>Page not found</h1><a href="/">Back to the circle</a>'
        self.respond(views.layout(content, self.session, error), status)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/style.css':
            self.respond((ROOT / 'style.css').read_bytes(), mime='text/css')
            return
        self.resolve()
        if path not in ('/', '/register', '/login'):
            self.render(path, 404)
        elif path != '/' and self.session['user_id'] is not None:
            self.respond(status=303, location='/')
        else:
            self.render(path)

    def form(self):
        try:
            count = int(self.headers.get('Content-Length', '-1'))
        except ValueError:
            count = -1
        if not 0 <= count <= 8192:
            raise domain.Rejected(413, 'Request too large or missing length.')
        if self.headers.get_content_type() != 'application/x-www-form-urlencoded':
            raise domain.Rejected(415, 'Use form encoding.')
        try:
            fields = parse_qs(self.rfile.read(count).decode('utf-8'), keep_blank_values=True, max_num_fields=10, errors='strict')
        except (ValueError, UnicodeDecodeError) as error:
            raise domain.Rejected(400, 'Invalid form encoding.') from error
        if any(len(values) != 1 for values in fields.values()):
            raise domain.Rejected(400, 'Repeated form fields are not accepted.')
        fields = {name: values[0] for name, values in fields.items()}
        token = fields.get('csrf', '')
        if not re.fullmatch(r'[a-f0-9]{64}', token) or not hmac.compare_digest(token, self.session['csrf']):
            raise domain.Rejected(403, 'Your form expired. Reload and try again.')
        return fields

    def do_POST(self):
        self.resolve()
        path = urlsplit(self.path).path
        try:
            fields = self.form()
            if path in ('/register', '/login'):
                domain.throttle(self.client_address[0])
                operation = self.store.register if path == '/register' else self.store.login
                new_token = operation(fields, self.session['token'])
                self.session = self.store.resolve_session(new_token)
            elif path == '/logout':
                self.store.end_session(self.session['token'])
            elif path == '/posts':
                self.store.publish(self.session['user_id'], fields.get('body', ''))
            else:
                raise domain.Rejected(404, 'Page not found.')
        except domain.Rejected as rejection:
            self.render(path if path in ('/register', '/login') else '/', rejection.status, str(rejection))
            return
        self.respond(status=303, location='/')

def main():
    global DB
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--port', default=8001, type=int)
    arguments.add_argument('--db', default=DB, type=Path)
    options = arguments.parse_args()
    DB = options.db
    initialize()
    with ThreadingHTTPServer(('127.0.0.1', options.port), App) as server:
        print(f'Campus Circle SDD: http://127.0.0.1:{options.port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
