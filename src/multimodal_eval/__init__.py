"""Multimodal AI Evaluation Toolkit."""

from .evaluator import EvaluationResult, evaluate_response
from .pairwise import PairwiseResult, compare_responses
from .taxonomy import ErrorType, Severity
from .reporting import generate_markdown_report

__all__ = [
    "EvaluationResult",
    "evaluate_response",
    "PairwiseResult",
    "compare_responses",
    "ErrorType",
    "Severity",
    "generate_markdown_report",
]
