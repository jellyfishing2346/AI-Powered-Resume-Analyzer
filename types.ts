
export type View = 'analyzer' | 'pipeline' | 'settings';

export interface Skill {
  name: string;
  category: 'technical' | 'soft' | 'domain';
  match: boolean;
}

export interface CandidateAnalysis {
  id: string;
  fileName: string;
  candidateName: string;
  score: number; // 0-100
  rank: number;
  summary: string;
  topSkills: string[];
  missingSkills: string[];
  yearsExperience: number;
  pros: string[];
  cons: string[];
  verdict: 'Qualified' | 'Neutral' | 'Underqualified';
}

export interface JobDescription {
  title: string;
  company: string;
  requirements: string;
  seniority: string;
}

export enum AppStatus {
  IDLE = 'IDLE',
  ANALYZING = 'ANALYZING',
  COMPLETED = 'COMPLETED',
  ERROR = 'ERROR'
}