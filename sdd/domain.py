"""SDD domain/persistence layer: FR01/02, NFR01/02/04."""
from contextlib import contextmanager
import hashlib
import hmac
from pathlib import Path
import re
import secrets
import sqlite3
from threading import Lock
import time

LIFETIME = 28_800
ATTEMPTS = {}
_attempt_lock = Lock()

class Rejected(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status

def throttle(address):
    now = time.monotonic()
    with _attempt_lock:
        for key in list(ATTEMPTS):
            ATTEMPTS[key] = [instant for instant in ATTEMPTS[key] if instant > now - 60]
            if not ATTEMPTS[key]:
                del ATTEMPTS[key]
        history = ATTEMPTS.setdefault(address, [])
        if len(history) >= 10:
            raise Rejected(429, 'Too many attempts. Try again in a minute.')
        history.append(now)

def digest(secret, salt):
    return hashlib.pbkdf2_hmac('sha256', secret.encode('utf-8'), bytes.fromhex(salt), 600_000).hex()

def credentials(username, password):
    username = username.strip()
    if not re.fullmatch(r'[A-Za-z0-9_]{3,24}', username) or not 12 <= len(password) <= 128:
        raise Rejected(400, 'Use a valid username and a password of 12–128 characters.')
    return username

class Store:
    def __init__(self, path):
        self.path = Path(path)

    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys=ON')
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    name TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    password_hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    csrf TEXT NOT NULL,
                    user_id INTEGER REFERENCES users(id),
                    expires REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    body TEXT NOT NULL CHECK(length(body) BETWEEN 1 AND 500),
                    created TEXT NOT NULL);
            ''')

    def resolve_session(self, token):
        now = time.time()
        with self.connection() as db:
            db.execute('DELETE FROM sessions WHERE expires <= ?', (now,))
            session = db.execute('''SELECT s.*, u.name, u.username FROM sessions s
                LEFT JOIN users u ON s.user_id=u.id WHERE token=?''', (token,)).fetchone()
            if session is None:
                token = secrets.token_hex(32)
                db.execute('INSERT INTO sessions VALUES (?,?,NULL,?)', (token, secrets.token_hex(32), now + LIFETIME))
                session = db.execute('SELECT *, NULL AS name, NULL AS username FROM sessions WHERE token=?', (token,)).fetchone()
        return session

    def end_session(self, token):
        with self.connection() as db:
            db.execute('DELETE FROM sessions WHERE token=?', (token,))

    @staticmethod
    def replace_session(db, old_token, user_id):
        db.execute('DELETE FROM sessions WHERE token=?', (old_token,))
        token = secrets.token_hex(32)
        db.execute('INSERT INTO sessions VALUES (?,?,?,?)', (token, secrets.token_hex(32), user_id, time.time() + LIFETIME))
        return token

    def register(self, fields, old_token):
        username = credentials(fields.get('username', ''), fields.get('password', ''))
        name = fields.get('name', '').strip()
        if not 1 <= len(name) <= 50 or '\x00' in name:
            raise Rejected(400, 'Display name must contain 1–50 characters.')
        salt = secrets.token_hex(16)
        password_hash = digest(fields['password'], salt)
        try:
            with self.connection() as db:
                result = db.execute('INSERT INTO users(username,name,salt,password_hash) VALUES (?,?,?,?)', (username, name, salt, password_hash))
                return self.replace_session(db, old_token, result.lastrowid)
        except sqlite3.IntegrityError as error:
            raise Rejected(409, 'That username is already taken.') from error

    def login(self, fields, old_token):
        password = fields.get('password', '')
        username = credentials(fields.get('username', ''), password)
        with self.connection() as db:
            account = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            actual = digest(password, account['salt'] if account else '00' * 16)
            expected = account['password_hash'] if account else '00' * 32
            matches = hmac.compare_digest(actual, expected)
            if account is None or not matches:
                raise Rejected(401, 'Incorrect username or password.')
            return self.replace_session(db, old_token, account['id'])
