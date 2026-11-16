"""One explicit CLI mode; live failures never fall back to fixture answers."""

import argparse
import asyncio
import json
from pathlib import Path
from .common import (
    evaluation_source,
    digest,
    Run,
    load_config,
    read_json,
    data_path,
    write_json,
    sdk_versions,
)
from .workflow import pipeline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=["prepare", "demo", "evaluate", "sdk-check", "generate-qa"]
    )
    parser.add_argument("--config", default="configs/default.json")
    parser.add_argument("--mode", choices=["fixture", "live"], default="fixture")
    parser.add_argument("--engine", choices=["python", "fabric"], default=None)
    parser.add_argument(
        "--case", help="Select one scenario ID; default runs every case"
    )
    parser.add_argument("--output-dir", default="runs/demo")
    parser.add_argument(
        "--results", help="Previously saved result.json to rescore without a model call"
    )
    args = parser.parse_args()
    if args.command == "evaluate" and not args.results:
        parser.error("evaluate requires --results; it never calls a model")
    config = load_config(args.config)
    effective_mode = "fixture" if args.command == "sdk-check" else args.mode
    run = Run(args.output_dir, config, effective_mode, args.command)
    try:
        data = (
            None if args.command == "evaluate" else read_json(data_path(config, "data"))
        )
        if args.case and data is not None:
            cases = data["queries"] if isinstance(data, dict) else data
            selected = [row for row in cases if row["id"] == args.case]
            if not selected:
                raise ValueError("Unknown case ID")
            if isinstance(data, dict):
                data["queries"] = selected
            else:
                data = selected
        if args.command == "prepare":
            if config["project"] == "egyptian-rag":
                from .workflow import validate_corpus

                validate_corpus(data["corpus"], data["queries"])
            result = {
                "data_sha256": __import__(
                    "project_demo.common", fromlist=["digest"]
                ).digest(data),
                "data": data,
                "model_called": False,
            }
        elif args.command == "generate-qa":
            if config["project"] != "egyptian-rag":
                raise ValueError("generate-qa is available only in the RAG repo")
            from .generate_qa import generate

            result = generate(config, data["corpus"], run.path, args.mode)
        elif args.command == "evaluate" and args.results:
            saved, provenance = evaluation_source(args.results)
            run.record.update(
                mode=saved["mode"],
                config=saved["config"],
                config_sha256=digest(saved["config"]),
            )
            payload = saved["result"]
            if "output" in payload:
                payload = payload["output"]
            from .workflow import evaluate

            result = {
                "metrics": evaluate(
                    payload.get("scenarios", payload.get("examples", []))
                ),
                **provenance,
            }
        else:
            engine = args.engine or (
                "fabric"
                if args.mode == "live" or args.command == "sdk-check"
                else "python"
            )
            mode = "fixture" if args.command == "sdk-check" else args.mode
            if engine == "fabric":
                from .fabric_consumer import run as execute

                result = asyncio.run(
                    execute(config, mode, data, run.path / "sdk", relay=True)
                )
            else:
                result = asyncio.run(
                    pipeline(config, mode, data, run.path / "nim", relay=False)
                )
            result["sdk_versions"] = sdk_versions()
        record = run.finish(result)
        print(
            json.dumps(
                {
                    "status": record["status"],
                    "result_file": str(run.path / "result.json"),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception as error:
        run.fail(error)
        print(
            json.dumps(
                {
                    "status": "failed",
                    "error": run.record["error"],
                    "result_file": str(run.path / "result.json"),
                },
                ensure_ascii=False,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
