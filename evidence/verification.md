# Verification and audit record

## Vibe authentication milestone

Command: `python tests/test_acceptance.py` from the repository root.

2026-10-19: 8 tests passed in 5.123 seconds. Tests use real HTTP requests to an ephemeral local server and isolated SQLite databases. Covered home/security headers, registration/session rotation, case-insensitive duplicates, login/logout/hash storage, invalid registration, wrong password, missing CSRF, and throttling.

First execution: 8 setup errors, because the sandbox-selected OS temporary directory did not allow SQLite file access. Correction: create test temporary directories inside the ignored repository `data/test-runs` directory. This is an environment/harness issue, not evidence that registration logic failed. Database contexts were also made explicit about closing connections to avoid Windows file locks.

The original shell HTTP probe was blocked; HTTP checks subsequently passed through the acceptance harness after network permission was granted. No browser screenshot or visual verification has yet been completed.

## Vibe posting milestone
2026-10-19: all 14 HTTP tests passed in 9.041 seconds. Added persistence, anonymous posting rejection, post length bounds, escaped HTML, newest-first order, server-derived authorship, and CSRF session binding.

## Vibe final review
A15 initially failed: a non-ASCII CSRF value raised TypeError and disconnected the client. Fix: validate the 64-character hex token format before constant-time comparison. Final full run: 18 tests passed in 11.411 seconds. A16 verifies 500 emoji characters; A17 verifies expired sessions; A18 verifies unknown routes. Browser preview attempt timed out, so visual QA remains unverified.

## Shared contract expansion, before SDD implementation
A19-A22 added for request encoding/size/media type, repeated keys, newest-100 bounds, and NUL rejection. Vibe hardened for repeated keys and NUL. All 22 vibe tests passed in 13.832 seconds. SDD baseline invocation failed at import with FileNotFoundError for sdd/app.py, confirming no implementation existed when the tests/specification baseline was prepared. This is a missing-implementation baseline, not a count of 22 individually failed tests.
