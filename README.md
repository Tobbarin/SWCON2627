# Campus Circle — two ways to build the same social app

Course: Software Construction 2026–27 (SWCON2627).

Campus Circle is a small student community website. The shared scope is account registration, login, logout, a shared home feed, and publishing text posts as the signed-in user. Both implementations will use the same scope and visual design.

## Current status

Milestone 0: repository and evidence collection prepared. GitHub connected on 2026-10-19; initial README published to https://github.com/Tobbarin/SWCON2627. Implementation has not started.

The user requested incremental **pushes**, not only incremental local commits. Development will pause at each push boundary if GitHub access is unavailable; the whole project must not be completed offline and uploaded at the end.

## Layout

- `vibe/`: first implementation, built through short natural-language feature iterations and feedback.
- `sdd/`: second, independent implementation; specifications, contracts, acceptance criteria, and tasks will precede its code.
- `evidence/`: course brief extraction, actual development prompts, milestone and verification records.
- `report/`: eventual comparison report, based on recorded observations.

## Implementation direction

A server-rendered Python application with SQLite, HTML, CSS, and a small amount of JavaScript keeps setup reproducible and dependency costs low. Accounts and posts will persist on the server. Authentication must use password hashing and server-side sessions; the app must render user posts as text and validate requests. The implementation and tests will establish the actual controls, rather than treating this README as proof of security.

The SDD toolkit will be selected and its official setup verified after the vibe implementation is complete. The course brief specifically requests identification of an SDD tool and mentions Spec Kit. We will not claim to have used a toolkit that was not actually run.

## Development and evidence rules

1. Finish, verify, commit, and push one milestone at a time.
2. Complete the vibe version before starting the SDD implementation.
3. Do not copy the vibe implementation into the SDD project and call it an independent build.
4. Record actual prompts, outputs, defects, test results, and limitations; do not invent failures or measurements.
5. Preserve authentic authorship. AI-created commits must not be represented as contributions by students.
6. Keep personal student identifiers out of a public repository until the student deliberately supplies them for publication.

## Planned push boundaries

0. Repository scaffold and evidence collection.
1. Vibe: running application shell and responsive page.
2. Vibe: registration and session authentication.
3. Vibe: posting and persistent shared feed.
4. Vibe: tests, review, fixes, and usage documentation.
5. SDD: toolkit setup, constitution, specification, contracts, plan, and acceptance tests.
6. SDD: authentication implementation and verification.
7. SDD: posting and feed implementation and verification.
8. Comparison, report, and final reproducibility checks.

These are planning boundaries, not claims of completed work. Record each actual push in `evidence/milestones.md`.
