
import { GoogleGenAI, Type } from "@google/genai";
import { CandidateAnalysis, JobDescription } from "../types";

const MODEL_NAME = 'gemini-3-flash-preview';

export const analyzeResume = async (
  fileBase64: string,
  fileName: string,
  mimeType: string,
  jobDesc: JobDescription
): Promise<CandidateAnalysis> => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });

  const prompt = `
    Analyze the attached resume against the following Job Description:
    
    JOB TITLE: ${jobDesc.title}
    COMPANY: ${jobDesc.company}
    SENIORITY: ${jobDesc.seniority}
    REQUIREMENTS: ${jobDesc.requirements}

    Perform a deep NLP analysis to determine:
    1. Candidate Name (extract from resume).
    2. Overall fit score (0-100).
    3. Match of skills (Technical, Soft, Domain).
    4. Key missing skills compared to JD.
    5. Years of relevant experience.
    6. Summary of pros and cons.
    7. A final verdict.

    Focus on identifying if they are "Qualified" or "Underqualified".
  `;

  const response = await ai.models.generateContent({
    model: MODEL_NAME,
    contents: [
      {
        parts: [
          { text: prompt },
          { inlineData: { data: fileBase64, mimeType: mimeType } }
        ]
      }
    ],
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          candidateName: { type: Type.STRING },
          score: { type: Type.NUMBER },
          summary: { type: Type.STRING },
          topSkills: { type: Type.ARRAY, items: { type: Type.STRING } },
          missingSkills: { type: Type.ARRAY, items: { type: Type.STRING } },
          yearsExperience: { type: Type.NUMBER },
          pros: { type: Type.ARRAY, items: { type: Type.STRING } },
          cons: { type: Type.ARRAY, items: { type: Type.STRING } },
          verdict: { type: Type.STRING, description: "One of: Qualified, Neutral, Underqualified" }
        },
        required: ["candidateName", "score", "summary", "topSkills", "missingSkills", "yearsExperience", "pros", "cons", "verdict"]
      }
    }
  });

  if (!response.text) {
    throw new Error("AI response text is undefined");
  }
  const rawResult = JSON.parse(response.text);
  
  return {
    ...rawResult,
    id: Math.random().toString(36).substr(2, 9),
    fileName,
    rank: 0, // Assigned later by sorting
  };
};