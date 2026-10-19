# SDD implementation

Completed second implementation, written independently after the vibe version, from a previously published Spec Kit specification baseline.

```sh
python sdd/app.py --port 8001
```

Run from the repository root with Python 3.12+. Open http://127.0.0.1:8001. Register a new account; there are no seeded users. The separate database defaults to sdd/data/campus.sqlite3. Use --db PATH to choose another file. Stop with Ctrl+C.

PowerShell test command:

```powershell
$env:CAMPUS_BUILD='sdd'
python tests/test_acceptance.py
```

On POSIX: `CAMPUS_BUILD=sdd python tests/test_acceptance.py`.

The app.py adapter handles HTTP, domain.py handles persistence and security rules, and views.py renders escaped HTML. It imports no vibe Python. CSS is intentionally shared for visual parity. The external shared suite has 22 HTTP cases; tests/verify_runtime.py additionally exercises actual restart persistence and local response time.

Read specs/001-campus-circle/ for requirements, contracts, architecture, tasks, and traceability. tooling.md records actual Spec Kit execution and how to regenerate ignored upstream tooling.

Local teaching prototype only: standard-library HTTP server, loopback binding, HTTP-compatible cookies, process-local throttling. Public deployment requires a production server/TLS setup and operational decisions. No password recovery, uploads, editing/deletion, messaging, or moderation. Visual/browser acceptance remains unverified; see ../evidence/manual-review.md.
