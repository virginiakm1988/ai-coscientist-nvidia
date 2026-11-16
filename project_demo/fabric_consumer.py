"""Fabric execution; direct Python fixture mode remains available without SDKs."""

import json
import os
import sys
from pathlib import Path


def make_config(config):
    from nemo_fabric import (
        FabricConfig,
        DiscoveryConfig,
        HarnessConfig,
        MetadataConfig,
        RuntimeConfig,
    )

    return FabricConfig(
        metadata=MetadataConfig(name=config["project"]),
        discovery=DiscoveryConfig(local_paths=[Path(__file__).parent / "adapters"]),
        harness=HarnessConfig(
            adapter_id="virginia.demo." + config["project"], resolution="preinstalled"
        ),
        runtime=RuntimeConfig(input_schema="text", output_schema="message"),
    )


async def run(config, mode, data, output_dir, relay=True):
    from nemo_fabric import Fabric

    os.environ.setdefault("ADAPTER_PYTHON", sys.executable)
    os.environ.setdefault("PYTHONUTF8", "1")
    settings = make_config(config)
    result = await Fabric().run(
        settings,
        base_dir=Path.cwd(),
        input=json.dumps(
            {
                "config": config,
                "mode": mode,
                "data": data,
                "output_dir": str(Path(output_dir).resolve()),
                "relay": relay,
            },
            ensure_ascii=True,
        ),
    )
    mapping = result.to_mapping()
    if str(mapping.get("status", "")).lower() not in {"succeeded", "success"}:
        raise RuntimeError(
            "Fabric execution failed: " + json.dumps(mapping, ensure_ascii=True)
        )
    return mapping
