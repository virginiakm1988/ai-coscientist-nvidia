# Independent code review

Reviewer: separate implementation agent (`build_reasoning_legal_repos`); not the author of this repository. Review date: 2026-11-16.

## Round 1 — correctness and research methods

Scope: source, CLI, configurations, dataset provenance, scoring, NVIDIA SDK boundaries, model/data split handling, notebooks and documentation. This is code review; GPU training is not validated merely by reviewing its recipe.

### AC-1 [P1] evaluate could run inference and mislabel source evidence

Without --results, evaluate fell through to demo. With --results, new run metadata used the requested/default mode instead of the source mode. Require a successful saved source and preserve its mode, config and digest without new model calls.

Status at first review: changes requested; owner notified.

### AC-2 [P1] Documented install extras did not install required SDKs

README/notebook used .[agent] but pyproject defined agents. Align install commands with actual extras and validate a clean setup.

Status at first review: changes requested; owner notified.

### AC-3 [P2] Interactive lesson exposed only execution mode

Add a case/claim input and allow saved-result selection so users can explore counterexamples and actual runs instead of only rerunning fixed scenarios.

Status at first review: changes requested; owner notified.

## Strengths verified in source

Real Fabric custom lifecycle and Relay instrumentation are present, rather than placeholder SDK imports. Fixture responses and conceptual-method scope are explicit. Model credentials are environment-based and local trace payload export is disabled by default. Helix code rescores captured trials rather than fabricating new agent execution.

## Round 2 — readability, reproducibility and regression verification

AC-1 is resolved: `evaluate` rejects a missing source before execution, requires a successful labeled source record, carries source mode/configuration into the new record, and records the source SHA-256 with `model_called=False`. No evaluation branch falls through to inference. AC-2 is resolved: installation instructions and notebooks now use the defined `agents` extra. AC-3 is resolved: the lesson has a scenario selector and the evaluation notebook accepts a saved result path.

The claim checker uses integer counts, verifies a common evaluation-set identity, rejects inconsistent citation IDs, computes percentage-point changes independently, and prevents NIM from changing the checked status/citation list. Public data are explicitly authored examples. Fabric lifecycle and Relay integration remain real SDK paths; fixture Python execution is labeled separately.

Independently reran the regression suite after fixes: **9 tests passed** using `python -m unittest discover -s tests -v`. Reviewed the formatted implementation, notebook mode controls, sources, licenses and failure paths.

**Review disposition:** reported code, scoring and teaching defects are resolved. Notebook bootstrap/publication and real GPU/model executions remain separately reported in the repository validation evidence; this review does not turn an unexecuted recipe or a model download into a successful inference/training result.
