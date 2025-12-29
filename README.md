# Full Stack Setup: React Frontend & FastAPI Backend

## Backend (Python/FastAPI)

1. Open the `backend/` folder.
2. (Optional) Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```
    The backend will be available at http://127.0.0.1:8000

## Frontend (React)

1. Make sure you are in the project root directory.
2. Install dependencies:
    ```sh
    npm install
    ```
3. (If you add a start script) Start the frontend:
    ```sh
    npm start
    ```
    (Or use your preferred React build tool.)

## Connecting Frontend & Backend

The React frontend can make HTTP requests to the FastAPI backend at `http://localhost:8000`.

---
# Aura AI: Resume Intelligence 🚀

Aura AI is a high-performance, AI-driven resume analyzer and candidate ranking system. It leverages advanced NLP via the **Gemini 3 Flash** model to provide deep insights into candidate qualifications, skill gaps, and job fit.

![Aura AI Branding](https://img.shields.io/badge/Aura-AI--Intelligence-6366f1?style=for-the-badge)

## ✨ Features

- **NLP-Powered Ranking**: Automatically score and rank candidates on a scale of 0-100 based on job description alignment.
- **Deep Sentiment Analysis**: Extract nuanced pros and cons from resume text, going beyond simple keyword matching.
- **Interactive Talent Pipeline**: View your entire candidate pool in a structured, ranked list with visual health indicators.
- **Visual Analytics**: Real-time bar charts using Recharts to visualize the distribution of candidate scores.
- **Dynamic Job Editor**: Adjust requirements, seniority levels, and role titles on the fly to see how rankings shift.
- **Multimodal Support**: Process PDF, TXT, and Word documents using Gemini's multimodal capabilities.

## 🛠️ Tech Stack

- **Frontend**: React (ES6+), TypeScript.
- **Styling**: Tailwind CSS (Glassmorphism UI).
- **Intelligence**: Google Gemini API (`@google/genai`).
- **Data Viz**: Recharts.
- **Build/Env**: ESM modules, modern browser environment.

## 🚀 Getting Started

### Prerequisites

- A modern browser with ES6 module support.
- A valid Google Gemini API Key. The application expects this to be provided via the `process.env.API_KEY` environment variable.

### Installation & Setup

1.  **Clone the project** into your root directory.
2.  **Ensure Environment Variables**: The app retrieves the API key automatically.
3.  **Launch**: Open `index.html` in a supported development environment or server.

## 📖 Usage Guide

### 1. Define the Role
Navigate to the **Resume Analyzer** tab. Enter the Role Title, Company, and detailed Requirements. You can use the segmented control to quickly toggle seniority levels.

### 2. Upload Resumes
Drop one or multiple resumes into the upload zone. Aura AI will process them in parallel using the Gemini 3 Flash engine.

### 3. Analyze Results
- **Summary Dashboard**: View top candidates and scoring distribution instantly.
- **Pipeline View**: Click on "Pipeline" in the navigation to see a full-width, deep dive into every candidate. This includes specific missing skills and an AI-generated summary.
- **Settings**: Adjust system strictness or wipe local session data to start a new hiring batch.

## 📁 Project Structure

```text
.
├── App.tsx                 # Main application state & orchestration
├── index.html              # Entry point & Tailwind/Font configurations
├── index.tsx               # React DOM mounting
├── types.ts                # Shared interfaces (Candidate, Job, Views)
├── metadata.json           # Application metadata
├── components/
│   ├── Layout.tsx          # Wrapper with navigation & global styling
│   ├── FileUpload.tsx      # Specialized file handling & base64 encoding
│   └── CandidateChart.tsx  # Visualization logic for scoring
└── services/
    └── geminiService.ts    # AI integration logic & prompt engineering
```

## 🛡️ Architecture & Security

- **Client-Side Processing**: All resume parsing and AI requests happen directly from the client to the Gemini API.
- **Prompt Engineering**: Uses a sophisticated JSON schema-based prompt to ensure consistent, structured responses from the LLM.
- **Glassmorphism UI**: Uses Tailwind's backdrop-filter for a premium, modern software-as-a-service aesthetic.

---