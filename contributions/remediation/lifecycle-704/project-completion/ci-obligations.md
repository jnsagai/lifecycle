# Lifecycle #704 — current native CI obligations

Source: the captured native workflows at
`f603fe7327b642574332df02a66dd420bd133aea`. Local execution below does not substitute
for the actual submitted PR's head-bound GitHub checks.

| Workflow/job | Expected scope | Current disposition |
| --- | --- | --- |
| `on-pr.yml` / common | Shared workflow: capability detection, all-files pre-commit, format/copyright targets when present, module tidy and frozen lockfile checks, frozen uv/pytest when both Python inputs exist | Actual PR result pending; scoped contribution hooks recorded locally |
| build / x86_64-linux | Build `//examples/... //score/...`; test `//...` | Five affected targets freshly pass, 125 cases. Full default Docker-mode matrix pending |
| build / arm64-linux | Build examples and score | Not run locally; required native CI result/disposition pending |
| build / asan_ubsan_lsan | Native x86_64 sanitizer test matrix | Not run locally; required native CI result/disposition pending |
| build / tsan | Native x86_64 thread-sanitizer test matrix | Not run locally; required native CI result/disposition pending |
| Clippy | Rust 1.90.0, all features/targets/workspace, warnings denied | No Rust changes; actual native job result pending |
| coverage | Native unified coverage workflow and threshold | Actual native job result pending; no new coverage percentage claimed |
| docs-check | Native docs verification target | Actual native job result pending; no docs source changes in the patch |
| docs-build | Native docs build, after build jobs | Actual native job result pending |
| Gitlint | Gitlint 0.19.1 with S-CORE configuration | Prepared commit message passes locally; submitted commit check still required |
| Ready to merge | Depends on common, build, docs-check, docs-build, Clippy, coverage and Gitlint | Cannot pass until native jobs run on the actual PR head |
| `on-pr-target.yml` / QNX | `unit-tests-x86_64-qnx`, `unit-tests-arm64-qnx`, `x86_64-qnx`, `arm64-qnx` | Native license/user/password secrets and runner/QEMU environment not supplied here; actual job results pending |
| Eclipse eligibility and author DCO | Account/commit eligibility and genuine human sign-off | Current declared-account lookup succeeds; actual PR eligibility and author DCO remain pending |
| CODEOWNERS/content review | Human review and committer responsibility | Reviewer/request artifacts prepared; no approval receipt supplied |

The unchanged dependency graph warns that `score_tooling` resolves 2.2.1 to 2.2.2;
the original lock and module are preserved. The patch introduces no dependency,
toolchain, warning suppression or native check-policy change. Resource caps and
the exact LLVM archive cache used for local execution are recorded separately.

The shared common workflow's native tag `on-pr/v0.0.0` is resolved to its exact
commit in `native-policy/shared-common-source.json`; its source is retained as
`native-policy/shared-common-on-pr.yml`. Capability-dependent checks and the
disabled module-name check are distinguished from unconditional steps. Actual
GitHub branch-protection settings were not inferred from this workflow inventory.

Assisted-by: OpenAI Codex (model revision unavailable)
