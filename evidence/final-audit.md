# Final convergence audit

2026-10-19. AI source review and executed verification; no human acceptance claim.

| Requirement | Implementation evidence | Verification / remaining limit |
|---|---|---|
| FR01 registration | Vibe auth route; SDD Store.register, uniqueness constraint | A02/A03/A05 pass in both |
| FR02 identity | Password derivation, rotated opaque sessions, logout deletion | A02/A04/A06/A17 pass; actual restart login passes |
| FR03 feed | SQL newest-100 join in both builds | A01/A09/A13/A21 pass; actual process persistence passes |
| FR04 publication | Session-derived user, trimmed bounded text, escaped HTML | A10/A11/A12/A13/A16/A22 pass |
| FR05 invalid requests | Controlled status/error handling and no account/post mutation on rejected paths | A07/A14/A15/A18/A19/A20 pass; test assertions sample contract behavior, not exhaustive proof |
| NFR01 security | Explicit CSRF format/match, parameterized SQL, headers, password hashing | Automated selected cases pass; no independent penetration test |
| NFR02 throttle | Locked process-local per-IP rolling window | A08 passes; no distributed/production control |
| NFR03 usability | Labels, responsive CSS, focus and errors in source | Browser preview timed out; manual/assistive technology review pending |
| NFR04 reliability | Transactions, constraints, explicitly closed connections | HTTP suite and actual restart probes pass |
| NFR05 portability | Standard-library-only apps and documented commands | Executed on bundled Windows Python 3.12.14; other operating systems not executed |
| NFR06 performance | 100-post feed, 20 sequential warmed local requests | Both medians under 2000 ms; no concurrency guarantee |

The SDD build imports no Python code from vibe. Shared CSS is identical by design and the black-box harness is reused. No package dependencies were invented for the application. The exact serving model, student contributions, coverage percentage, manual review, and CI execution are not established and are not claimed.

The final report PDF was rendered to PNGs. All nine pages were reviewed in a contact sheet, with the test table and workflow page also inspected individually. This validates report layout; it does not substitute for website visual review.
