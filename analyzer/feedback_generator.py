import json
from typing import Dict, List

class FeedbackGenerator:
    def __init__(self):
        self.templates = {
            "skills": {
                "high": "Excellent skills match for {role} role",
                "medium": "Good foundation but could strengthen {missing} skills",
                "low": "Consider developing core {role} skills: {missing}"
            },
            "experience": {
                "senior": "Strong experience for senior positions",
                "mid": "Well-qualified for mid-level roles",
                "junior": "Would benefit from more practical experience"
            }
        }
        self.benchmarks = self.load_benchmarks()

    def load_benchmarks(self) -> Dict:
        """Load role benchmarks from JSON file"""
        try:
            with open('analyzer/role_benchmarks.json') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def generate_skill_feedback(self, 
                              skills: List[str], 
                              required: List[str], 
                              role: str) -> List[str]:
        missing = [skill for skill in required if skill not in skills]
        match_ratio = len(skills) / len(required) if required else 0
        
        if match_ratio > 0.75:
            return [self.templates["skills"]["high"].format(role=role)]
        elif match_ratio > 0.5:
            return [self.templates["skills"]["medium"].format(
                missing=", ".join(missing[:3])
            )]
        else:
            return [self.templates["skills"]["low"].format(
                role=role,
                missing=", ".join(missing[:5])
            )]

    def generate_experience_feedback(self, 
                                   years: int, 
                                   levels: Dict) -> List[str]:
        if years >= 6:
            return [self.templates["experience"]["senior"]]
        elif years >= 3:
            return [self.templates["experience"]["mid"]]
        else:
            return [self.templates["experience"]["junior"]]

    def generate(self, 
                resume_data: Dict, 
                ranking: Dict, 
                role: str) -> Dict:
        """Generate feedback based on resume data and role requirements"""
        role_benchmarks = self.benchmarks.get(role, {})
        
        feedback = {
            "strengths": [],
            "improvements": []
        }
        
        # Skill feedback
        feedback["improvements"].extend(
            self.generate_skill_feedback(
                resume_data["skills"],
                role_benchmarks.get("required_skills", []),
                role
            )
        )
        
        # Experience feedback
        feedback["improvements"].extend(
            self.generate_experience_feedback(
                resume_data["experience"],
                role_benchmarks.get("experience_levels", {})
            )
        )
        
        # Positive feedback for strong matches
        if ranking["skill_match"] > 0.8:
            feedback["strengths"].append(
                "Your technical skills closely match this role's requirements"
            )
        
        if ranking["experience_score"] > 0.7:
            feedback["strengths"].append(
                "You have substantial relevant experience"
            )
        
        return feedback