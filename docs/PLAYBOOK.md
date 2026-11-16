# Demonstration playbook

## Intended result

Check research claims against executable numerical evidence, preserve the evidence chain, and use NVIDIA NIM to explain the checked result. NeMo Fabric controls the custom agent lifecycle and NeMo Relay records tool/model activity.

## 1. Prepare a reproducible session

Create an isolated environment, install the indicated extras, and record the Git commit with `git rev-parse HEAD`. Keep `configs/default.json` with the run. Inspect the source licenses before adding external data. The program saves a configuration SHA-256, mode, elapsed time, individual predictions, aggregate metrics, and failures. Use environment variables or Colab Secrets for credentials.

## 2. Inspect and test the core method

Run `prepare`, inspect the authored inputs, then run `demo --mode fixture`. Run `python -m unittest discover -s tests -v`. These tests check invalid evidence, missing citations, scoring boundaries, data separation, or malformed retrieval output as appropriate; they do not establish model quality.

The deterministic tool calculates the difference in accuracy in percentage points from integer correct/total counts. It verifies the test-set identity and required citation IDs. The model cannot change the checked verdict or citation list. Four cases cover a supported comparison, missing evidence, wrong citations, and a wrong numerical claim. Input text never becomes executable Python or a shell command.

## 3. Run the live demonstration

Install `.[agents]`. Run `sdk-check` to validate the real Fabric/Relay lifecycle without spending model requests. Configure current NIM model IDs and `NVIDIA_API_KEY`, then run:

```bash
python -m project_demo demo --mode live --engine fabric --output-dir runs/live
```

The default request cap is small and is shared between the workflow's NIM clients in one run. Attempts are reserved before network I/O, so failed HTTP requests consume the budget. A new invocation creates a new run and budget. No automatic fallback to fixture data or different models is permitted.

## 4. Review and evaluate

Inspect `result.json`, the request evidence, and local Relay event logs. Recompute metrics with `evaluate --results <result.json>`. For Helix, install the pinned source requirement on a compatible remote Python 3.12 environment and run `project_demo.helix_evaluate`. Its checks are structured decision and retrieval checks; they do not replace a human assessment of whether prose is scientifically justified.

## Acceptance and failure handling

Claim-decision accuracy is scored against the authored case labels. A complete citation chain does not prove experimental validity; the numerical experiment itself and the prose explanation still require human review.

A failure is part of the execution record. Resolve missing entitlement, invalid model ID, unsupported SDK release, malformed response, or insufficient GPU memory explicitly, then start a separate run. Do not edit old evidence to make it appear successful. The [validation file](../VALIDATION.json) is the source of truth for checks actually completed in this release.

## Method differences

This is a companion implementation of evidence-oriented programming concepts. The authored experiment records are illustrative, not published scientific results or an autonomous-discovery benchmark. No unidentified paper is claimed to be reproduced.
