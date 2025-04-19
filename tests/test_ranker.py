import pytest # type: ignore
from analyzer.ranker import ResumeRanker

@pytest.fixture
def ranker():
    return ResumeRanker()

def test_skill_match(ranker):
    score = ranker.calculate_skill_match(
        ["python", "sql"],
        ["python", "java", "sql"]
    )
    assert score == pytest.approx(0.666, 0.01)

def test_experience_score(ranker):
    score = ranker.calculate_experience_score(
        3,
        {"junior": {"min": 0, "max": 2},
         "senior": {"min": 5, "max": 10}}
    )
    assert score == pytest.approx(0.3)