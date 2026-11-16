"""Direct NeMo Relay instrumentation; no NAT dependency or remote trace exporter."""

from pathlib import Path
import json


async def instrumented(name, arguments, tool, model, output_dir, *, enabled, mode):
    if not enabled:
        checked = await tool(arguments)
        return checked, await model(checked)
    import nemo_relay as relay

    path = Path(output_dir).resolve()
    path.mkdir(parents=True, exist_ok=True)
    plugin_file = path / "relay-plugins.toml"
    plugin_file.write_text(
        'version = 1\n[[components]]\nkind = "observability"\nenabled = true\n'
        "[components.config]\nversion = 4\nenable_full_payloads = false\n"
        "[components.config.atof]\nenabled = true\n"
        '[[components.config.atof.sinks]]\ntype = "file"\noutput_directory = '
        + json.dumps(str(path / "relay"))
        + '\nfilename = "events.jsonl"\nmode = "append"\n',
        encoding="utf-8",
    )
    async with relay.plugin.activate({}, str(plugin_file)):
        try:
            with relay.scope.scope(name, relay.ScopeType.Agent) as handle:

                async def tool_call(args):
                    return relay.ToolExecutionResult(await tool(args))

                checked = (
                    await relay.tools.execute(
                        name + ".tools", arguments, tool_call, handle=handle
                    )
                ).result

                async def model_call(_request):
                    return await model(checked)

                output = await relay.llm.execute(
                    "nvidia-nim" if mode == "live" else "authored-fixture",
                    relay.LLMRequest(
                        {},
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": json.dumps(checked, ensure_ascii=False),
                                }
                            ]
                        },
                    ),
                    model_call,
                    handle=handle,
                )
        finally:
            await relay.subscribers.flush_async()
    return checked, output
