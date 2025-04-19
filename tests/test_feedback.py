import pytest # type: ignore
from analyzer.feedback_generator import FeedbackGenerator

@pytest.fixture
def feedback_gen():
    return FeedbackGenerator()

def test_skill_feedback_high(feedback_gen):
    feedback = feedback_gen.generate_skill_feedback(
        ["python", "machine learning", "sql"],
        ["python", "sql"],
        "data_scientist"
    )
    assert "Excellent" in feedback[0]

def test_skill_feedback_low(feedback_gen):
    feedback = feedback_gen.generate_skill_feedback(
        ["python"],
        ["python", "sql", "statistics"],
        "data_scientist"
    )
    assert "Consider developing" in feedback[0]

def test_experience_feedback(feedback_gen):
    feedback = feedback_gen.generate_experience_feedback(
        4,
        {"junior": {"min": 0, "max": 2},
         "mid": {"min": 3, "max": 5}}
    )
    assert "mid-level" in feedback[0]