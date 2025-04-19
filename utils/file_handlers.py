from PyPDF2 import PdfReader # type: ignore
from docx import Document # type: ignore

def extract_text(file_path: str) -> str:
    """Extract text from PDF or DOCX files"""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                return " ".join(page.extract_text() for page in reader.pages)
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            return " ".join(para.text for para in doc.paragraphs)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise RuntimeError(f"Error processing file: {str(e)}")