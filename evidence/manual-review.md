# Human acceptance and browser review

Not yet performed. In-app browser attempts against ports 8000 and 8001 timed out even though local HTTP acceptance tests and subprocess probes passed. Do not infer visual/browser success from these automated results.

Suggested review for each build:

- [ ] Open the local URL in an ordinary browser; check desktop and narrow mobile layout.
- [ ] Navigate login/registration/composer/logout using keyboard only; confirm visible focus and readable errors.
- [ ] Create an account, publish, log out, and log back in.
- [ ] Open a second browser profile and verify public feed visibility and separate identity.
- [ ] Submit empty/too-long posts and inspect errors.
- [ ] Publish text resembling HTML; verify it stays literal text.
- [ ] Stop/restart and verify persistent content (also automated by verify_runtime.py).
- [ ] Capture screenshots for the course presentation if desired.
- [ ] Review public names/content and scope assumptions with an actual stakeholder.
- [ ] Supply team name, student names/IDs, actual roles/contributions, and personal reflections before submission.

This checklist is remaining human validation, not a record of completed actions.
