# Run Campus Circle

Install Python 3.12 or newer. No application packages are required.

Open two terminals in the repository directory:

```sh
python vibe/app.py --port 8000
```

```sh
python sdd/app.py --port 8001
```

On Windows, `py -3.12` can replace `python` if that is your installed launcher's command. Open http://127.0.0.1:8000 and http://127.0.0.1:8001. Each build has its own database and account set. Create an account on each, publish, log out, and log back in. Use separate browser profiles when comparing multiple users. There are no default accounts.

Stop each server with Ctrl+C. Users/posts/sessions persist in its ignored data/campus.sqlite3. An eight-hour session expiry is absolute; restarting does not renew it. A custom --db PATH can isolate another demonstration.

## Verify both

```sh
python tests/run_checks.py
python tests/verify_runtime.py
```

run_checks saves genuine logs in evidence/test-results-vibe.txt and test-results-sdd.txt. verify_runtime starts/stops its own servers and saves runtime-metrics.json. Both create isolated temporary databases under ignored data/. The metrics file changes on each run. These scripts do not change your demonstration accounts.

Human browser and acceptance review remains in evidence/manual-review.md. Read each build's README for prototype limits.

## Documents

- evidence/ contains actual prompts, milestone IDs, audit history, raw test logs, and measurements.
- sdd/specs/001-campus-circle/ contains the specification baseline and completed task record.


