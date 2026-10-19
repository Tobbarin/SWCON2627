# Research and decisions

1. Python/SQLite: verified available, supports persistent relational data without dependencies. Tradeoff: standard-library HTTP server is suitable only for a local teaching prototype.
2. Password storage: PBKDF2-HMAC-SHA256, 600,000 iterations, independent random 16-byte salt per account. Compare fixed-length hex digests with compare_digest. Account-not-found still performs a derivation. This records an implementation decision, not certification of password security.
3. CSRF: 32-byte random secret bound to server session. Validate lowercase hex format before string compare to avoid the Unicode failure observed in the vibe build.
4. Sessions: 32-byte random opaque token, server persistence, eight-hour absolute expiry, rotate on successful auth, remove on logout. HttpOnly/SameSite=Strict/Path=/ cookies. Secure deliberately omitted for loopback HTTP.
5. SDD tooling: official Spec Kit 0.12.11 from PyPI, supported by https://github.github.io/spec-kit/installation.html. Initialized Codex integration with PowerShell scripts. Existing README was the only nonempty project file. setup-plan.ps1 executed against the recorded feature directory.
6. Workflow adaptation: the agent executes the installed scripts and writes the specified artifacts directly in this chat; slash-command UI invocations are not claimed. Installed command/template guidance informs the workflow. No separate autonomous Spec Kit model runs occurred.
7. Reuse controls: share CSS and external acceptance tests only. Independent Python implementation, separate database, same requirements. Learning transfer prevents a causal claim that SDD alone improved defects or speed.
