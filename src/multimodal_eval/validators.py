from __future__ import annotations

from collections.abc import Mapping, Sequence

ALLOWED_TASK_TYPES = {"text", "multimodal", "image_qa", "tool_use", "pairwise"}


def require_non_empty_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")
    return value.strip()


def validate_task_type(task_type: str) -> str:
    task_type = require_non_empty_string(task_type, "task_type")
    if task_type not in ALLOWED_TASK_TYPES:
        raise ValueError(
            f"Unsupported task_type '{task_type}'. "
            f"Expected one of: {', '.join(sorted(ALLOWED_TASK_TYPES))}."
        )
    return task_type


def validate_dimensions(scores: Mapping[str, float]) -> None:
    if not isinstance(scores, Mapping) or not scores:
        raise ValueError("scores must be a non-empty mapping.")


def validate_errors(errors: Sequence[Mapping[str, object]] | None) -> None:
    if errors is None:
        return
    if isinstance(errors, (str, bytes)) or not isinstance(errors, Sequence):
        raise ValueError("errors must be a sequence of mappings.")
    for item in errors:
        if not isinstance(item, Mapping):
            raise ValueError("Each error must be a mapping.")
        if "type" not in item:
            raise ValueError("Each error requires a 'type' field.")
