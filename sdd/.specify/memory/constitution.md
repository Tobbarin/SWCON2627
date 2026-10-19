# Campus Circle Constitution
Version 1.0.0 — ratified 2026-10-19 by the AI agent for this course prototype; human review pending.

1. Requirements precede code. Each behavior must have an identifier, an acceptance scenario, and a verification method. Unverified requirements remain unverified.
2. Keep scope equivalent to the completed vibe app: registration, login/logout, public feed, and authenticated text posts. No feature expansion to improve one build's comparison score.
3. Derive identity from server state. Never persist plaintext passwords. Reject invalid state-changing requests, parameterize SQL, and escape user content.
4. Separate persistence/security rules, HTTP orchestration, and HTML rendering. Do not import or copy the vibe application's Python code. Shared visual CSS and the external test harness are explicitly permitted comparison controls.
5. Publish specifications before implementation; publish each verified slice separately. Do not fabricate Git history, prompts, student work, reviews, failures, or performance results.
6. Local prototype only. Production readiness, accessibility conformance, and legal compliance require separate evidence.

Governance: changes to observable behavior require updating spec.md, contracts/http.md, tasks.md, and acceptance tests before implementation. Fixes that restore an existing contract require a regression test and audit record.
