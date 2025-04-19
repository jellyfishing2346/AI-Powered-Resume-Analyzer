import pytest # type: ignore
from analyzer.parser import ResumeParser
import os

@pytest.fixture
def parser():
    return ResumeParser()

def test_pdf_parsing(parser, tmp_path):
    # Create dummy PDF
    pdf_path = os.path.join(tmp_path, "test.pdf")
    with open(pdf_path, "w") as f:
        f.write("Dummy content")
    
    # Should raise for invalid PDF
    with pytest.raises(Exception):
        parser.extract_text(pdf_path)

def test_skill_extraction(parser):
    test_text = "Expert in Python and Machine Learning"
    result = parser.extract_entities(test_text)
    assert "python" in result["skills"]
    assert "machine learning" in result["skills"]