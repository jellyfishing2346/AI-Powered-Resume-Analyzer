import React, { useState, useMemo } from 'react';
import { Layout } from './components/Layout';
import { FileUpload } from './components/FileUpload';
import { CandidateChart } from './components/CandidateChart';
import { analyzeResume } from './services/geminiService';
import { CandidateAnalysis, JobDescription, AppStatus, View } from './types';

const INITIAL_JD: JobDescription = {
  title: 'Senior Software Engineer',
  company: 'Aura Tech',
  seniority: 'Senior',
  requirements: '5+ years React, TypeScript, Node.js, AWS experience. Strong problem solving and team leadership skills.'
};

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<View>('analyzer');
  const [jobDesc, setJobDesc] = useState<JobDescription>(INITIAL_JD);
  const [candidates, setCandidates] = useState<CandidateAnalysis[]>([]);
  const [status, setStatus] = useState<AppStatus>(AppStatus.IDLE);
  const [error, setError] = useState<string | null>(null);

  const sortedCandidates = useMemo(() => {
    return [...candidates].sort((a, b) => b.score - a.score).map((c, i) => ({ ...c, rank: i + 1 }));
  }, [candidates]);

  const handleFilesSelected = async (files: File[]) => {
    setStatus(AppStatus.ANALYZING);
    setError(null);
    
    try {
      const results: CandidateAnalysis[] = [];
      for (const file of files) {
        const base64 = await fileToBase64(file);
        const analysis = await analyzeResume(base64, file.name, file.type, jobDesc);
        results.push(analysis);
      }
      setCandidates(prev => [...prev, ...results]);
      setStatus(AppStatus.COMPLETED);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze one or more resumes. Ensure your API key is configured.");
      setStatus(AppStatus.ERROR);
    }
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const result = reader.result as string;
        resolve(result.split(',')[1]);
      };
      reader.onerror = error => reject(error);
    });
  };

  const resetPipeline = () => {
    setCandidates([]);
    setStatus(AppStatus.IDLE);
  };

  const seniorityLevels = ['Junior', 'Mid', 'Senior', 'Lead'];

  const renderAnalyzer = () => (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="space-y-6">
        <div className="glass-panel p-6 rounded-2xl shadow-sm bg-white border">
          <h2 className="text-lg font-semibold mb-6 flex items-center">
            <span className="bg-indigo-100 p-2 rounded-lg mr-2 text-xl">📋</span>
            Job Description
          </h2>
          <div className="space-y-6">
            <div>
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Role Title</label>
              <input 
                type="text" 
                placeholder="e.g. Senior Frontend Engineer"
                value={jobDesc.title}
                onChange={(e) => setJobDesc({...jobDesc, title: e.target.value})}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all placeholder:text-gray-300 shadow-sm"
              />
            </div>
            
            <div>
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Company Name</label>
              <input 
                type="text" 
                placeholder="e.g. Google"
                value={jobDesc.company}
                onChange={(e) => setJobDesc({...jobDesc, company: e.target.value})}
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all placeholder:text-gray-300 shadow-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Seniority Level</label>
              <div className="flex p-1 bg-gray-100 rounded-xl border border-gray-200 shadow-inner">
                {seniorityLevels.map((level) => (
                  <button
                    key={level}
                    onClick={() => setJobDesc({ ...jobDesc, seniority: level })}
                    className={`flex-1 py-2 text-xs font-bold rounded-lg transition-all ${
                      jobDesc.seniority === level
                        ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-black/5'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-white/50'
                    }`}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Requirements & Skills</label>
              <textarea 
                rows={6}
                placeholder="Describe key qualifications, tech stack, and experience required..."
                value={jobDesc.requirements}
                onChange={(e) => setJobDesc({...jobDesc, requirements: e.target.value})}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none transition-all placeholder:text-gray-300 shadow-sm"
              />
            </div>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl shadow-sm bg-white border">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <span className="bg-indigo-100 p-2 rounded-lg mr-2 text-xl">📤</span>
            Upload Resumes
          </h2>
          <FileUpload onFilesSelected={handleFilesSelected} isLoading={status === AppStatus.ANALYZING} />
          {error && (
            <div className="mt-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100">
              {error}
            </div>
          )}
        </div>
      </div>

     
      <div className="lg:col-span-2 space-y-6">
        <div className="glass-panel p-6 rounded-2xl shadow-sm bg-white border">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-lg font-semibold">Active Session</h2>
              <p className="text-sm text-gray-500">Summary of currently analyzed batch</p>
            </div>
            <button onClick={resetPipeline} className="text-sm text-indigo-600 hover:text-indigo-800 font-medium">
              Clear All
            </button>
          </div>
          
          {candidates.length > 0 ? (
            <div className="space-y-6">
              <CandidateChart data={candidates} />
              <div className="space-y-3">
                {sortedCandidates.slice(0, 3).map((candidate) => (
                   <div key={candidate.id} className="border rounded-xl p-4 bg-gray-50/50 hover:bg-white hover:border-indigo-100 transition-all cursor-default shadow-sm border-gray-100">
                     <div className="flex justify-between items-center">
                        <div>
                          <div className="font-bold text-gray-900">{candidate.candidateName}</div>
                          <div className="text-[10px] text-gray-400 uppercase font-bold tracking-tight">{candidate.yearsExperience} yrs experience</div>
                        </div>
                        <div className="text-indigo-600 font-black text-lg">{candidate.score}%</div>
                     </div>
                   </div>
                ))}
                {candidates.length > 3 && (
                   <button 
                     onClick={() => setCurrentView('pipeline')}
                     className="w-full py-3 text-sm text-gray-500 hover:text-indigo-600 transition-colors font-medium border-t"
                   >
                     View all {candidates.length} candidates in Pipeline &rarr;
                   </button>
                )}
              </div>
            </div>
          ) : (
            <div className="h-80 flex flex-col items-center justify-center text-center text-gray-400">
              <div className="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-4 text-3xl border border-dashed border-gray-200">📊</div>
              <h3 className="text-gray-900 font-semibold">Ready for Analysis</h3>
              <p className="text-sm mt-1">Upload candidate resumes to begin ranking.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  const renderPipeline = () => (
    <div className="animate-in fade-in slide-in-from-right-4 duration-500">
      <div className="mb-8 flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Talent Pipeline</h2>
          <p className="text-gray-500">Exhaustive list of all processed resumes ranked by AI qualification score.</p>
        </div>
        <div className="flex space-x-2">
          <button className="px-4 py-2 border rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">Export CSV</button>
          <button onClick={resetPipeline} className="px-4 py-2 bg-red-50 text-red-600 border border-red-100 rounded-lg text-sm font-medium hover:bg-red-100 transition-colors">Wipe Data</button>
        </div>
      </div>

      {sortedCandidates.length > 0 ? (
        <div className="grid grid-cols-1 gap-4">
          {sortedCandidates.map((candidate) => (
            <div key={candidate.id} className="glass-panel p-6 rounded-2xl shadow-sm bg-white border hover:border-indigo-200 transition-all">
              <div className="flex flex-col md:flex-row justify-between gap-6">
                <div className="flex items-start gap-4 flex-1">
                  <div className="w-14 h-14 rounded-2xl bg-indigo-600 flex items-center justify-center text-white text-xl font-bold shadow-indigo-200 shadow-lg shrink-0">
                    #{candidate.rank}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{candidate.candidateName}</h3>
                    <p className="text-sm text-gray-500 mb-3">{candidate.yearsExperience} Years Exp • {candidate.fileName}</p>
                    <div className="flex flex-wrap gap-2">
                      {candidate.topSkills.map(skill => (
                        <span key={skill} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-medium border">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex flex-col md:items-end justify-between shrink-0">
                  <div className="text-right">
                    <div className={`text-4xl font-black ${
                      candidate.score > 80 ? 'text-emerald-500' : 
                      candidate.score > 50 ? 'text-indigo-500' : 
                      'text-rose-500'
                    }`}>
                      {candidate.score}%
                    </div>
                    <div className={`inline-block px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest mt-1 border ${
                       candidate.verdict === 'Qualified' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 
                       candidate.verdict === 'Neutral' ? 'bg-gray-50 text-gray-500 border-gray-100' :
                       'bg-rose-50 text-rose-600 border-rose-100'
                    }`}>
                      {candidate.verdict}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 pt-6 border-t grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 flex items-center">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-2"></span>
                    Candidate Strengths
                  </h4>
                  <ul className="space-y-2">
                    {candidate.pros.map((pro, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start">
                        <span className="text-emerald-500 mr-2">✓</span> {pro}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 flex items-center">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mr-2"></span>
                    Gaps & Concerns
                  </h4>
                  <ul className="space-y-2">
                    {candidate.missingSkills.length > 0 ? (
                      candidate.missingSkills.map((gap, i) => (
                        <li key={i} className="text-sm text-gray-700 flex items-start">
                          <span className="text-rose-500 mr-2">!</span> Missing: {gap}
                        </li>
                      ))
                    ) : (
                      <li className="text-sm text-gray-400 italic">No significant gaps found.</li>
                    )}
                  </ul>
                </div>
              </div>
              <div className="mt-4 p-4 bg-gray-50 rounded-xl text-sm text-gray-600 italic border border-dashed border-gray-200">
                "{candidate.summary}"
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="glass-panel p-20 rounded-3xl text-center border">
          <div className="text-6xl mb-6">🔦</div>
          <h3 className="text-xl font-bold mb-2">The Pipeline is Empty</h3>
          <p className="text-gray-500 max-w-sm mx-auto mb-8">Start by uploading resumes in the analyzer tab to see them appear here with detailed scoring.</p>
          <button onClick={() => setCurrentView('analyzer')} className="px-6 py-2 bg-indigo-600 text-white rounded-xl shadow-lg shadow-indigo-200 font-medium">Go to Analyzer</button>
        </div>
      )}
    </div>
  );

  const renderSettings = () => (
    <div className="max-w-2xl mx-auto animate-in fade-in slide-in-from-left-4 duration-500">
      <h2 className="text-3xl font-bold text-gray-900 mb-8">System Settings</h2>
      <div className="space-y-6">
        <div className="glass-panel p-6 rounded-2xl border bg-white shadow-sm">
          <h3 className="text-lg font-bold mb-4">AI Configuration</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Model Engine</label>
              <select className="w-full px-3 py-2 border rounded-lg bg-gray-50 text-gray-500" disabled>
                <option>Gemini 3 Flash Preview (Optimized for Speed)</option>
              </select>
              <p className="text-[10px] text-gray-400 mt-1">High-performance multimodal NLP for resume parsing.</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Strictness Level</label>
              <input type="range" className="w-full accent-indigo-600" min="0" max="100" defaultValue="70" />
              <div className="flex justify-between text-[10px] text-gray-400 uppercase font-bold tracking-tighter">
                <span>Lenient</span>
                <span>Standard</span>
                <span>Strict</span>
              </div>
            </div>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border bg-white shadow-sm">
          <h3 className="text-lg font-bold mb-4 text-rose-600">Danger Zone</h3>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-bold text-gray-900">Clear All Local Data</p>
              <p className="text-xs text-gray-500">Wipe all candidate data and session history.</p>
            </div>
            <button onClick={resetPipeline} className="px-4 py-2 border border-rose-200 text-rose-600 rounded-lg text-sm font-medium hover:bg-rose-50 transition-colors">Wipe Memory</button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <Layout currentView={currentView} onViewChange={setCurrentView}>
      {currentView === 'analyzer' && renderAnalyzer()}
      {currentView === 'pipeline' && renderPipeline()}
      {currentView === 'settings' && renderSettings()}
    </Layout>
  );
};

export default App;

