from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping, Any
from collections import Counter

from .scoring import weighted_score


def summarize_results(results: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(results)
    if not rows:
        return {"evaluations": 0, "average_score": 0.0, "verdicts": {}, "errors": {}}

    scores = []
    verdicts = Counter()
    errors = Counter()

    for row in rows:
        if "scores" in row and row["scores"]:
            scores.append(weighted_score(row["scores"]))
        verdicts[str(row.get("verdict", "UNKNOWN"))] += 1
        for error in row.get("errors", []):
            errors[str(error.get("type", "UNKNOWN"))] += 1

    avg = round(sum(scores) / len(scores), 3) if scores else 0.0
    return {
        "evaluations": len(rows),
        "average_score": avg,
        "verdicts": dict(verdicts),
        "errors": dict(errors),
    }


def generate_markdown_report(
    results: Iterable[Mapping[str, Any]],
    output_path: str | Path | None = None,
    title: str = "AI Evaluation Report",
) -> str:
    summary = summarize_results(results)

    lines = [
        f"# {title}",
        "",
        f"- Evaluations: **{summary['evaluations']}**",
        f"- Average weighted score: **{summary['average_score']:.2f}/5.00**",
        "",
        "## Verdict Distribution",
        "",
    ]

    if summary["verdicts"]:
        for verdict, count in sorted(summary["verdicts"].items()):
            lines.append(f"- {verdict}: {count}")
    else:
        lines.append("- No verdict data")

    lines += ["", "## Error Distribution", ""]

    if summary["errors"]:
        for error_type, count in sorted(
            summary["errors"].items(), key=lambda item: (-item[1], item[0])
        ):
            lines.append(f"- {error_type}: {count}")
    else:
        lines.append("- No errors recorded")

    report = "\n".join(lines) + "\n"

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")

    return report
