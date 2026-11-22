import React, { useState, useEffect, useRef } from 'react';
import confetti from 'canvas-confetti';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import FileUploader from './components/FileUploader';
import JobDescriptionInput from './components/JobDescriptionInput';
import AnalysisProgress from './components/AnalysisProgress';
import MatchScoreCard from './components/MatchScoreCard';
import SkillsBreakdown from './components/SkillsBreakdown';
import AtsChecklist from './components/AtsChecklist';
import SuggestionsSection from './components/SuggestionsSection';
import InterviewPrepHub from './components/InterviewPrepHub';
import ArchitectureModal from './components/ArchitectureModal';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

const API_BASE = '/api';

export default function App() {
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [targetRole, setTargetRole] = useState('Full Stack Software Engineer');
  const [presets, setPresets] = useState([]);
  
  const [analysisData, setAnalysisData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isBackendHealthy, setIsBackendHealthy] = useState(false);
  const [isArchitectureOpen, setIsArchitectureOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const resultsRef = useRef(null);

  // Initialize and check backend health & presets
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
          setIsBackendHealthy(true);
        }
      } catch (err) {
        setIsBackendHealthy(false);
      }
    };

    const fetchPresets = async () => {
      try {
        const res = await fetch(`${API_BASE}/presets`);
        if (res.ok) {
          const data = await res.json();
          setPresets(data.presets || []);
          if (data.presets && data.presets.length > 0) {
            setTargetRole(data.presets[0].role);
            setJobDescription(data.presets[0].description);
          }
        }
      } catch (err) {
        console.error("Presets error:", err);
      }
    };

    checkHealth();
    fetchPresets();
  }, []);

  // 1-Click Sample Resume Loader
  const handleLoadSampleResume = async () => {
    try {
      const res = await fetch('/sample-resume.pdf');
      if (res.ok) {
        const blob = await res.blob();
        const sampleFile = new File([blob], 'sample_software_engineer.pdf', { type: 'application/pdf' });
        setFile(sampleFile);
        setResumeText('');
      } else {
        // Fallback text
        setResumeText(`Alex Morgan
alex.morgan.tech@gmail.com | +1 (555) 234-5678 | San Francisco, CA
Full Stack & Machine Learning Engineer

SKILLS: Python, TypeScript, JavaScript, FastAPI, React, Node.js, PyTorch, Docker, Kubernetes, AWS, PostgreSQL, Redis, Sentence-Transformers (all-MiniLM-L6-v2), OpenAI API.

EXPERIENCE:
Software Engineer II | Cognitive Solutions Inc. (2023 - Present)
- Architected high-throughput RESTful microservices with FastAPI and PostgreSQL handling 40,000+ daily requests with sub-50ms latency.
- Implemented semantic search pipelines using Sentence-Transformers (all-MiniLM-L6-v2) and cosine similarity, elevating document match precision by 32%.
- Engineered single-page user dashboards in React and Tailwind CSS, increasing candidate submission conversion by 28%.
- Automated multi-stage Docker container builds and CI/CD pipelines in GitHub Actions, slashing deploy times by 65%.

EDUCATION:
Bachelor of Science in Computer Science | UC Berkeley (2017 - 2021)`);
      }
    } catch (err) {
      console.error("Error loading sample resume:", err);
    }
  };

  const handleSelectPreset = (preset) => {
    setTargetRole(preset.role);
    setJobDescription(preset.description);
  };

  const handleAnalyze = async () => {
    if (!file && !resumeText.trim()) {
      setErrorMessage("Please upload a PDF resume or paste resume text to begin.");
      return;
    }
    if (!jobDescription.trim()) {
      setErrorMessage("Please enter or select a target job description.");
      return;
    }

    setErrorMessage('');
    setIsLoading(true);
    setAnalysisData(null);

    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('target_role', targetRole);
    if (file) {
      formData.append('file', file);
    } else {
      formData.append('resume_text', resumeText);
    }

    try {
      const res = await fetch(`${API_BASE}/full-analysis`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to analyze resume. Please verify file format.");
      }

      const data = await res.json();
      setAnalysisData(data);

      // Trigger celebratory confetti for strong matches
      if (data.match?.overall_match_score >= 75) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      }

      // Smooth scroll to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 200);

    } catch (err) {
      setErrorMessage(err.message || "An unexpected error occurred during analysis.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadCandidateReport = async () => {
    if (!analysisData) return;
    try {
      const res = await fetch(`${API_BASE}/export-report?target_role=${encodeURIComponent(targetRole)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(analysisData)
      });
      if (!res.ok) throw new Error("Could not export report.");
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const cand = (analysisData.resume?.contact?.name || 'Candidate').replace(/\s+/g, '_');
      a.download = `ResumeAI_Report_${cand}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Error generating PDF report: " + err.message);
    }
  };

  const handleDownloadMasterGuide = () => {
    // Direct link to the generated master interview and architecture PDF
    window.open('/api/master-guide-pdf', '_blank');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      
      {/* Top Navbar */}
      <Navbar
        onOpenArchitecture={() => setIsArchitectureOpen(true)}
        onDownloadGuide={handleDownloadMasterGuide}
        isBackendHealthy={isBackendHealthy}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        
        {/* Hero Section */}
        <Hero onScrollToDemo={() => window.scrollTo({ top: 380, behavior: 'smooth' })} />

        {/* Input Interface Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <FileUploader
            file={file}
            setFile={setFile}
            resumeText={resumeText}
            setResumeText={setResumeText}
            onLoadSampleResume={handleLoadSampleResume}
          />
          <JobDescriptionInput
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            targetRole={targetRole}
            setTargetRole={setTargetRole}
            presets={presets}
            onSelectPreset={handleSelectPreset}
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
          />
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs sm:text-sm flex items-center gap-3 mb-8">
            <AlertCircle className="w-5 h-5 shrink-0 text-rose-400" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Loading Progress State */}
        {isLoading && <AnalysisProgress />}

        {/* Results Dashboard */}
        {analysisData && (
          <div ref={resultsRef} className="space-y-8 animate-fadeIn">
            
            {/* Main Scorecard */}
            <MatchScoreCard
              match={analysisData.match}
              feedback={analysisData.feedback}
              onDownloadReport={handleDownloadCandidateReport}
              candidateName={analysisData.resume?.contact?.name}
              targetRole={targetRole}
            />

            {/* Skills Alignment Matrix */}
            <SkillsBreakdown
              match={analysisData.match}
              resume={analysisData.resume}
            />

            {/* ATS Compliance Checklist */}
            <AtsChecklist
              checks={analysisData.match?.ats_checks}
              atsScore={analysisData.match?.ats_compatibility_score}
            />

            {/* AI Optimization & XYZ Rewrites */}
            <SuggestionsSection
              feedback={analysisData.feedback}
            />

            {/* Technical Interview Prep Hub */}
            <InterviewPrepHub
              questions={analysisData.feedback?.interview_questions}
            />

          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>
            ResumeAI &copy; {new Date().getFullYear()} &bull; Built with FastAPI, Sentence-Transformers, OpenAI API, and React.
          </p>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setIsArchitectureOpen(true)}
              className="hover:text-slate-300 transition"
            >
              Architecture & Stack
            </button>
            <button
              onClick={handleDownloadMasterGuide}
              className="hover:text-slate-300 transition"
            >
              Master PDF Guide
            </button>
            <a
              href="https://github.com/beingdeveloper21/ResumeAI"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-slate-300 transition"
            >
              GitHub Repository
            </a>
          </div>
        </div>
      </footer>

      {/* Architecture Deep Dive Modal */}
      <ArchitectureModal
        isOpen={isArchitectureOpen}
        onClose={() => setIsArchitectureOpen(false)}
        onDownloadGuide={handleDownloadMasterGuide}
      />

    </div>
  );
}
