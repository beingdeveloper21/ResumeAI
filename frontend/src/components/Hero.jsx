import React from 'react';
import { Target, Zap, ShieldCheck, Award, ArrowRight } from 'lucide-react';

export default function Hero({ onScrollToDemo }) {
  return (
    <div className="relative pt-8 pb-10 overflow-hidden text-center">
      
      {/* Decorative gradient blur backdrop */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-tr from-blue-600/15 via-cyan-500/10 to-indigo-600/10 blur-[100px] pointer-events-none -z-10" />

      {/* Pill Badge */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-950/60 border border-blue-500/30 text-xs font-medium text-blue-300 mb-5 shadow-inner">
        <Zap className="w-3.5 h-3.5 text-blue-400" />
        <span>Dense Semantic Embeddings (all-MiniLM-L6-v2) + LLM Feedback</span>
      </div>

      {/* Title */}
      <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight max-w-4xl mx-auto leading-tight sm:leading-tight">
        Next-Generation <span className="bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent">AI Resume Analyzer</span> & Job Matcher
      </h1>

      {/* Subtitle */}
      <p className="mt-4 text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
        Extract structured skills, benchmark against job descriptions using 384-dimensional cosine similarity, audit ATS hygiene, and generate high-impact XYZ rewrites and personalized interview questions.
      </p>

      {/* Highlights Bar */}
      <div className="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-4xl mx-auto px-4">
        
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 text-left">
          <div className="flex items-center gap-2 text-blue-400 font-semibold text-sm">
            <Target className="w-4 h-4" />
            <span>Semantic Bi-Encoder</span>
          </div>
          <p className="text-xs text-slate-400 mt-1">all-MiniLM-L6-v2 dense vector similarity over cosine distance</p>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 text-left">
          <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
            <ShieldCheck className="w-4 h-4" />
            <span>ATS Compliance</span>
          </div>
          <p className="text-xs text-slate-400 mt-1">6-point deterministic audit for contact, metrics, and verbs</p>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 text-left">
          <div className="flex items-center gap-2 text-cyan-400 font-semibold text-sm">
            <Award className="w-4 h-4" />
            <span>Google XYZ Rewrites</span>
          </div>
          <p className="text-xs text-slate-400 mt-1">Actionable transformation of passive bullets into metric-driven achievements</p>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 text-left">
          <div className="flex items-center gap-2 text-indigo-400 font-semibold text-sm">
            <Zap className="w-4 h-4" />
            <span>Interview Prep</span>
          </div>
          <p className="text-xs text-slate-400 mt-1">Tailored Technical, System Design & Behavioral Q&As with model talking points</p>
        </div>

      </div>

    </div>
  );
}
