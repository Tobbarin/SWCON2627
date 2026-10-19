# Tasks: Campus Circle

## Phase 1: Specify/design before application code
- [x] T001 Initialize genuine Spec Kit 0.12.11 with Codex/PowerShell.
- [x] T002 Establish constitution, scope, user scenarios, requirements and quality checklist.
- [x] T003 Run setup-plan; write research, data model, HTTP contract, quickstart and traceability.
- [ ] T004 Add contract tests A19–A22 before implementation; publish baseline.

## Phase 2: User story 1 — authentication
- [ ] T005 Implement domain persistence, validation, hashing, throttling and session transitions in domain.py (FR01/FR02, NFR01/02/04).
- [ ] T006 Implement independent HTTP auth adapter and views (FR05/NFR03).
- [ ] T007 Run A01–A08, A14/A15/A17–A20, review, publish auth slice.

## Phase 3: User stories 2/3 — feed
- [ ] T008 Implement validated post creation and newest-100 public feed (FR03/FR04).
- [ ] T009 Run full HTTP suite, persistence restart and performance probes; publish.

## Phase 4: Converge
- [ ] T010 Audit implementation against each requirement; fix with regression tests.
- [ ] T011 Record measured results, remaining verification gaps, and comparison validity limitations.
- [ ] T012 Final run documentation and report; publish final evidence.

Dependencies: T001–T004 precede T005. T005/T006 precede T007. T007 must be published before T008. T008 precedes T009. T010–T012 follow all implemented stories. No parallel-agent work is needed.
