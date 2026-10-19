# Development prompt record

## P001 — initial user request (2026-10-19)

The exact task-bearing text is preserved below; the example project description preceding it also specified login, registration, and posting.

> so the basics are, making a website social media with the login, registration and postion, but you need to make the same website 2 times, once with vibe coding and once with with SDD, if you could first make the vibe coding, this need to be pushed to a github, but dont make everything and then push, push little at a time, like when something is finnished, this pushing should be for booth projects, and after you have made the vibe coing, make the same porject using sdd, but you have the project description page so read from that and do what you think is best

Purpose: create comparable implementations and preserve incremental repository evidence.

Initial outcome: course brief read, project chosen, scaffold prepared. GitHub integration is not connected and no target repository was supplied. Work paused before feature implementation to preserve the requested incremental push workflow.

The environment is Codex desktop. No exact model identifier has been independently verified for the report. Do not infer it from available model names.

## Recording subsequent iterations

## V001 — agent-authored implementation instruction

Build the first running Campus Circle page using Python's standard-library HTTP server and separate HTML/CSS. Use a calm green student-community design, responsive columns, an honest empty feed, and no simulated working authentication. Verify the server response before publishing this milestone.

Observed: application started on port 8000 and Python compilation succeeded. The first HTTP readiness check was blocked by network permissions; it was not a pass. Network access was then granted for a retry. Authentication and posting intentionally awaited later iterations.

## V002 — agent-authored implementation instruction

Add server-persisted registration, login, and logout to the existing shell. Use SQLite, salted PBKDF2 password hashes, opaque server sessions rotated at login, session-bound CSRF tokens, validation, and a small per-client authentication throttle. Keep the app runnable without installing dependencies. Do not add posting yet.

## V003 — agent-authored implementation instruction

Add a signed-in composer and shared persistent feed to the existing vibe build. Limit trimmed posts to 1–500 characters, derive the author from the server session, escape all user content, and show the latest 100 posts in descending insertion order. Extend HTTP tests for persistence, anonymous rejection, boundaries, XSS escaping, ordering, author spoofing, and session-bound CSRF.

## V004 — review/refinement instruction

Extend verification to malformed Unicode CSRF values, 500-character Unicode posts, expired sessions, and unknown routes. Reject malformed CSRF with HTTP 403 rather than disconnecting.

Observed failure: A15 submitted `å` as CSRF; `hmac.compare_digest` raised TypeError because string comparison accepts ASCII only. A16 (500 emoji post) passed. Refinement: require the submitted CSRF value to match exactly 64 lowercase hex characters before constant-time comparison. The failure was reproduced through HTTP before the fix.

Tooling failure: an initial file-replacement patch targeted the same path twice and was rejected before writing; the patch was reapplied as a single update. This was an edit-tool error, not an application defect.

For each material user prompt or agent implementation instruction, preserve its actual text, purpose, expected result, observed output, any measured defect, and the exact refinement if one was made. Clearly distinguish user prompts from agent-authored implementation instructions. Do not fabricate additional user turns, hidden reasoning, failed attempts, or human reviews.

## S001 - agent-authored specification instruction
Use installed Spec Kit 0.12.11 scaffolding to define equivalent Campus Circle user stories, requirements, constitution, data states, HTTP contracts, plan, tasks, and acceptance-test mappings before writing independent Python code. Disclose prior-build learning and shared CSS/tests. Publish the baseline before implementation.

## V005 - shared contract refinement
Reject ambiguous repeated form keys and NUL in display names/posts; parse percent-encoded UTF-8 strictly. Add A19-A22 and run them against both builds. These controls were applied to the vibe build before SDD code existed.

## S002 - agent-authored implementation instruction
Implement only the SDD authentication slice from the published constitution, spec and HTTP contract. Use independent domain.py, views.py and app.py; do not import or copy vibe Python. Keep the shared CSS and external acceptance harness as comparison controls. Run the authentication and malformed-request cases before publishing.

## S003 - agent-authored implementation instruction
Implement FR03/FR04 from the committed SDD contract: authorized publication, validated 1-500-character text, session-derived author, persistent newest-100 public feed, and escaped rendering. Run the full shared suite and actual process-restart/performance probes. Record harness defects separately from application defects.
