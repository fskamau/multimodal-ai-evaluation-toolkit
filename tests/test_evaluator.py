from multimodal_eval.evaluator import evaluate_response


def test_evaluator_returns_structured_result():
    result = evaluate_response(
        evaluation_id="eval_001",
        task_type="text",
        prompt="Summarize the passage.",
        response="A concise summary.",
        scores={
            "factuality": 5,
            "instruction_following": 5,
            "completeness": 4,
            "relevance": 5,
            "grounding": 4,
        },
    )

    payload = result.to_dict()
    assert payload["evaluation_id"] == "eval_001"
    assert payload["verdict"] in {"PASS", "PASS_WITH_ISSUES"}
    assert payload["overall_score"] > 0
