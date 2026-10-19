# Verification and audit record

## Vibe authentication milestone

Command: `python tests/test_acceptance.py` from the repository root.

2026-10-19: 8 tests passed in 5.123 seconds. Tests use real HTTP requests to an ephemeral local server and isolated SQLite databases. Covered home/security headers, registration/session rotation, case-insensitive duplicates, login/logout/hash storage, invalid registration, wrong password, missing CSRF, and throttling.

First execution: 8 setup errors, because the sandbox-selected OS temporary directory did not allow SQLite file access. Correction: create test temporary directories inside the ignored repository `data/test-runs` directory. This is an environment/harness issue, not evidence that registration logic failed. Database contexts were also made explicit about closing connections to avoid Windows file locks.

The original shell HTTP probe was blocked; HTTP checks subsequently passed through the acceptance harness after network permission was granted. No browser screenshot or visual verification has yet been completed.
