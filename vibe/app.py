"""Campus Circle vibe build. Local teaching application; Python 3.12+."""
import argparse
import hashlib
import hmac
import html
import re
import secrets
import sqlite3
import threading
import time
from contextlib import contextmanager
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'data' / 'campus.sqlite3'
TTL = 8 * 60 * 60
ATTEMPTS = {}
LOCK = threading.Lock()

@contextmanager
def connect():
    db = sqlite3.connect(DB, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        with db:
            yield db
    finally:
        db.close()

def initialize():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE COLLATE NOCASE,
            name TEXT NOT NULL, salt TEXT NOT NULL, password_hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY, csrf TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id), expires REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id),
            body TEXT NOT NULL CHECK(length(body) BETWEEN 1 AND 500),
            created TEXT NOT NULL);
        ''')

def password_hash(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 600_000).hex()

def escape(value):
    return html.escape(str(value), quote=True)

class App(BaseHTTPRequestHandler):
    def reply(self, content='', status=200, kind='text/html', location=None):
        body = content.encode('utf-8') if isinstance(content, str) else content
        self.send_response(status)
        self.send_header('Content-Type', kind + '; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'same-origin')
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        if hasattr(self, 'sid'):
            self.send_header('Set-Cookie', f'circle_session={self.sid}; HttpOnly; SameSite=Strict; Path=/; Max-Age={TTL}')
        if location:
            self.send_header('Location', location)
        self.end_headers()
        self.wfile.write(body)

    def session(self):
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get('Cookie', ''))
        except Exception:
            cookie = SimpleCookie()
        token = cookie['circle_session'].value if 'circle_session' in cookie else ''
        with connect() as db:
            db.execute('DELETE FROM sessions WHERE expires < ?', (time.time(),))
            row = db.execute('''SELECT s.*, u.username, u.name FROM sessions s
                LEFT JOIN users u ON s.user_id=u.id WHERE s.token=?''', (token,)).fetchone()
            if row is None:
                token, csrf = secrets.token_hex(32), secrets.token_hex(32)
                db.execute('INSERT INTO sessions VALUES (?,?,NULL,?)', (token, csrf, time.time() + TTL))
                row = db.execute('SELECT *, NULL AS username, NULL AS name FROM sessions WHERE token=?', (token,)).fetchone()
        self.sid, self.state = token, row

    def hidden(self):
        return f'<input type="hidden" name="csrf" value="{self.state["csrf"]}">'

    def page(self, center, error='', status=200):
        source = (ROOT / 'index.html').read_text(encoding='utf-8')
        start, end = source.index('<main>'), source.index('</main>')
        notice = f'<div class="error" role="alert">{escape(error)}</div>' if error else ''
        source = source[:start] + '<main>' + notice + center + source[end:]
        if self.state['user_id']:
            account = f'<div class="account"><span class="username">Hi, {escape(self.state["name"])}</span><form method="post" action="/logout">{self.hidden()}<button>Log out</button></form></div>'
        else:
            account = '<div class="account"><a href="/login">Log in</a><a class="button" href="/register">Join the circle</a></div>'
        source = source.replace('<span class="header-note">A little closer to your campus.</span>', account)
        self.reply(source, status)

    def auth_page(self, register=False, error='', status=200):
        title = 'Join your campus circle' if register else 'Welcome back'
        extras = '<label>Display name<input name="name" required maxlength="50" autocomplete="name"></label>' if register else ''
        destination = '/register' if register else '/login'
        alternate = '<a href="/login">Already a member? Log in</a>' if register else '<a href="/register">New here? Create an account</a>'
        self.page(f'''<section class="card auth"><div class="eyebrow">YOUR CAMPUS, CONNECTED</div>
            <h2>{title}</h2><p>A little closer to the people around you.</p>
            <form method="post" action="{destination}">{self.hidden()}{extras}
            <label>Username<input name="username" required minlength="3" maxlength="24" pattern="[A-Za-z0-9_]+" autocomplete="username"></label>
            <span class="hint">3–24 letters, numbers, or underscores.</span>
            <label>Password<input name="password" type="password" required minlength="12" maxlength="128" autocomplete="{'new-password' if register else 'current-password'}"></label>
            <span class="hint">12–128 characters.</span><button>{'Create account' if register else 'Log in'}</button></form>{alternate}</section>''', error, status)

    def home(self, error='', status=200):
        source = (ROOT / 'index.html').read_text(encoding='utf-8')
        center = source.split('<main>', 1)[1].split('</main>', 1)[0]
        center = center.replace('<span class="pill">Registration opens in the next milestone</span>', '<a class="button" href="/register">Join the circle ↗</a>' if not self.state['user_id'] else '<span class="pill">You’re in the circle</span>')
        feed_start = center.index('<div class="feed-heading">')
        if self.state['user_id']:
            composer = f'''<section class="card composer"><h2>What’s happening on campus?</h2>
            <form method="post" action="/posts">{self.hidden()}<label for="post-body">Share a moment</label>
            <textarea id="post-body" name="body" maxlength="500" required placeholder="An idea, a study tip, a little hello…"></textarea>
            <div class="composer-footer"><span class="hint">Text only · Up to 500 characters</span><button>Publish post ↗</button></div></form></section>'''
        else:
            composer = ''
        with connect() as db:
            posts = db.execute('''SELECT p.*, u.name, u.username FROM posts p JOIN users u ON p.user_id=u.id
                ORDER BY p.id DESC LIMIT 100''').fetchall()
        feed = '<div class="feed-heading"><h2>Community feed</h2><span>Latest 100 · newest first</span></div>'
        for post in posts:
            feed += f'''<article class="card post"><div class="post-head"><span class="avatar" aria-hidden="true">{escape(post['name'][0].upper())}</span>
            <div><strong>{escape(post['name'])}</strong> <span class="hint">@{escape(post['username'])}</span>
            <time datetime="{escape(post['created'])}">{escape(post['created'])} UTC</time></div></div><p class="post-body">{escape(post['body'])}</p></article>'''
        if not posts:
            feed += '<section class="empty"><div class="empty-icon">✳</div><h2>A fresh start for your campus</h2><p>No posts yet. Be the first to share a moment.</p></section>'
        center = center[:feed_start] + composer + feed
        self.page(center, error, status)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/style.css':
            self.reply((ROOT / 'style.css').read_bytes(), kind='text/css')
            return
        self.session()
        if path == '/':
            self.home()
        elif path in ('/login', '/register'):
            if self.state['user_id']:
                self.reply(status=303, location='/')
            else:
                self.auth_page(path == '/register')
        else:
            self.page('<h1>Page not found</h1><a href="/">Back to the circle</a>', status=404)

    def do_POST(self):
        self.session()
        path = urlsplit(self.path).path
        try:
            length = int(self.headers.get('Content-Length', '-1'))
        except ValueError:
            length = -1
        if length < 0 or length > 8192:
            self.reply('Request too large or missing length.', 413)
            return
        if self.headers.get_content_type() != 'application/x-www-form-urlencoded':
            self.reply('Use form encoding.', 415)
            return
        try:
            form = parse_qs(self.rfile.read(length).decode('utf-8'), keep_blank_values=True, max_num_fields=10)
        except (ValueError, UnicodeDecodeError):
            self.reply('Invalid form.', 400)
            return
        value = lambda key: form.get(key, [''])[0]
        if not hmac.compare_digest(value('csrf'), self.state['csrf']):
            self.page('<h1>Please reload and try again.</h1>', 'Your form expired.', 403)
            return
        if path == '/logout':
            with connect() as db:
                db.execute('DELETE FROM sessions WHERE token=?', (self.sid,))
            self.reply(status=303, location='/')
            return
        if path == '/posts':
            if not self.state['user_id']:
                self.home('Log in to publish a post.', 401)
                return
            body = value('body').strip()
            if not 1 <= len(body) <= 500:
                self.home('Posts must contain 1–500 characters.', 400)
                return
            with connect() as db:
                db.execute('INSERT INTO posts(user_id,body,created) VALUES (?,?,?)',
                    (self.state['user_id'], body, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
            self.reply(status=303, location='/')
            return
        if path not in ('/register', '/login'):
            self.reply('Page not found.', 404)
            return
        now = time.time()
        with LOCK:
            for key in list(ATTEMPTS):
                ATTEMPTS[key] = [t for t in ATTEMPTS[key] if now - t < 60]
                if not ATTEMPTS[key]:
                    del ATTEMPTS[key]
            attempts = ATTEMPTS.setdefault(self.client_address[0], [])
            limited = len(attempts) >= 10
            if not limited:
                attempts.append(now)
        if limited:
            self.auth_page(path == '/register', 'Too many attempts. Try again in a minute.', 429)
            return
        username, password, name = value('username').strip(), value('password'), value('name').strip()
        if not re.fullmatch(r'[A-Za-z0-9_]{3,24}', username) or not 12 <= len(password) <= 128:
            self.auth_page(path == '/register', 'Check the username and password lengths.', 400)
            return
        with connect() as db:
            if path == '/register':
                if not 1 <= len(name) <= 50:
                    self.auth_page(True, 'Display name must be 1–50 characters.', 400)
                    return
                salt = secrets.token_hex(16)
                try:
                    user_id = db.execute('INSERT INTO users(username,name,salt,password_hash) VALUES (?,?,?,?)', (username, name, salt, password_hash(password, salt))).lastrowid
                except sqlite3.IntegrityError:
                    self.auth_page(True, 'That username is already taken.', 409)
                    return
            else:
                user = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
                candidate = password_hash(password, user['salt'] if user else '00' * 16)
                if not user or not hmac.compare_digest(candidate, user['password_hash']):
                    self.auth_page(False, 'Incorrect username or password.', 401)
                    return
                user_id = user['id']
            db.execute('DELETE FROM sessions WHERE token=?', (self.sid,))
            self.sid = secrets.token_hex(32)
            db.execute('INSERT INTO sessions VALUES (?,?,?,?)', (self.sid, secrets.token_hex(32), user_id, now + TTL))
        self.reply(status=303, location='/')

def main():
    global DB
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--db', type=Path, default=DB)
    args = parser.parse_args()
    DB = args.db
    initialize()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), App)
    print(f'Campus Circle: http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
