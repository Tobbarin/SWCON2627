# Vibe implementation

Completed first implementation, built through feature-first natural-language iterations. Accounts, sessions, and posts persist in SQLite. No external Python packages are needed.

## Run

From the repository root, with Python 3.12 or newer:

```sh
python vibe/app.py --port 8000
```

Open http://127.0.0.1:8000. Create an account (username: 3–24 ASCII letters/numbers/underscores; display name: 1–50 characters; password: 12–128 characters), publish a text post, log out, then log back in. Posts are visible to everyone visiting this local server. Test another account in a separate browser profile. There are no seeded accounts or public passwords.

## Verify

```sh
python tests/test_acceptance.py
```

The suite uses isolated databases and real HTTP. Default data is in `vibe/data/campus.sqlite3` (ignored by Git); override with `--db PATH`. Ctrl+C stops the server. To start fresh, stop the app, back up the database if needed, then remove that specific local database yourself.

## Boundaries

Local course demonstration, bound to loopback. Python's standard-library HTTP server is not a production deployment stack. HTTP cookies deliberately omit Secure for loopback HTTP; public hosting requires HTTPS, Secure cookies, a hardened web server, operational rate limiting, and retention/moderation decisions. No password reset, email verification, editing, deletion, file uploads, or private messages are in scope. The feed shows only the newest 100 posts. Throttling is per process/IP, so a restart clears it. These limitations apply to both builds.

Feature prompts and actual defects are recorded in `../evidence/`. Browser preview was attempted but timed out in the environment; passing HTTP tests do not establish visual accessibility or cross-browser compatibility.
