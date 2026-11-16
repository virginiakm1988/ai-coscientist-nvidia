"""Custom NeMo Fabric lifecycle, following NVIDIA's public adapter contract."""

import json
from pathlib import Path
from nemo_fabric_adapter_contract.models import (
    AgentConfig,
    AgentRunResult,
    AgentRunStatus,
    RuntimeContext,
)
from nemo_fabric_adapters.common import lifecycle
from .workflow import pipeline


class Runtime:
    def __init__(self):
        self.context = None

    async def start(self, payload):
        if self.context is not None:
            raise RuntimeError("Runtime already started")
        if not isinstance(payload.get("config"), AgentConfig):
            raise TypeError("Fabric must supply a validated AgentConfig")
        self.context = RuntimeContext.from_mapping(payload.get("runtime_context"))

    async def invoke(self, request, context):
        if self.context is None or context.runtime_id != self.context.runtime_id:
            raise RuntimeError("Runtime was not started or invocation ID differs")
        job = json.loads(request.input)
        # Only this installed workflow runs. No user shell, imports, or evaluation of source text.
        result = await pipeline(
            job["config"],
            job["mode"],
            job["data"],
            job["output_dir"],
            relay=job["relay"],
        )
        return AgentRunResult(status=AgentRunStatus.SUCCEEDED, output=result)

    async def stop(self):
        self.context = None


if __name__ == "__main__":
    lifecycle.serve(Runtime, config_loader=AgentConfig.from_mapping)
