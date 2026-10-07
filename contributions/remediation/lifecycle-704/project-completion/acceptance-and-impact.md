# Lifecycle #704 — acceptance and change impact

Issue: [#704](https://github.com/eclipse-score/lifecycle/issues/704).
Native baseline: `f603fe7327b642574332df02a66dd420bd133aea`.
The exact current diff is [submission.patch](submission.patch); its subject and
measurements are in [native-results.json](native-results.json).

| Issue requirement | Implementation and evidence |
| --- | --- |
| No/minimal duplication of `mw_com_config.json` | Delete all three checked-in configuration copies. Maintain the shared service-type definition once in `config/mw_com_config.bzl`; emit the three configurations from explicit profiles |
| One instance in an appropriate location | One central generator in the existing `config` package. Three output documents remain necessary because the original provider, client and integration values differ |
| Import everywhere needed | Update the two unit BUILD packages and integration environment BUILD package; preserve output filename labels. The unchanged shared integration packaging macro continues to consume its original environment label |
| Preserve effective behavior | Compare every field and list order of all three generated JSON objects against original Git documents. Also compare both unit runfile payloads and the integration tar member |
| Verify actual consumers | Execute both communication-dependent unit tests, the control implementation tests, configuration mapping tests and switch-run-target integration test on this baseline |

The literal phrase “single instance” is interpreted as one maintained source of
configuration definitions, with distinct generated deployments. A single identical
runtime document would change the baseline QM/ASIL-B and permission settings.
The PR description explains this interpretation for the issue owner to assess.
The change removes duplicated JSON source files; it does not claim that all
per-profile field literals inside the generator have been eliminated.

The native inventory contains three removed JSON source paths, three modified
BUILD files, the new macro and complete CC0-1.0 terms. Native C++/Rust implementations,
API declarations, schemas, dependency locks and toolchain configuration are unchanged.
The licence addition completes the distribution terms already declared in the
macro disclosure. No dependency is introduced: `write_file` comes from the
already-pinned `bazel_skylib` dependency.

The build graph changes source JSON inputs into generated JSON inputs. Generated
filenames, rootpath arguments, unit data dependencies, integration tar member,
logging export and integration visibility entries remain compatible. The consumer
inventory covers tracked references; external/dynamically formed paths remain a
receiving-project impact-review question. Build-time ordering and runfiles are
measured with actual Bazel artifacts rather than inferred from the macro.

No intended runtime requirement or architecture change is proposed. Existing
native configuration architecture context is retained at
`feat_arc_sta__lifecycle__cfg_params_static`, version 1, status valid, and
`doc__lifecycle_module_architecture`, version 1, status valid. The captured native
architecture distinguishes Launch Manager component/run-target configuration;
these IDs are context, not a claim that they directly specify every communication
deployment field or that this packet closes their safety obligations.

The proposed impact disposition is to retain native IDs/status/version and existing
design because generated runtime objects are equal. An authorized native reviewer
must accept that disposition and identify any additional required native work
products or export links. No agent-created approval, native safety closure or
qualification result is supplied. QNX and the complete native CI matrix require
their own results or receiving-project dispositions.

Assisted-by: OpenAI Codex (model revision unavailable)
