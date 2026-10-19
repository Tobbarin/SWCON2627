# Implementation Plan: Campus Circle
Date: 2026-10-19. Baseline: spec.md and constitution 1.0.0.

## Summary
Build an independent layered implementation, matching the observable scope and visual styling of the vibe application. The existing HTTP acceptance suite is a comparison control, frozen at 18 cases before this implementation. Additional contract cases will be added before implementation for request parsing and feed limits.

## Technical Context
Python 3.12 standard library; SQLite persistence; server-rendered HTML; CSS. Local loopback port 8001. No application packages. Spec Kit 0.12.11 supplies the workflow scaffolding; its dependency packages are development tooling only.

## Constitution Check
Requirements have identifiers and tests. Identity and security invariants are explicit. Domain/store logic will live in domain.py, views in views.py, HTTP adapters in app.py. No vibe Python imports/copies. Shared style.css is deliberate visual parity. Scope excludes public hosting. Gates pass for implementation; human acceptance and visual QA remain pending.

## Phase 0 — Research
Resolved choices in research.md. No unresolved technology question requires an agent delegation. Use the already verified available Python/SQLite runtime and standard-library cryptographic functions. The installed Spec Kit entry point has no __main__; invoke its console entry point rather than python -m specify_cli.

## Phase 1 — Design
data-model.md defines records/invariants. contracts/http.md defines routes, form fields, status codes, and security transitions. quickstart.md defines reproducibility. Publish these artifacts before application source.

## Source Structure
- app.py: request parsing, session resolution, status/redirect responses, route dispatch.
- domain.py: SQLite lifecycle, account validation/authentication, sessions, posts, authentication throttle.
- views.py: escaped HTML rendering and form construction.
- style.css: visual CSS shared from the vibe build, explicitly disclosed.
- ../tests/test_acceptance.py: black-box test harness, selected with CAMPUS_BUILD=sdd.

## Verification
Write contract tests before code, run authentication slice separately, then all tests. Perform audit against contract and record limitations. Use a new process restart test and a local performance probe. No coverage percentage without instrumentation. Browser preview is attempted separately and may be blocked by this environment.

## Complexity Tracking
Three application modules vs one in the vibe build is intentional separation for auditing; no framework, plugin architecture, ORM, or external service is necessary for this bounded scope.
