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

For each material user prompt or agent implementation instruction, preserve its actual text, purpose, expected result, observed output, any measured defect, and the exact refinement if one was made. Clearly distinguish user prompts from agent-authored implementation instructions. Do not fabricate additional user turns, hidden reasoning, failed attempts, or human reviews.
