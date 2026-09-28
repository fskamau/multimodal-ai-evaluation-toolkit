import pytest

from multimodal_eval.scoring import validate_score, weighted_score


def test_validate_score_accepts_valid_value():
    assert validate_score(4) == 4.0


def test_validate_score_rejects_out_of_range():
    with pytest.raises(ValueError):
        validate_score(6)


def test_weighted_score_uses_available_dimensions():
    result = weighted_score({"factuality": 5, "instruction_following": 3})
    assert 3 <= result <= 5
