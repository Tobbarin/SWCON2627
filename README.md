# Campus Circle — two ways to build the same social app

Course: Software Construction 2026–27 (SWCON2627).

Campus Circle is a small student community website. The shared scope is account registration, login, logout, a shared home feed, and publishing text posts as the signed-in user. Both implementations will use the same scope and visual design.

## Current status

Both implementations are complete and published incrementally at https://github.com/Tobbarin/SWCON2627. Each passes 22 shared HTTP tests, and both passed actual process-restart probes. The SDD specification baseline was published before its application source. The course report is in [report/experience-report.md](report/experience-report.md), with a printable PDF alongside it.

Start with [RUN.md](RUN.md). Python 3.12+ is required; there are no application dependencies. Run `python vibe/app.py --port 8000` and `python sdd/app.py --port 8001` in separate terminals. The builds have independent databases.

Visual/browser and stakeholder acceptance remain pending. The report is an AI-assisted review draft: students must supply real team details, contributions, and personal reflections before submission. Neither app is a production deployment.

The user requested incremental **pushes**, not only incremental local commits. Development will pause at each push boundary if GitHub access is unavailable; the whole project must not be completed offline and uploaded at the end.

## Layout

- `vibe/`: first implementation, built through short natural-language feature iterations and feedback.
- `sdd/`: second, independent implementation; specifications, contracts, acceptance criteria, and tasks will precede its code.
- `evidence/`: course brief extraction, actual development prompts, milestone and verification records.
- `report/`: eventual comparison report, based on recorded observations.

## Implementation direction

A server-rendered Python application with SQLite, HTML, CSS, and a small amount of JavaScript keeps setup reproducible and dependency costs low. Accounts and posts will persist on the server. Authentication must use password hashing and server-side sessions; the app must render user posts as text and validate requests. The implementation and tests will establish the actual controls, rather than treating this README as proof of security.

The SDD build used an adapted GitHub Spec Kit 0.12.11 workflow, actually initialized after the vibe build. See [sdd/tooling.md](sdd/tooling.md) for provenance and execution details. Specifications, contracts, and the shared acceptance baseline preceded independent SDD source. Only CSS and external tests were reused between builds.

## Development and evidence rules

1. Finish, verify, commit, and push one milestone at a time.
2. Complete the vibe version before starting the SDD implementation.
3. Do not copy the vibe implementation into the SDD project and call it an independent build.
4. Record actual prompts, outputs, defects, test results, and limitations; do not invent failures or measurements.
5. Preserve authentic authorship. AI-created commits must not be represented as contributions by students.
6. Keep personal student identifiers out of a public repository until the student deliberately supplies them for publication.

## Completed publication sequence

0. Repository scaffold and evidence collection.
1. Vibe: running application shell and responsive page.
2. Vibe: registration and session authentication.
3. Vibe: posting and persistent shared feed.
4. Vibe: tests, review, fixes, and usage documentation.
5. SDD: toolkit setup, constitution, specification, contracts, plan, and acceptance tests.
6. SDD: authentication implementation and verification.
7. SDD: posting and feed implementation and verification.
8. Comparison, report, and final reproducibility checks.

Actual remote commit IDs and verification outcomes are in [evidence/milestones.md](evidence/milestones.md). Publication used the GitHub connector after local credential-helper failures. The connected account's commit attribution does not establish student code authorship; implementation and drafting were AI-assisted in Codex.
