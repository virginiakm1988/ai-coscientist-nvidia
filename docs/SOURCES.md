# Sources and licensing

- [Original EOP teaching project](https://github.com/virginiakm1988/EOP_agent_tutorial)
- [NeMo Fabric](https://github.com/NVIDIA/NeMo-Fabric)
- [NeMo Relay](https://github.com/NVIDIA/NeMo-Relay)
- [NeMo Helix](https://github.com/NVIDIA-NeMo/nemo-helix)

## Version pins checked for this implementation

- NeMo Fabric: Python distributions `nemo-fabric==0.6.1`, `nemo-fabric-adapters-common==0.6.1`. Adapter contract cross-checked against public commit `910218f0891749c9364e814596e452f7258e23bb` and tested against the installed release.
- NeMo Relay: `nemo-relay==0.11.1`; actual scoped tool/LLM instrumentation, local ATOF sink.
- NeMo Data Designer: `data-designer==0.10.0`; structured LLM column, seeded dataframe, explicit run configuration.
- NeMo Helix: source commit `6386f9f0a84e8c4b71c4852fec9d7fae1aaf6b11`, package `packages/nhx_evals_sdk`. No full service platform is required for captured-trial scoring.
- NeMo AutoModel: `nemo-automodel==0.7.0`; recipe/API compared against official public source `c57935fc64faea913ce9f5e38ea7e57e6416cc93` and the v0.7 documentation.
- Omni-FinAI 70B revision: `8f9e1ccba75181c7ca95df77e8313a76bfdd4a50`.
- Small Llama 3.2 1B revision: `4e20de362430cd3b72f300e6b0f18e50e7166e08`.

Only the SDKs applicable to this repository are installed. Hosted NIM model IDs are recorded with each run; their server implementation is provider-managed and cannot be frozen by a client package lock. These tutorials are independent companion implementations. NVIDIA SDKs and related public code retain their own Apache-2.0 notices. Llama-derived checkpoints retain their model licenses and use policies. No external weights or paper text are redistributed here.

## Method map

The deterministic tool calculates the difference in accuracy in percentage points from integer correct/total counts. It verifies the test-set identity and required citation IDs. The model cannot change the checked verdict or citation list. Four cases cover a supported comparison, missing evidence, wrong citations, and a wrong numerical claim. Input text never becomes executable Python or a shell command.

This is a companion implementation of evidence-oriented programming concepts. The authored experiment records are illustrative, not published scientific results or an autonomous-discovery benchmark. No unidentified paper is claimed to be reproduced.

The overview diagram is newly authored in NVIDIA-inspired green, black, and neutral colors; it is not an official NVIDIA architecture figure or endorsement.
