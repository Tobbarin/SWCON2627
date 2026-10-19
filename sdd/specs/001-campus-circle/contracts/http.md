# HTTP form contract v1

All HTML UTF-8. GET / returns 200 for visitors/members; members see composer. GET /register and /login return 200 to guests and 303 Location:/ to members. GET /style.css returns CSS. Unknown routes return 404.

POST bodies: application/x-www-form-urlencoded, Content-Length integer from 0 to 8192 bytes, at most ten fields, valid UTF-8. Invalid encoding returns 400, unsupported media type 415, missing/invalid/oversized length 413. Reject repeated form keys with 400 to avoid ambiguous values. A posted CSRF token must be exactly 64 lowercase hex characters and match the current session; otherwise 403 with no domain mutation. Security checks happen before route actions.

| Route | Fields besides csrf | Success | Other outcomes |
|---|---|---|---|
| POST /register | username, name, password | 303 /; new account and rotated authenticated session | 400 invalid; 409 duplicate; 429 throttle |
| POST /login | username, password | 303 /; rotated authenticated session | 400 invalid format; 401 generic credentials failure; 429 throttle |
| POST /logout | none | 303 /; previous server session removed | 403 invalid CSRF |
| POST /posts | body | 303 /; one post owned by session account | 401 guest; 400 invalid body; 403 invalid CSRF |

Passwords preserve whitespace. Names/posts trim leading/trailing whitespace and reject NUL. Unknown extra fields, including supplied author identifiers, never determine ownership. Posts accept Unicode code points, including 500 emoji within the encoded request bound.

Session cookie: circle_session; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800. Use no-store, nosniff, same-origin referrer policy, and CSP default-src self, no scripts, no framing, no base URI, same-origin form actions. No TLS/public deployment claim.

FR01 -> A02/A03/A05; FR02 -> A02/A04/A06/A17; FR03 -> A01/A09/A13/A21; FR04 -> A10/A11/A12/A13/A16/A22; FR05 -> A07/A14/A15/A18/A19/A20. NFR01 -> A01/A02/A04/A07/A12/A14/A15/A17. NFR02 -> A08. NFR03 -> manual review pending. NFR04 -> A09 plus restart probe. NFR05 -> documented run commands. NFR06 -> performance probe.
