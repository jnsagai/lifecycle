# Lifecycle #704 — contribution headers and upstream audit

Native PR: [#762](https://github.com/eclipse-score/lifecycle/pull/762), source head
`0f63daeb489ad107f41143303f19fb9484c58392`. It remains Draft until the author's ready-for-review instruction.

All **four code files changed by PR #762** have complete project headers. All
**24 code files added on the evidence branch** and the local publication verifier
also have the required fields after the helper corrections. These scopes have
copyright, NOTICE ownership reference, readable Apache terms, license URL and
an appropriate SPDX expression. AI-generated helpers and the macro retain CC0
disclosure and assistance attribution.

The broader upstream audit checked **485 nonempty files in the default source
set**, plus **25 additional source/build configuration files**, including CodeQL,
FlatBuffers, Docker, Bazel configuration, TOML and the extensionless shell tool.
It found **seven inherited source files and nine inherited configuration files
without headers** (listed individually in `header-audit.json`). Those paths are
unchanged by PR #762. This audit does not certify all upstream code as compliant.
The initial evidence revision's broad wording is superseded by this inventory.
The author's scope question is pending; default preparation retains the issue
PR's scope and records these existing gaps separately.

The inherited empty `scripts/BUILD` has no content and is exempted by the native
checker. JSON measurements/configurations and verbatim licence terms are data;
source headers are not inserted into those formats.

Corrected five evidence helpers: completed the four Python notices and added the
missing shell-wrapper header. Completed the local publication verifier's notice.
Python ASTs are unchanged and the shell executable body is byte-identical.
The native PR implementation and all five retained candidate-source hashes are
unchanged. No new runtime verification is attributed to these comment-only
supporting-script changes; existing native results remain bound to the same source.

The [Eclipse handbook](https://www.eclipse.org/projects/handbook/) describes
copyright/NOTICE ownership, readable licence terms, SPDX expressions and AI
licence disclosures. The [pinned Lifecycle header checker](https://github.com/eclipse-score/tools/blob/7694bf823421b5542cd2f45239b8bdf205dbface/cr_checker/tool/cr_checker.py)
passes. Its Apache-only template reports a nonfatal format warning for the
correctly disclosed mixed Apache-2.0/CC0-1.0 macro. The combined SPDX expression
and required legal fields are verified independently; the warning and original
policy are retained without suppressions or a toolchain/checker modification.

[header-audit.json](header-audit.json) retains the file inventories, individual
hashes, legal-field checks and actual checker command/result.
[header-corrections.json](header-corrections.json) records before/after hashes,
body preservation and the prior sealed archive hashes. Original snapshots remain
available in the prior evidence commit and the local history archives.
[native-copyright-check.log](native-copyright-check.log) is the raw read-only result.

Author DCO, complete native CI and authorized acceptance retain their separate
statuses. This audit supplies no human approval or legal-agreement certification.

Assisted-by: OpenAI Codex (header correction and verification)
