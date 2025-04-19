from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from typing import Dict, List

class ResumeRanker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def calculate_skill_match(self, 
                           resume_skills: List[str], 
                           required_skills: List[str]) -> float:
        if not required_skills:
            return 0.0
        matched = sum(1 for skill in resume_skills if skill in required_skills)
        return matched / len(required_skills)

    def calculate_experience_score(self, 
                                exp_years: int, 
                                exp_levels: Dict) -> float:
        if not exp_levels:
            return 0.0
        max_exp = max(level["max"] for level in exp_levels.values())
        return min(exp_years / max_exp, 1.0)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        tfidf = self.vectorizer.fit_transform([text1, text2])
        return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    def rank(self, 
           resume_data: Dict, 
           required_skills: List[str],
           exp_levels: Dict) -> Dict:
        skill_score = self.calculate_skill_match(
            resume_data["skills"], 
            required_skills
        )
        exp_score = self.calculate_experience_score(
            resume_data["experience"],
            exp_levels
        )
        return {
            "score": 0.6 * skill_score + 0.4 * exp_score,
            "skill_match": skill_score,
            "experience_score": exp_score
        }