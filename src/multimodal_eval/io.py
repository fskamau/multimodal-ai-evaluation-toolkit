from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Mapping, Any


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(data: Any, path: str | Path, indent: int = 2) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8")
    return output


def save_evaluations_csv(
    rows: Iterable[Mapping[str, Any]], path: str | Path
) -> Path:
    rows = list(rows)
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        output.write_text("", encoding="utf-8")
        return output

    flattened = []
    for row in rows:
        item = {
            "evaluation_id": row.get("evaluation_id"),
            "task_type": row.get("task_type"),
            "verdict": row.get("verdict"),
            "overall_score": row.get("overall_score"),
            "error_count": len(row.get("errors", [])),
        }
        for name, value in row.get("scores", {}).items():
            item[f"score_{name}"] = value
        flattened.append(item)

    fieldnames = sorted({key for item in flattened for key in item})
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened)

    return output
