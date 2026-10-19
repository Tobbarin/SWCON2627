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

## SDD authentication slice
14 selected HTTP cases passed in 8.433 seconds: A01-A08, A14/A15/A17-A20. Posting cases not yet implemented or claimed. Independent domain, HTTP, and view modules were written after the published specification baseline.

## SDD feed slice
All 22 shared HTTP tests passed in 13.745 seconds. Both builds then passed actual subprocess restart, persisted session, and login-after-restart probes. runtime-metrics.json records 20 sequential home requests with 100 stored posts: vibe median 2.761 ms, maximum 27.990 ms; SDD median 2.939 ms, maximum 24.254 ms. Both meet the local median-under-2000-ms target. These are warm local measurements, not deployment benchmarks. The probe initially retained its own seeding SQLite handle and hit a Windows cleanup lock; explicit closing fixed the harness, with no application code change.

## Final reproducibility run
run_checks.py saved genuine output for both builds: vibe 22/22 in 13.869 seconds; SDD 22/22 in 13.830 seconds. Both exit 0. No coverage instrumentation, browser success, stakeholder acceptance, or CI run is claimed. The SDD app was also launched on port 8001 for browser QA, but the in-app browser timed out again.
