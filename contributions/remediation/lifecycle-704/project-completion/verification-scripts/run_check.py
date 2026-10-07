# *******************************************************************************
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# AI Disclosure: Prepared with OpenAI Codex. AI-generated portions are
# offered under CC0-1.0; original human content retains Apache-2.0.
# Human review pending.
# Assisted-by: OpenAI Codex (model revision unavailable)
# SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
# *******************************************************************************

"""Run a named check against the bound disposable Lifecycle candidate."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

sys.path.insert(0, '/home/jefferson/s-core_sw_fabric/src')
from score_sw_fabric.storage import validate_run_root

PACKET = Path(__file__).resolve().parents[1]
LOCATION = json.loads((PACKET / 'run-location.json').read_text())
ROOT = Path(LOCATION['run_root'])
validate_run_root(ROOT)
NATIVE = Path(LOCATION['native'])
environment = dict(os.environ, **json.loads((ROOT / 'environment.json').read_text()))
environment['PATH'] = environment.pop('PATH_PREFIX') + ':' + os.environ['PATH']
label, *command = sys.argv[1:]
if command[0] == 'bazel':
    command[0] = str(NATIVE / '.llm_tmp/bin/bazel')
elif command[0] == 'buildifier':
    command[0] = str(ROOT / 'tools/buildifier')
started = time.time()
before = subprocess.check_output(['git', 'diff', '--binary'], cwd=NATIVE)
with (PACKET / 'logs' / (label + '.log')).open('w') as output:
    process = subprocess.Popen(command, cwd=NATIVE, env=environment,
                               stdout=output, stderr=subprocess.STDOUT,
                               start_new_session=True)
    try:
        while process.poll() is None:
            validate_run_root(ROOT)
            time.sleep(2)
    except BaseException:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait()
        raise
validate_run_root(ROOT)
result = {'argv': command, 'cwd': str(NATIVE), 'exit_code': process.returncode,
          'elapsed_seconds': time.time() - started,
          'started_at_utc_epoch': started,
          'baseline': LOCATION['baseline'],
          'candidate_diff_sha256_before': hashlib.sha256(before).hexdigest(),
          'candidate_diff_sha256_after': hashlib.sha256(subprocess.check_output(
              ['git', 'diff', '--binary'], cwd=NATIVE)).hexdigest(),
          'log_sha256': hashlib.sha256((PACKET / 'logs' / (label + '.log')).read_bytes()).hexdigest()}
(PACKET / 'logs' / (label + '.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
print((PACKET / 'logs' / (label + '.log')).read_text()[-3500:])
sys.exit(process.returncode)
