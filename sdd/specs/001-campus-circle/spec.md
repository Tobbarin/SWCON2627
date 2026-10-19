# Feature Specification: Campus Circle
**Feature directory**: 001-campus-circle (no feature branch required)
**Created**: 2026-10-19
**Status**: Implementation baseline; AI-reviewed, pending human acceptance
**Input**: Build the same social website a second time using SDD, after completing the vibe implementation. Core functions: registration, login, and posting.

## User Scenarios & Testing
### User Story 1 — Join and return (P1)
A campus visitor creates a pseudonymous account and can return to it later.
Why: posting needs a persistent identity. Independently test with registration and login before posts exist.
1. Given a new username, when valid registration is submitted, then an account is persisted and the visitor is signed in.
2. Given an existing username in any letter case, when registration is repeated, then it is rejected without creating another account.
3. Given a signed-in visitor, when they log out, then the old session cannot identify them; valid credentials can establish a new session.

### User Story 2 — Share a moment (P1)
A signed-in member publishes a short text update.
Why: this is the central social function. Independently test after an account is available.
1. Given a signed-in member, when a valid post is published, then it appears with that member's display name and username.
2. Given no signed-in session, when a post is submitted, then no post is stored.
3. Given a manipulated author field, when a post is submitted, then its author still comes from the session.

### User Story 3 — Read the community (P2)
Any visitor reads the newest public updates.
Why: public reading gives the app value before joining. Independently test with an empty or prepared dataset.
1. Given no posts, when the home page opens, then an honest empty state appears.
2. Given multiple posts, when the feed opens, then the newest insertion appears first and no more than 100 are shown.
3. Given content containing HTML, when displayed, then it appears as text without executing.

### Edge Cases
Whitespace-only posts; exactly 500 Unicode code points; 501 characters; duplicate usernames differing only by ASCII case; expired or stolen old session tokens; missing, mismatched, or Unicode CSRF values; invalid form encoding; oversized requests; unknown routes.

## Requirements
Functional requirements describe observable services. Non-functional requirements constrain quality and operation.
- FR01: Register with a username of 3–24 ASCII letters, digits, or underscores, a trimmed 1–50 character display name, and a 12–128 character password. Do not trim passwords. Usernames are unique without ASCII case sensitivity.
- FR02: Log in with the same credentials case-insensitively for username. Wrong credentials reveal only a generic failure. Rotate sessions at successful registration/login. Log out invalidates the server record.
- FR03: Any visitor reads the newest 100 posts by descending insertion identifier. Posts survive application restart.
- FR04: Only signed-in members can publish. Trim surrounding whitespace; accept 1–500 Unicode code points. Preserve internal newlines. Identity is never supplied by the browser.
- FR05: Invalid forms return a clear error and do not mutate user/post data. Successful form submissions redirect to the home page.
- NFR01 Security: hash passwords with a per-user random salt, enforce session-bound CSRF on every POST, reject malformed tokens safely, escape all user text, parameterize SQL, and expire sessions after eight hours.
- NFR02 Security: allow at most ten authentication attempts per client IP per rolling 60 seconds in one process. The next attempt returns a controlled rate-limit response.
- NFR03 Usability: responsive layout, associated labels, visible keyboard focus, meaningful titles, empty state, and error text. Manual browser review remains required; no conformance claim follows from HTML alone.
- NFR04 Reliability: committed users/posts survive restart. Isolated repeatable HTTP tests exercise success and failure paths. SQLite enforces foreign keys and username uniqueness.
- NFR05 Portability: run with Python 3.12+ and its standard library on a loopback HTTP server. No application dependency installation.
- NFR06 Performance: target a median home-page response below two seconds over 20 sequential requests with 100 stored posts on the development machine; measure and report actual results. This is a local target, not a load guarantee.

## Key Entities
Account: identifier, username, display name, salt, password hash. Session: unpredictable identifier, CSRF secret, optional account, expiration. Post: identifier, account, text, UTC creation timestamp.

## Success Criteria
SC01: All FR01–FR05 acceptance cases pass through HTTP against both builds.
SC02: Invalid state-changing requests create no users/posts; HTML-like text renders escaped.
SC03: Persistent data remains readable after server restart.
SC04: Both implementations meet the same scope and document verification gaps.
SC05: NFR06 is measured separately and its pass/fail result is recorded.

## Assumptions and exclusions
The student community is conceptual; no actual university identity integration or enrollment checks. Posts and names are public to visitors of this server. No uploads, recovery email, private messaging, editing, deletion, or moderation. Human stakeholders and team contributions are not simulated. The second build can learn from defects found in the first; this is a known validity limitation.
