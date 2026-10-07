# Lifecycle #704 — complete code-header audit

Native PR: [#762](https://github.com/eclipse-score/lifecycle/pull/762), source head
`0f63daeb489ad107f41143303f19fb9484c58392`. It remains Draft until the author's ready-for-review instruction.

Checked **485 nonempty tracked native code files**, including all **four code
files changed by the PR**, and **24 code files added on the evidence branch**.
The local publication verifier is checked too. Every current nonempty code file
in these scopes has copyright, NOTICE ownership reference, readable Apache terms,
license URL and an appropriate SPDX expression. The AI-generated helpers and
macro also retain CC0 disclosure and assistance attribution.

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
