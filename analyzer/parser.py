import spacy # type: ignore
import re
from PyPDF2 import PdfReader # type: ignore
from docx import Document # type: ignore
from typing import Dict, List, Union

nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    def __init__(self):
        self.skill_patterns = [
            [{"LOWER": "python"}], 
            [{"LOWER": "machine"}, {"LOWER": "learning"}],
            [{"LOWER": "data"}, {"LOWER": "analysis"}]
        ]
        self.matcher = spacy.matcher.Matcher(nlp.vocab)
        for pattern in self.skill_patterns:
            self.matcher.add("SKILLS", [pattern])

    def extract_text(self, file_path: str) -> str:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                return " ".join(page.extract_text() for page in reader.pages)
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            return " ".join(para.text for para in doc.paragraphs)
        else:
            raise ValueError("Unsupported file format")

    def extract_entities(self, text: str) -> Dict[str, Union[List[str], int]]:
        doc = nlp(text)
        skills = set()
        exp_years = 0
        education = []
        
        # Extract skills using matcher and noun chunks
        matches = self.matcher(doc)
        for _, start, end in matches:
            skills.add(doc[start:end].text.lower())
        
        # Extract experience
        exp_pattern = r"(\d+)\s*(years?|yrs?|y)"
        for match in re.finditer(exp_pattern, text.lower()):
            exp_years += int(match.group(1))
        
        # Extract education
        edu_terms = ["bachelor", "master", "phd", "doctorate", "bs", "ms", "mba"]
        for token in doc:
            if token.text.lower() in edu_terms:
                education.append(token.text.lower())
        
        return {
            "skills": list(skills),
            "experience": exp_years,
            "education": education,
            "raw_text": text
        }

    def parse(self, file_path: str) -> Dict:
        text = self.extract_text(file_path)
        return self.extract_entities(text)