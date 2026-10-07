# Copyright (c) 2026 Contributors to the Eclipse Foundation
# SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
# AI Disclosure: Generated with OpenAI Codex; AI portions offered under CC0-1.0.
# Human curation retains Apache-2.0. Human review pending.
"""Retain and verify native test/configuration artifacts after measured execution."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET

sys.path.insert(0, '/home/jefferson/s-core_sw_fabric/src')
from score_sw_fabric.storage import validate_run_root

PACKET = Path(__file__).resolve().parents[1]
PROJECT = PACKET.parents[3]
LOCATION = json.loads((PACKET / 'run-location.json').read_text())
ROOT = Path(LOCATION['run_root'])
NATIVE = Path(LOCATION['native'])
validate_run_root(ROOT)
BASE = LOCATION['baseline']
CONFIGS = {
    'provider_test': 'score/launch_manager/src/daemon/src/control/control_provider_test_mw_com_config.json',
    'client_test': 'score/launch_manager/src/lm_control/src/details/test_lmcontrol_mw_com_config.json',
    'integration': 'tests/utils/environments/mw_com_config.json',
}
TESTS = {
    'score/launch_manager/src/daemon/src/control/control_provider_UT': 3,
    'score/launch_manager/src/lm_control/ilm_control_UT': 2,
    'score/launch_manager/src/lm_control/lm_control_impl_UT': 36,
    'scripts/config_mapping/tests/lifecycle_config_tests': 83,
    'tests/integration/switch_run_target/switch_run_target': 1,
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(name, value):
    (PACKET / name).write_text(json.dumps(value, indent=2) + '\n')

assert json.loads((PACKET / 'logs/affected-tests-complete-license.json').read_text())['exit_code'] == 0
results = []
for target, expected in TESTS.items():
    source = NATIVE / 'bazel-testlogs' / target
    destination = PACKET / 'logs/test-results' / target
    destination.mkdir(parents=True, exist_ok=True)
    for name in ['test.xml', 'test.log']:
        shutil.copyfile(source / name, destination / name)
    suites = ET.parse(source / 'test.xml').getroot()
    suites = [suites] if suites.tag == 'testsuite' else list(suites.iter('testsuite'))
    counts = {key: sum(int(s.get(key, '0')) for s in suites)
              for key in ['tests', 'failures', 'errors', 'skipped']}
    assert counts['tests'] == expected and all(counts[key] == 0 for key in ['failures', 'errors', 'skipped']), (target, counts)
    results.append({'target': '//' + target.rsplit('/', 1)[0] + ':' + target.rsplit('/', 1)[1], **counts})
write('native-test-results.json', results)

equivalence = []
baseline = {}
for profile, path in CONFIGS.items():
    original = subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=NATIVE)
    generated = (NATIVE / 'bazel-bin' / path).read_bytes()
    baseline[profile] = json.loads(original)
    assert json.loads(generated) == baseline[profile], profile
    destination = PACKET / 'generated' / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(generated)
    equivalence.append({'profile': profile, 'output': path, 'parsed_equal': True,
                        'original_sha256': sha(original), 'generated_sha256': sha(generated)})
write('configuration-equivalence.json', equivalence)
write('baseline-configurations.json', baseline)

runfiles = []
for profile, target in [('provider_test', 'score/launch_manager/src/daemon/src/control/control_provider_UT'),
                        ('client_test', 'score/launch_manager/src/lm_control/ilm_control_UT')]:
    path = CONFIGS[profile]
    payload = NATIVE / 'bazel-bin' / (target + '.runfiles') / '_main' / path
    assert json.loads(payload.read_bytes()) == baseline[profile]
    runfiles.append({'target': target, 'runfiles_key': '_main/' + path,
                     'parsed_equal': True, 'sha256': sha(payload.read_bytes())})
write('unit-runfiles-equivalence.json', runfiles)

archive = NATIVE / 'bazel-bin/tests/integration/switch_run_target/switch_run_target_test_tar.tar'
member = 'tests/switch_run_target/etc/mw_com_config.json'
with tarfile.open(archive) as bundle:
    content = bundle.extractfile(member).read()
assert json.loads(content) == baseline['integration']
write('packaged-configuration-equivalence.json', {'member': member, 'parsed_equal': True,
      'tar_sha256': sha(archive.read_bytes()), 'member_sha256': sha(content)})

changes = json.loads((PACKET / 'notice-equivalence.json').read_text())
for path, expected in changes['candidate_sources'].items():
    data = (NATIVE / path).read_bytes()
    assert sha(data) == expected, path
    destination = PACKET / 'candidate-source' / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
for path in [*CONFIGS.values(), *[p for p in changes['candidate_sources'] if p not in ['config/mw_com_config.bzl', 'LICENSES/CC0-1.0.txt']]]:
    destination = PACKET / 'baseline-source' / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=NATIVE))
prepared = PACKET / 'submission.patch'
# The packet's plain patch already binds this current-head, complete-license subject.
write('native-results.json', {'baseline': BASE, 'patch_sha256': sha(prepared.read_bytes()),
      'native_cases_passed': sum(item['tests'] for item in results), 'native_targets_passed': len(results),
      'failures': 0, 'errors': 0, 'skipped': 0, 'configuration_profiles_equal': 3,
      'unit_runfiles_equal': 2, 'integration_package_equal': True,
      'notice_only_change': False, 'notice_and_license_only_amendment': True,
      'human_review': 'Pending for this exact revision',
      'scope': 'Fresh x86_64 Linux host-mode affected checks on pinned baseline; full native CI and QNX not executed'})
print(json.dumps(json.loads((PACKET / 'native-results.json').read_text())))
