from __future__ import annotations

from typing import Mapping

DEFAULT_DIMENSIONS = (
    "factuality",
    "instruction_following",
    "completeness",
    "relevance",
    "grounding",
)

DEFAULT_WEIGHTS = {
    "factuality": 0.25,
    "instruction_following": 0.25,
    "completeness": 0.15,
    "relevance": 0.10,
    "grounding": 0.15,
    "visual_grounding": 0.10,
    "tool_use": 0.10,
}


def validate_score(value: float, minimum: float = 1.0, maximum: float = 5.0) -> float:
    value = float(value)
    if not minimum <= value <= maximum:
        raise ValueError(f"Score must be between {minimum} and {maximum}; received {value}.")
    return value


def normalize_scores(scores: Mapping[str, float]) -> dict[str, float]:
    return {name: validate_score(value) for name, value in scores.items()}


def weighted_score(
    scores: Mapping[str, float],
    weights: Mapping[str, float] | None = None,
) -> float:
    scores = normalize_scores(scores)
    weights = dict(weights or DEFAULT_WEIGHTS)

    applicable = {k: v for k, v in weights.items() if k in scores}
    if not applicable:
        raise ValueError("No weighted dimensions were present in scores.")

    total_weight = sum(applicable.values())
    return round(
        sum(scores[k] * weight for k, weight in applicable.items()) / total_weight,
        3,
    )


def score_percentage(score: float, maximum: float = 5.0) -> float:
    return round((validate_score(score, 0.0, maximum) / maximum) * 100.0, 1)
