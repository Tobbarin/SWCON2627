"""Black-box HTTP acceptance tests shared by both independently built apps."""
import http.client
import importlib.util
import os
from pathlib import Path
import re
import tempfile
import threading
import unittest
from urllib.parse import urlencode
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
BUILD = os.environ.get('CAMPUS_BUILD', 'vibe')
spec = importlib.util.spec_from_file_location('campus', ROOT / BUILD / 'app.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class Acceptance(unittest.TestCase):
    def setUp(self):
        runtime = ROOT / 'data' / 'test-runs'
        runtime.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=runtime)
        app.DB = Path(self.temp.name) / 'test.sqlite3'
        app.initialize()
        app.ATTEMPTS.clear()
        class Quiet(app.App):
            def log_message(self, *args):
                pass
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Quiet)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.cookie = ''

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self, path='/', fields=None, cookie=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        headers = {'Cookie': self.cookie if cookie is None else cookie}
        body = None
        if fields is not None:
            body = urlencode(fields)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        connection.request('GET' if fields is None else 'POST', path, body, headers)
        response = connection.getresponse()
        text = response.read().decode()
        result = (response.status, text, dict(response.getheaders()))
        if response.getheader('Set-Cookie'):
            self.cookie = response.getheader('Set-Cookie').split(';')[0]
        connection.close()
        return result

    def csrf(self, path='/register'):
        status, body, _ = self.request(path)
        self.assertEqual(status, 200)
        return re.search(r'name="csrf" value="([a-f0-9]+)"', body).group(1)

    def register(self, username='student', name='Student'):
        csrf = self.csrf()
        return self.request('/register', dict(csrf=csrf, username=username, name=name, password='long-password-123'))

    def test_A01_home_and_security_headers(self):
        status, body, headers = self.request()
        self.assertEqual(status, 200)
        self.assertIn('Stay in the circle', body)
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])
        self.assertIn('HttpOnly', headers['Set-Cookie'])

    def test_A02_register_and_session_rotation(self):
        old = self.csrf()
        old_cookie = self.cookie
        status, _, headers = self.request('/register', dict(csrf=old, username='student', name='Student', password='long-password-123'))
        self.assertEqual(status, 303)
        self.assertEqual(headers['Location'], '/')
        self.assertNotEqual(old_cookie, self.cookie)
        self.assertIn('Hi, Student', self.request()[1])
        self.assertNotIn('Hi, Student', self.request(cookie=old_cookie)[1])

    def test_A03_case_insensitive_duplicate(self):
        self.assertEqual(self.register()[0], 303)
        self.cookie = ''
        self.assertEqual(self.register('STUDENT')[0], 409)

    def test_A04_login_logout_and_password_storage(self):
        self.register()
        token = self.csrf('/')
        old = self.cookie
        self.assertEqual(self.request('/logout', {'csrf': token})[0], 303)
        self.assertNotIn('Hi, Student', self.request(cookie=old)[1])
        token = self.csrf('/login')
        self.assertEqual(self.request('/login', dict(csrf=token, username='STUDENT', password='long-password-123'))[0], 303)
        self.assertIn('Hi, Student', self.request()[1])
        with app.connect() as db:
            row = db.execute('SELECT * FROM users').fetchone()
            self.assertNotEqual(row['password_hash'], 'long-password-123')
            self.assertEqual(len(row['salt']), 32)

    def test_A05_invalid_registration(self):
        token = self.csrf()
        self.assertEqual(self.request('/register', dict(csrf=token, username='x', name='Student', password='short'))[0], 400)

    def test_A06_wrong_login(self):
        self.register()
        self.cookie = ''
        token = self.csrf('/login')
        self.assertEqual(self.request('/login', dict(csrf=token, username='student', password='wrong-password-123'))[0], 401)

    def test_A07_missing_csrf(self):
        self.csrf()
        self.assertEqual(self.request('/register', dict(username='student', name='Student', password='long-password-123'))[0], 403)

    def test_A08_throttle(self):
        token = self.csrf('/login')
        for _ in range(10):
            self.request('/login', dict(csrf=token, username='x', password='short'))
        self.assertEqual(self.request('/login', dict(csrf=token, username='x', password='short'))[0], 429)

    def post(self, body, **extra):
        return self.request('/posts', dict(csrf=self.csrf('/'), body=body, **extra))

    def test_A09_post_persists_and_visible_to_another_visitor(self):
        self.register()
        self.assertEqual(self.post('Hello campus!')[0], 303)
        self.cookie = ''
        self.assertIn('Hello campus!', self.request()[1])
        app.initialize()
        self.assertIn('Hello campus!', self.request()[1])

    def test_A10_anonymous_post_rejected(self):
        token = self.csrf()
        self.assertEqual(self.request('/posts', dict(csrf=token, body='No account'))[0], 401)

    def test_A11_post_bounds(self):
        self.register()
        self.assertEqual(self.post('   ')[0], 400)
        self.assertEqual(self.post('x' * 501)[0], 400)
        self.assertEqual(self.post('x' * 500)[0], 303)

    def test_A12_html_is_escaped(self):
        self.register(name='<script>bad</script>')
        self.post('<script>alert(1)</script>')
        body = self.request()[1]
        self.assertNotIn('<script>', body)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', body)

    def test_A13_newest_first_and_author_cannot_be_spoofed(self):
        self.register()
        self.post('older-message', user_id='999')
        self.post('newer-message')
        body = self.request()[1]
        self.assertLess(body.index('newer-message'), body.index('older-message'))
        with app.connect() as db:
            self.assertEqual(db.execute('SELECT user_id FROM posts LIMIT 1').fetchone()[0], 1)

    def test_A14_csrf_is_bound_to_session(self):
        token = self.csrf()
        self.cookie = ''
        self.csrf()
        self.assertEqual(self.request('/register', dict(csrf=token, username='student', name='Student', password='long-password-123'))[0], 403)

if __name__ == '__main__':
    unittest.main(verbosity=2)
