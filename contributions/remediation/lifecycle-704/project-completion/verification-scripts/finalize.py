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

"""Seal the current-head project artifact packet without supplying human gates."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parents[1]
PROJECT = PACKET.parents[3]
REL = 'remediation/lifecycle-704/project-completion/'

def load(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

location = load(PACKET / 'run-location.json')
native = Path(location['native'])
results = load(PACKET / 'native-results.json')
scoped_hooks = load(PACKET / 'logs/pre-commit.json')
assert scoped_hooks['candidate_diff_sha256_before'] == scoped_hooks['candidate_diff_sha256_after']
hooks = load(PACKET / 'logs/pre-commit-all-files.json')
assert hooks['candidate_diff_sha256_before'] == hooks['candidate_diff_sha256_after'], 'Native formatter changed source'
assert results['native_cases_passed'] == 125
for name in ['buildifier', 'gitlint']:
    assert load(PACKET / 'logs' / (name + '.json'))['exit_code'] == 0
changes = load(PACKET / 'notice-equivalence.json')
for relative, expected in changes['candidate_sources'].items():
    assert sha(native / relative) == expected, relative
for relative in changes['deleted_paths']:
    assert not (native / relative).exists(), relative
assert hashlib.sha256(subprocess.check_output(['git', 'diff', '--binary'], cwd=native)).hexdigest() == results['patch_sha256']
policy_checks = {}
for captured in sorted((PACKET / 'native-policy').rglob('*')):
    if not captured.is_file():
        continue
    relative = captured.relative_to(PACKET / 'native-policy').as_posix()
    if relative in ['score.gitlint', 'gitlint-source.json', 'shared-common-on-pr.yml', 'shared-common-source.json']:
        continue
    baseline_bytes = subprocess.check_output(['git', 'show', location['baseline'] + ':' + relative], cwd=native)
    captured_hash = sha(captured)
    baseline_hash = hashlib.sha256(baseline_bytes).hexdigest()
    candidate_hash = sha(native / relative)
    assert captured_hash == baseline_hash == candidate_hash, relative
    policy_checks[relative] = {'baseline_sha256': baseline_hash, 'captured_sha256': captured_hash,
                              'candidate_sha256': candidate_hash, 'unchanged': True}
write(PACKET / 'policy-invariance.json', {'baseline': location['baseline'], 'files': policy_checks,
                                        'scope': 'Captured native policy bytes equal Git baseline and current candidate; external SCORE Gitlint and shared-common workflow provenance recorded separately'})
pattern = 'mw_com_config|test_lmcontrol_mw_com_config|control_provider_test_mw_com_config'
inventory_paths = ['--', ':(glob)**/*.bzl', ':(glob)**/BUILD', ':(glob)**/BUILD.bazel']
inventory_commands = [['git', 'grep', '-n', '-E', pattern, location['baseline'], *inventory_paths],
                      ['git', 'grep', '-n', '-E', pattern, *inventory_paths]]
inventory = [subprocess.check_output(command, cwd=native, text=True).splitlines()
             for command in inventory_commands]
for required in ['score/launch_manager/src/daemon/src/control/BUILD',
                 'score/launch_manager/src/lm_control/BUILD', 'tests/utils/environments/BUILD',
                 'tests/utils/bazel/integration.bzl']:
    assert any(required + ':' in line for line in inventory[0]), required
    assert any(required + ':' in line for line in inventory[1]), required
write(PACKET / 'consumer-inventory.json', {'baseline': location['baseline'],
      'commands': inventory_commands, 'baseline_references': inventory[0], 'candidate_references': inventory[1],
      'scope': 'Tracked native repository references, including intent-to-add candidate macro; generated outputs and external/dynamic consumers excluded'})
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
results.update({'buildifier_exit_code': 0, 'gitlint_exit_code': 0,
                'notice_only_change': False, 'notice_and_license_only_amendment': True,
                'pre_commit_scoped_exit_code': scoped_hooks['exit_code'],
                'pre_commit_exit_code': hooks['exit_code'], 'native_policy_unchanged': True,
                'scope': 'Current-head affected x86_64 Linux host tests, configuration/runfile/package comparisons and recorded contribution hooks; full native CI/QNX remain pending'})
write(PACKET / 'native-results.json', results)
hook_status = 'pass' if hooks['exit_code'] == 0 else 'have an unresolved failure'
body = (PACKET / 'native-policy/.github/PULL_REQUEST_TEMPLATE/improvement.md').read_text()
body = body.replace('[A short description of the improvement being addressed by the contribution.]',
'''Replace the three checked-in `mw_com_config.json` copies with generated outputs
from one shared `config/mw_com_config.bzl` definition and explicit `provider_test`,
`client_test` and `integration` profiles. Maintain `LmControlService` once while
preserving every original effective runtime value, output label, unit runfile
path and integration package filename.

The profiles intentionally differ in QM/ASIL-B, strict permission checks,
allowed providers, instance specifiers and consumer/provider settings. One
maintained definition source emits these distinct deployment documents; replacing
them with one identical runtime document would change those settings.

Include the macro's scoped Apache-2.0/CC0-1.0 AI disclosure and complete CC0 terms.
The macro body and BUILD edits retain the earlier implementation's exact bytes.
No C++/Rust API, runtime implementation, schema or dependency pin changes.''')
body = body.replace('> [!IMPORTANT]\n> Please replace `[ISSUE-NUMBER]` with the issue-number that tracks this bug fix. If there is no such\n> ticket yet, create one via [this issue template](../ISSUE_TEMPLATE/new?template=improvement.md).\n\ncloses [ISSUE-NUMBER] (improvement ticket)', 'Closes #704 (improvement ticket)')
body += f'''\n## Validation

Fresh checks on `{results['baseline']}`, Bazel 8.7.0, x86_64 Linux host mode:

- 125 cases across five targets pass, with zero failures, errors or skips:
  provider 3; client 2; control implementation 36; configuration mapping 83;
  switch-run-target integration 1. Tests execute with cache results disabled
  and network-isolated sandboxes.
- All three generated JSON objects equal their original Git documents,
  including every field and list order.
- Both unit runfile payloads retain their paths and parsed values.
- The integration tar retains `tests/switch_run_target/etc/mw_com_config.json`
  and its original parsed content.
- Buildifier format/lint and the native S-CORE Gitlint configuration pass.
- Native pre-commit `--all-files` hooks {hook_status}; raw commands and results are retained.

Patch SHA-256: `{results['patch_sha256']}`.
Full native CI, ARM64, sanitizer/coverage/docs campaigns and the licensed QNX
matrix remain pending. Local affected checks do not replace those PR jobs.

## Impact and review

No intended runtime requirement/design change: retain existing native IDs and
statuses, subject to authorized impact review. Acceptance mapping, captured
policy, exact source/configuration/XML evidence, a content-review request and
the current merge checklist accompany the local contribution packet. Human
review of this exact revision and actual author DCO remain pending.

## AI assistance

The generator and BUILD edits were produced with DeepSeek V4 Flash through Fabro
(recorded historical model label). OpenAI Codex prepared the licence/disclosure
amendment, current-head verification and submission artifacts. Copied profile
data retains Apache-2.0; generated portions are offered under CC0-1.0. AI tools
are credited as assistance and are not human coauthors.
'''
(PACKET / 'PR-body.md').write_text(body)
(PACKET / 'README.md').write_text(f'''# Lifecycle #704 — current project contribution packet

The scoped configuration cleanup is implemented and verified on current captured
upstream `{results['baseline']}`: **125 cases pass**, with zero failures, errors
or skips. All three effective JSON profiles, both unit runfiles and the integration
package configuration are equal to their originals. Buildifier and Gitlint pass.
Native pre-commit `--all-files` hooks {hook_status}; see the complete retained result.

The three JSON source files are removed and one central generator maintains the
shared service definition. Distinct deployment profiles preserve intentional
safety/permission differences. The [acceptance and impact assessment](acceptance-and-impact.md)
states this interpretation of issue #704's “single instance” requirement explicitly.

| Artifact | Location |
| --- | --- |
| Exact native patch, complete licence terms and retained source | [submission.patch](submission.patch), candidate-source/ and baseline-source/ |
| Improvement-template PR, title and commit message | [PR-body.md](PR-body.md), [pr-title.txt](pr-title.txt), [commit-message.txt](commit-message.txt) |
| Acceptance and native impact mapping | [acceptance-and-impact.md](acceptance-and-impact.md) |
| Exact-candidate engineering assessment | [review.md](review.md) |
| Current verification and reproducible measurements | [native-results.json](native-results.json), test XML/raw logs under logs/ |
| Project workflow denominator and merge artifacts | [ci-obligations.md](ci-obligations.md), [merge-checklist.md](merge-checklist.md) |
| Content review request and designated reviewers | [content-review-request.md](content-review-request.md), captured CODEOWNERS |
| Author certification and current account observation | [DCO.md](DCO.md), [DCO-status.json](DCO-status.json), [eca-current-observation.json](eca-current-observation.json) |
| Exact subject, issue and publication state | [submission-record.json](submission-record.json) |

Patch SHA-256: `{results['patch_sha256']}`. The native macro body/BUILD files are
unchanged from the earlier implementation; complete CC0 terms are added. Original
113-case baseline evidence and the interrupted first formatter remain preserved
in the parent packet and its history archive. This packet does not rebind their
results to the newer source.

**The contribution is not yet merge-ready.** Author DCO, actual submitted-head
Eclipse/CI checks, authorized impact/content review and committer acceptance are
pending. These require real people/receipts and cannot be replaced with generated
documents. No PR or review request has been published.

Offline verification:

```bash
python3 contributions/remediation/lifecycle-704/project-completion/verify_packet.py
```

The manifest excludes itself, verification.json and Python caches. Verification
checks retained hashes and clean patch application; it performs no native build
and grants no human acceptance.

Assisted-by: OpenAI Codex (model revision unavailable)
''')
gates = ['Author personal DCO confirmation and truthful native sign-off',
         'Actual submitted-head Eclipse eligibility and complete native CI/platform results or approved dispositions',
         'Authorized content/impact review, issue-owner acceptance and committer merge decision']
if hooks['exit_code']:
    gates.append('Unresolved native pre-commit failure; see recorded result')
status = {'id': 'eclipse-score/lifecycle#704', 'observed_at': now,
          'ready_for_official_merge': False, 'remaining_gates': gates,
          'human_review': 'Advisory assessment prepared; authorized current-head review pending',
          'ai_assistance': ['DeepSeek V4 Flash (Fabro; recorded model label)', 'OpenAI Codex (preparation and verification; model revision unavailable)'],
          'artifacts': {key: REL + value for key, value in {
              'patch': 'submission.patch', 'pr_body': 'PR-body.md', 'pr_title': 'pr-title.txt',
              'commit_message_guidance': 'commit-message.txt', 'native_results': 'native-results.json',
              'acceptance_and_impact': 'acceptance-and-impact.md', 'ci_matrix': 'ci-obligations.md',
              'engineering_review': 'review.md',
              'human_disposition': 'merge-checklist.md', 'content_review_request': 'content-review-request.md',
              'dco_status': 'DCO-status.json', 'submission_record': 'submission-record.json',
              'evidence_manifest': 'artifact-manifest.json'}.items()},
          'patch_provenance': {'original_path': 'issues/eclipse-score/lifecycle/704/imported/fabro/evidence/lifecycle-704-upstream-packet/lifecycle-704.patch',
              'original_sha256': 'c8a33936900b24c13b46298e929d4ef483d0e128d44f9a2cce97909f55702f01',
              'prepared_sha256': results['patch_sha256'], 'source_diff_unchanged': False,
              'note': 'Macro licence/disclosure comments and complete CC0 distribution terms only; executable macro/BUILD bytes preserved. Current-head affected checks rerun.'}}
write(PACKET / 'status.json', status)
for file in PACKET.glob('*.md'):
    (PACKET / (file.name + '.license')).write_text('SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation\nSPDX-License-Identifier: Apache-2.0 AND CC0-1.0\nAI Disclosure: Prepared with OpenAI Codex; AI portions offered under CC0-1.0. Human review pending.\n')
files = {f.relative_to(PACKET).as_posix(): sha(f) for f in sorted(PACKET.rglob('*'))
         if f.is_file() and '__pycache__' not in f.parts and f.name not in ['artifact-manifest.json', 'verification.json']}
write(PACKET / 'artifact-manifest.json', {'algorithm': 'sha256', 'captured_at': now, 'files': files})
registry_path = PROJECT / 'contributions/registry.json'
registry = load(registry_path)
issue = next(x for x in registry['issues'] if x['id'] == status['id'])
issue['compliance_status'] = REL + 'status.json'
issue['prepared_pr_draft'] = REL + 'PR-body.md'
issue['engineering_review'] = 'current_head_artifact_and_impact_assessment_prepared_author_and_native_acceptance_pending'
issue['current_preparation'] = {'record': REL + 'README.md', 'native_results': REL + 'native-results.json',
                              'baseline': results['baseline'], 'patch_sha256': results['patch_sha256'],
                              'native_pr_created': False, 'dco': 'Author confirmation pending'}
write(registry_path, registry)
readme = PROJECT / 'contributions/README.md'
text = readme.read_text()
old = 'Lifecycle #704 now has a [fresh notice-adjusted verification and review packet](remediation/lifecycle-704/README.md): 113 affected native cases pass, all profile/runfile/package comparisons pass, and Buildifier passes. Actual human review, author DCO confirmation and remaining native CI/platform/impact dispositions remain pending.'
new = 'Lifecycle #704 has a [current-head project contribution packet](remediation/lifecycle-704/project-completion/README.md): 125 affected native cases pass, profile/runfile/package comparisons pass, and Buildifier/Gitlint pass. The native hook result, acceptance/impact mapping, PR draft, content-review request, DCO draft and complete project merge checklist are retained. Author certification, actual native CI and authorized review/acceptance remain pending.'
assert old in text or new in text, 'Expected Lifecycle entry'
readme.write_text(text.replace(old, new))
print(json.dumps({'packet_files_sealed': len(files), 'native_cases_passed': 125, 'remaining_gates': gates}))
