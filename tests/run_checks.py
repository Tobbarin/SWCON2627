"""Save real acceptance-suite output for both builds; nonzero on any failure."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
failed = False
for build in ('vibe', 'sdd'):
    environment = dict(os.environ, CAMPUS_BUILD=build, PYTHONIOENCODING='utf-8')
    result = subprocess.run([sys.executable, str(ROOT / 'tests' / 'test_acceptance.py')], env=environment, capture_output=True, text=True, encoding='utf-8')
    output = result.stdout + result.stderr
    (ROOT / 'evidence' / f'test-results-{build}.txt').write_text(output, encoding='utf-8')
    print(build + ': ' + output.splitlines()[-1])
    failed |= result.returncode != 0
sys.exit(1 if failed else 0)
