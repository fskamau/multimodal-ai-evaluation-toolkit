from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Mapping, Sequence

from .scoring import normalize_scores, weighted_score
from .validators import (
    require_non_empty_string,
    validate_dimensions,
    validate_errors,
    validate_task_type,
)


@dataclass(slots=True)
class EvaluationError:
    type: str
    severity: str = "MEDIUM"
    description: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(slots=True)
class EvaluationResult:
    evaluation_id: str
    task_type: str
    prompt: str
    response: str
    scores: dict[str, float]
    errors: list[EvaluationError] = field(default_factory=list)
    verdict: str = "PASS"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def overall_score(self) -> float:
        return weighted_score(self.scores)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["overall_score"] = self.overall_score
        return data


def _derive_verdict(score: float, error_count: int) -> str:
    if score < 2.5:
        return "FAIL"
    if error_count or score < 4.0:
        return "PASS_WITH_ISSUES"
    return "PASS"


def evaluate_response(
    *,
    evaluation_id: str,
    task_type: str,
    prompt: str,
    response: str,
    scores: Mapping[str, float],
    errors: Sequence[Mapping[str, str]] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> EvaluationResult:
    evaluation_id = require_non_empty_string(evaluation_id, "evaluation_id")
    task_type = validate_task_type(task_type)
    prompt = require_non_empty_string(prompt, "prompt")
    response = require_non_empty_string(response, "response")
    validate_dimensions(scores)
    validate_errors(errors)

    normalized = normalize_scores(scores)
    parsed_errors = [
        EvaluationError(
            type=str(item["type"]),
            severity=str(item.get("severity", "MEDIUM")),
            description=str(item.get("description", "")),
        )
        for item in (errors or [])
    ]

    overall = weighted_score(normalized)
    verdict = _derive_verdict(overall, len(parsed_errors))

    return EvaluationResult(
        evaluation_id=evaluation_id,
        task_type=task_type,
        prompt=prompt,
        response=response,
        scores=normalized,
        errors=parsed_errors,
        verdict=verdict,
        metadata=dict(metadata or {}),
    )
