# Improvement

> [!IMPORTANT]
> Use this template only for improvement that do not influence topics covered by contribution requests or bug fixes.

> [!CAUTION]
> Make sure to submit your pull-request as **Draft** until you are ready to have it reviewed by the Committers.

## Description

Replace the three checked-in `mw_com_config.json` copies with generated outputs
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
No C++/Rust API, runtime implementation, schema or dependency pin changes.

## Related ticket

Closes #704 (improvement ticket)

## Validation

Fresh checks on `f603fe7327b642574332df02a66dd420bd133aea`, Bazel 8.7.0, x86_64 Linux host mode:

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
- Native pre-commit `--all-files` hooks pass; raw commands and results are retained.

Patch SHA-256: `3cc9ced41cd32678d8e0cdd433881aaf7a8bc0329b2d3153e940cb51a80e4626`.
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
