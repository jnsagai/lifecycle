# Lifecycle #704 — current project contribution packet

The scoped configuration cleanup is implemented and verified on current captured
upstream `f603fe7327b642574332df02a66dd420bd133aea`: **125 cases pass**, with zero failures, errors
or skips. All three effective JSON profiles, both unit runfiles and the integration
package configuration are equal to their originals. Buildifier and Gitlint pass.
Native pre-commit `--all-files` hooks pass; see the complete retained result.

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

Patch SHA-256: `3cc9ced41cd32678d8e0cdd433881aaf7a8bc0329b2d3153e940cb51a80e4626`. The native macro body/BUILD files are
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
