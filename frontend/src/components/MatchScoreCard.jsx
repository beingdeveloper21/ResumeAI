import React from 'react';
import { Target, Zap, ShieldCheck, Download, Award, Clock } from 'lucide-react';

export default function MatchScoreCard({ match, feedback, onDownloadReport, candidateName, targetRole }) {
  const overall = match.overall_match_score;
  const semantic = match.semantic_similarity_score;
  const keyword = match.keyword_match_score;
  const ats = match.ats_compatibility_score;

  // Determine accent color
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-emerald-400 border-emerald-500/40 bg-emerald-950/20';
    if (score >= 60) return 'text-cyan-400 border-cyan-500/40 bg-cyan-950/20';
    return 'text-amber-400 border-amber-500/40 bg-amber-950/20';
  };

  const getScoreStroke = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#06b6d4';
    return '#f59e0b';
  };

  // SVG circular gauge math
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (overall / 100) * circumference;

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-2xl">
      
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <span className="px-2.5 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-blue-500/10 text-blue-400 border border-blue-500/20">
            Evaluation Complete
          </span>
          <h2 className="text-xl sm:text-2xl font-bold text-white mt-2">
            Match Analysis for <span className="text-blue-400">{candidateName || "Candidate"}</span>
          </h2>
          <p className="text-xs sm:text-sm text-slate-400">
            Target Role: <span className="text-slate-200 font-medium">{targetRole || "Software Engineer"}</span> &bull; {match.experience_level_match}
          </p>
        </div>

        {/* Download Report Button */}
        <button
          type="button"
          onClick={onDownloadReport}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold text-xs sm:text-sm shadow-lg shadow-blue-500/20 transition self-start sm:self-auto cursor-pointer"
        >
          <Download className="w-4 h-4" />
          <span>Download Candidate Report PDF</span>
        </button>
      </div>

      {/* Main Metric Gauges Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 my-6 items-center">
        
        {/* Radial Overall Score */}
        <div className="flex flex-col items-center justify-center p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
          <div className="relative w-36 h-36 flex items-center justify-center">
            <svg className="w-full h-full -rotate-90" viewBox="0 0 160 160">
              <circle
                cx="80"
                cy="80"
                r={radius}
                stroke="#1e293b"
                strokeWidth="12"
                fill="transparent"
              />
              <circle
                cx="80"
                cy="80"
                r={radius}
                stroke={getScoreStroke(overall)}
                strokeWidth="12"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                fill="transparent"
                style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
              />
            </svg>
            <div className="absolute text-center">
              <span className="text-3xl font-extrabold text-white">{overall}%</span>
              <p className="text-[10px] uppercase tracking-wider text-slate-400 font-medium">Overall Match</p>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-2 text-center">Weighted Composite Score</p>
        </div>

        {/* Sub-Metric 1: Semantic Similarity */}
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 flex flex-col justify-between h-full">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="flex items-center gap-1.5 font-medium">
                <Target className="w-4 h-4 text-blue-400" />
                Semantic Similarity
              </span>
              <span className="font-mono text-blue-400 font-bold">{semantic}%</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-600 to-blue-400 rounded-full transition-all duration-700"
                style={{ width: `${semantic}%` }}
              />
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-3">
            Computed via <b>all-MiniLM-L6-v2</b> 384-dimensional dense embeddings and cosine distance.
          </p>
        </div>

        {/* Sub-Metric 2: Keyword Match */}
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 flex flex-col justify-between h-full">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="flex items-center gap-1.5 font-medium">
                <Award className="w-4 h-4 text-cyan-400" />
                Keyword Match
              </span>
              <span className="font-mono text-cyan-400 font-bold">{keyword}%</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-cyan-600 to-cyan-400 rounded-full transition-all duration-700"
                style={{ width: `${keyword}%` }}
              />
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-3">
            Direct overlap of required technical skills & frameworks extracted from job description.
          </p>
        </div>

        {/* Sub-Metric 3: ATS Score */}
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 flex flex-col justify-between h-full">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="flex items-center gap-1.5 font-medium">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                ATS Compatibility
              </span>
              <span className="font-mono text-emerald-400 font-bold">{ats}/100</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 rounded-full transition-all duration-700"
                style={{ width: `${ats}%` }}
              />
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-3">
            Evaluated on contact info, length, quantified achievements (%), and action verb impact.
          </p>
        </div>

      </div>

      {/* Summary Verdict Callout */}
      <div className="p-4 rounded-xl bg-blue-950/30 border border-blue-500/20 text-xs sm:text-sm text-slate-300 flex items-start gap-3">
        <div className="mt-0.5 text-blue-400 shrink-0">
          <Zap className="w-4 h-4" />
        </div>
        <div>
          <p className="font-semibold text-blue-300">Executive Evaluation Verdict:</p>
          <p className="mt-0.5 text-slate-300">{match.summary_verdict}</p>
        </div>
      </div>

    </div>
  );
}
