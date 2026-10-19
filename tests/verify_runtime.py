"""Actual process restart and bounded local performance probe for both builds."""
import http.client
from contextlib import closing
import json
from pathlib import Path
import re
import socket
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]

def probe(build):
    runtime = ROOT / 'data' / 'runtime-probes'
    runtime.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=runtime) as temporary:
        database = Path(temporary) / 'probe.sqlite3'
        with socket.socket() as selector:
            selector.bind(('127.0.0.1', 0))
            port = selector.getsockname()[1]
        cookie = ''
        def request(path='/', fields=None):
            nonlocal cookie
            connection = http.client.HTTPConnection('127.0.0.1', port, timeout=4)
            headers = {'Cookie': cookie}
            if fields is not None:
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            connection.request('GET' if fields is None else 'POST', path, None if fields is None else urlencode(fields), headers)
            response = connection.getresponse()
            body = response.read().decode()
            if response.getheader('Set-Cookie'):
                cookie = response.getheader('Set-Cookie').split(';')[0]
            status = response.status
            connection.close()
            return status, body
        def start():
            process = subprocess.Popen([sys.executable, str(ROOT / build / 'app.py'), '--port', str(port), '--db', str(database)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                try:
                    if request()[0] == 200:
                        return process
                except OSError:
                    pass
                if process.poll() is not None:
                    raise RuntimeError(f'{build} exited before readiness: {process.returncode}')
                time.sleep(.05)
            process.terminate()
            process.wait(timeout=5)
            raise RuntimeError(f'{build} readiness timeout')
        def token(path='/'):
            return re.search(r'name="csrf" value="([a-f0-9]+)"', request(path)[1]).group(1)
        process = start()
        try:
            assert request('/register', dict(csrf=token('/register'), username='probe_user', name='Runtime Probe', password='test-only-password-123'))[0] == 303
            assert request('/posts', dict(csrf=token(), body='persisted-across-process-restart'))[0] == 303
        finally:
            process.terminate()
            process.wait(timeout=5)
        process = start()
        try:
            status, body = request()
            assert status == 200 and 'persisted-across-process-restart' in body and 'Hi, Runtime Probe' in body
            assert request('/logout', dict(csrf=token()))[0] == 303
            assert request('/login', dict(csrf=token('/login'), username='probe_user', password='test-only-password-123'))[0] == 303
            with closing(sqlite3.connect(database)) as connection:
                with connection:
                    connection.executemany('INSERT INTO posts(user_id,body,created) VALUES (1,?,?)', [(f'Benchmark {i}', '2026-10-19T00:00:00Z') for i in range(99)])
            request()  # unmeasured warm-up
            samples = []
            for _ in range(20):
                begin = time.perf_counter()
                assert request()[0] == 200
                samples.append((time.perf_counter() - begin) * 1000)
            return {'process_restart_persistence': 'pass', 'session_persisted': 'pass', 'login_after_restart': 'pass',
                'stored_posts': 100, 'sequential_samples': 20, 'median_home_ms': round(statistics.median(samples), 3),
                'max_home_ms': round(max(samples), 3), 'target_median_below_2000ms': statistics.median(samples) < 2000,
                'conditions': 'loopback HTTP, Python 3.12, Windows, one process per build; no concurrency/load guarantee'}
        finally:
            process.terminate()
            process.wait(timeout=5)

if __name__ == '__main__':
    results = {build: probe(build) for build in ('vibe', 'sdd')}
    (ROOT / 'evidence' / 'runtime-metrics.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(results, indent=2))
