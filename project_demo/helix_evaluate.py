"""Rescore captured Fabric trials with the real, pinned NeMo Helix SDK.

No new model calls are made. This adapter preserves each source run's execution
mode and evaluates explicit structured checks, not the mere presence of words.
"""

import argparse
import asyncio
import json
from pathlib import Path


def extract_cases(record):
    payload = record["result"]
    if "output" in payload:
        payload = payload["output"]
    return payload.get("scenarios", payload.get("examples", []))


def checks(row):
    if "check" in row:
        return {
            "decision_correct": row["check"]["status"] == row["expected_status"],
            "report_matches_check": row["answer"]["status"] == row["check"]["status"],
        }
    return {
        "answerability_correct": (not row["answer"]["abstain"]) == row["answerable"],
        "all_required_sources_retrieved": set(row["relevant_ids"])
        <= set(row["retrieved_ids"]),
    }


async def evaluate(source, output_dir):
    from nhx_evals_sdk.agent_eval.evaluator import AgentEvaluator
    from nhx_evals_sdk.agent_eval.tasks import AgentEvalRunConfig, AgentEvalTask
    from nhx_evals_sdk.agent_eval.trials import (
        AgentEvalTrial,
        AgentEvalTrialStatus,
        AgentOutput,
    )
    from nhx_evals_sdk.metrics.protocol import (
        MetricOutput,
        MetricOutputSpec,
        MetricResult,
    )

    class StructuredChecks:
        type = "project_structured_checks"

        def __init__(self, names):
            self.names = names

        def output_spec(self):
            return [MetricOutputSpec.boolean(name) for name in self.names]

        async def compute_scores(self, input):
            values = checks(json.loads(input.candidate.output_text))
            return MetricResult(
                outputs=[
                    MetricOutput(name=name, value=values[name]) for name in self.names
                ]
            )

    record = json.loads(Path(source).read_text(encoding="utf-8"))
    if record["status"] != "succeeded":
        raise ValueError("A failed source run cannot be rescored as a successful trial")
    rows = extract_cases(record)
    if not rows:
        raise ValueError("Source has no project scenarios")
    tasks = []
    trials = []
    for row in rows:
        tasks.append(
            AgentEvalTask(
                id=row["id"],
                intent="Evaluate recorded project checks",
                inputs={},
                metrics=[StructuredChecks(list(checks(row)))],
            )
        )
        trials.append(
            AgentEvalTrial(
                id=row["id"] + ":captured",
                task_id=row["id"],
                status=AgentEvalTrialStatus.COMPLETED,
                output=AgentOutput(
                    output_text=json.dumps(row, ensure_ascii=True),
                    metadata={
                        "source_mode": record["mode"],
                        "source_result": str(Path(source).resolve()),
                    },
                ),
                metadata={"generated": False, "rescored_existing_output": True},
            )
        )
    result = await AgentEvaluator().run(
        tasks=tasks,
        trials=trials,
        config=AgentEvalRunConfig(
            work_dir=Path(output_dir),
            parallelism=1,
            labels={
                "source_mode": record["mode"],
                "project": record["config"]["project"],
            },
        ),
    )
    result.persist(write_dashboard=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True)
    parser.add_argument("--output-dir", default="runs/helix")
    args = parser.parse_args()
    asyncio.run(evaluate(args.results, args.output_dir))
    print("Helix scoring complete; inspect the persisted scores and dashboard.")


if __name__ == "__main__":
    main()
