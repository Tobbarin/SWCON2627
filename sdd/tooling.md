# Spec Kit provenance and workflow adaptation

The official PyPI package `specify-cli==0.12.11` was installed in the workspace tooling directory on 2026-10-19. `specify version` reported CLI 0.12.11, Python 3.12.14, Windows AMD64. Official setup reference: https://github.github.io/spec-kit/installation.html.

Actual execution used a small local Python wrapper importing `specify_cli.app` because `python -m specify_cli` has no package entry point. The normal installed console entry point is `specify_cli:main`.

Equivalent reproducible commands:

```sh
python -m pip install specify-cli==0.12.11
cd sdd
specify init --here --force --integration codex --script ps --ignore-agent-tools
```

Initialization succeeded and generated Codex skills, templates, PowerShell scripts, constitution template, and bundled workflow. No API keys were used. The force flag merged scaffolding into a directory containing only its placeholder README, before application source existed. The first pip attempt failed because of sandbox temp permissions; using workspace-local TEMP/TMP fixed installation.

The agent read generated specification and planning guidance, copied the spec template, wrote `.specify/feature.json`, then actually ran:

```powershell
./.specify/scripts/powershell/setup-plan.ps1 -Json
```

It returned the feature specification/plan paths for `specs/001-campus-circle` and feature identifier `001-campus-circle`. The agent filled the artifacts from the course scope and the shared observable application requirements, then added explicit contracts and tests before the independent implementation.

This is an adapted Spec Kit workflow executed directly by the coding agent. It does not claim that slash commands were dispatched through a separate UI, that a separate model generated specifications, or that formal mathematical verification was performed.

Upstream generated skills/templates/scripts/workflow files are ignored to keep the student repository focused on authored artifacts; regenerate them with the pinned command above. `.specify/init-options.json`, feature state, constitution, and all authored specifications are retained. Do not commit credential state if using any agent folder later.
