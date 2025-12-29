# Backend (FastAPI)

## Setup

1. Create a virtual environment (optional but recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

The backend will be available at http://127.0.0.1:8000

You can now add your NLP and resume analysis endpoints in `main.py`.
