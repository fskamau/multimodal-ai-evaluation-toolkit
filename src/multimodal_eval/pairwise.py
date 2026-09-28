from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Mapping

from .scoring import normalize_scores, weighted_score
from .validators import require_non_empty_string


@dataclass(slots=True)
class PairwiseResult:
    evaluation_id: str
    response_a: str
    response_b: str
    scores_a: dict[str, float]
    scores_b: dict[str, float]
    preferred_response: str
    preference_strength: str
    dimension_winners: dict[str, str] = field(default_factory=dict)
    justification: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["overall_a"] = weighted_score(self.scores_a)
        data["overall_b"] = weighted_score(self.scores_b)
        return data


def _winner(a: float, b: float, tolerance: float = 0.15) -> str:
    if abs(a - b) <= tolerance:
        return "TIE"
    return "A" if a > b else "B"


def _strength(delta: float) -> str:
    if delta < 0.20:
        return "SLIGHT"
    if delta < 0.75:
        return "MODERATE"
    return "STRONG"


def compare_responses(
    *,
    evaluation_id: str,
    response_a: str,
    response_b: str,
    scores_a: Mapping[str, float],
    scores_b: Mapping[str, float],
    justification: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> PairwiseResult:
    evaluation_id = require_non_empty_string(evaluation_id, "evaluation_id")
    response_a = require_non_empty_string(response_a, "response_a")
    response_b = require_non_empty_string(response_b, "response_b")

    a = normalize_scores(scores_a)
    b = normalize_scores(scores_b)

    shared = sorted(set(a) & set(b))
    if not shared:
        raise ValueError("scores_a and scores_b must share at least one dimension.")

    dimension_winners = {dim: _winner(a[dim], b[dim]) for dim in shared}
    overall_a = weighted_score(a)
    overall_b = weighted_score(b)

    preferred = _winner(overall_a, overall_b)
    strength = "TIE" if preferred == "TIE" else _strength(abs(overall_a - overall_b))

    return PairwiseResult(
        evaluation_id=evaluation_id,
        response_a=response_a,
        response_b=response_b,
        scores_a=a,
        scores_b=b,
        preferred_response=preferred,
        preference_strength=strength,
        dimension_winners=dimension_winners,
        justification=justification.strip(),
        metadata=dict(metadata or {}),
    )
