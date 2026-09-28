from multimodal_eval.pairwise import compare_responses


def test_pairwise_selects_higher_scoring_response():
    result = compare_responses(
        evaluation_id="pair_001",
        response_a="Response A",
        response_b="Response B",
        scores_a={"factuality": 5, "instruction_following": 5},
        scores_b={"factuality": 3, "instruction_following": 3},
    )

    assert result.preferred_response == "A"
    assert result.preference_strength in {"MODERATE", "STRONG"}
