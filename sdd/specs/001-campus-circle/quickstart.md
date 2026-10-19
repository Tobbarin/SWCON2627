# Quickstart

From repository root: `python sdd/app.py --port 8001`. Open http://127.0.0.1:8001. Create a fresh account and publish a post. Defaults to sdd/data/campus.sqlite3; override with --db PATH. Stop with Ctrl+C.

PowerShell verification: `$env:CAMPUS_BUILD='sdd'; python tests/test_acceptance.py`.
POSIX verification: `CAMPUS_BUILD=sdd python tests/test_acceptance.py`.

For the first auth-only slice, select Acceptance.test_A01_home_and_security_headers through A08 individually; posting cases are expected to fail until that slice is implemented. The final suite must pass in full.
