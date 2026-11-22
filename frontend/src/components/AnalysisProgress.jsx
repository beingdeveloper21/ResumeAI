import React, { useEffect, useState } from 'react';
import { Cpu, FileSearch, Sparkles, CheckCircle2, ShieldCheck, Target } from 'lucide-react';

const STEPS = [
  { icon: FileSearch, title: "Parsing PDF Document Streams", desc: "Extracting raw text and metadata via PyPDF & PyMuPDF fallback..." },
  { icon: Cpu, title: "Taxonomy & Entity Recognition", desc: "Identifying categorized skills, experience dates, and contact vectors..." },
  { icon: Target, title: "Dense Semantic Vector Encoding", desc: "Running Sentence-Transformers (all-MiniLM-L6-v2) for 384-dim cosine distance..." },
  { icon: ShieldCheck, title: "Deterministic ATS Hygiene Audit", desc: "Verifying keyword density, measurable metrics, and action verbs..." },
  { icon: Sparkles, title: "LLM Feedback & Interview Synthesis", desc: "Crafting XYZ bullet rewrites and customized technical questions..." }
];

export default function AnalysisProgress() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 700);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="bg-slate-900/90 border border-blue-500/30 rounded-2xl p-6 shadow-2xl max-w-2xl mx-auto my-8">
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 mb-3 animate-spin">
          <Cpu className="w-6 h-6" />
        </div>
        <h3 className="text-lg font-bold text-slate-100">Running ResumeAI Pipeline</h3>
        <p className="text-xs text-slate-400 mt-1">Executing end-to-end NLP parsing, semantic embedding, and LLM synthesis</p>
      </div>

      <div className="space-y-3.5">
        {STEPS.map((step, idx) => {
          const StepIcon = step.icon;
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div
              key={idx}
              className={`flex items-start gap-3.5 p-3 rounded-xl border transition ${
                isCurrent
                  ? 'bg-blue-950/40 border-blue-500/40 shadow-sm shadow-blue-500/10'
                  : isDone
                  ? 'bg-slate-950/50 border-slate-800 opacity-90'
                  : 'bg-slate-950/20 border-slate-900 opacity-40'
              }`}
            >
              <div className="mt-0.5 shrink-0">
                {isDone ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                ) : (
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${isCurrent ? 'bg-blue-500 text-white animate-pulse' : 'bg-slate-800 text-slate-500'}`}>
                    {idx + 1}
                  </div>
                )}
              </div>
              <div>
                <p className={`text-xs sm:text-sm font-semibold ${isCurrent ? 'text-blue-300' : isDone ? 'text-slate-200' : 'text-slate-500'}`}>
                  {step.title}
                </p>
                <p className="text-[11px] sm:text-xs text-slate-400 mt-0.5">{step.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
