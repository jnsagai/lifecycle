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

"""Offline integrity and clean-application check; no native build or acceptance."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

PACKET = Path(__file__).resolve().parent
manifest = json.loads((PACKET / 'artifact-manifest.json').read_text())
for relative, expected in manifest['files'].items():
    path = (PACKET / relative).resolve()
    assert path.is_relative_to(PACKET), relative
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative
changes = json.loads((PACKET / 'notice-equivalence.json').read_text())
original_patch = PACKET / 'historical-reference/original.patch'
assert hashlib.sha256(original_patch.read_bytes()).hexdigest() == 'c8a33936900b24c13b46298e929d4ef483d0e128d44f9a2cce97909f55702f01'
with tempfile.TemporaryDirectory(prefix='lifecycle704-original-offline-') as directory:
    original = Path(directory)
    shutil.copytree(PACKET / 'baseline-source', original, dirs_exist_ok=True)
    subprocess.run(['git', 'apply', '--whitespace=error-all', str(original_patch)],
                   cwd=original, check=True, capture_output=True)
    old_macro = (original / 'config/mw_com_config.bzl').read_bytes()
    new_macro = (PACKET / 'candidate-source/config/mw_com_config.bzl').read_bytes()
    assert hashlib.sha256(old_macro).hexdigest() == changes['old_macro_sha256']
    marker = b'"""Generated mw_com_config.json artifacts'
    assert old_macro[old_macro.index(marker):] == new_macro[new_macro.index(marker):]
    for relative in changes['candidate_sources']:
        if relative.endswith('/BUILD'):
            assert (original / relative).read_bytes() == (PACKET / 'candidate-source' / relative).read_bytes(), relative
    for relative in changes['deleted_paths']:
        assert not (original / relative).exists(), relative
with tempfile.TemporaryDirectory(prefix='lifecycle704-offline-') as directory:
    checkout = Path(directory)
    shutil.copytree(PACKET / 'baseline-source', checkout, dirs_exist_ok=True)
    for args in [['--check', '--whitespace=error-all'], ['--whitespace=error-all']]:
        subprocess.run(['git', 'apply', *args, str(PACKET / 'submission.patch')],
                       cwd=checkout, check=True, capture_output=True)
    for path, expected in changes['candidate_sources'].items():
        assert hashlib.sha256((checkout / path).read_bytes()).hexdigest() == expected, path
    for path in changes['deleted_paths']:
        assert not (checkout / path).exists(), path
results = json.loads((PACKET / 'native-results.json').read_text())
assert results['patch_sha256'] == hashlib.sha256((PACKET / 'submission.patch').read_bytes()).hexdigest()
print(json.dumps({'packet_files_verified': len(manifest['files']),
                  'candidate_files_verified': len(changes['candidate_sources']),
                  'deleted_paths_verified': len(changes['deleted_paths']),
                  'clean_application': True,
                  'original_implementation_body_preserved': True,
                  'scope': 'Retained bytes and clean patch application; no native execution or human acceptance'}))
