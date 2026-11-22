import React from 'react';
import { Briefcase, Play, Sparkles, Loader2 } from 'lucide-react';

export default function JobDescriptionInput({
  jobDescription,
  setJobDescription,
  targetRole,
  setTargetRole,
  presets,
  onSelectPreset,
  onAnalyze,
  isLoading
}) {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
      
      <div>
        {/* Header and Preset Pills */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-cyan-400" />
            <h2 className="font-semibold text-slate-100 text-sm sm:text-base">2. Target Job Description</h2>
          </div>

          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-[11px] text-slate-400 font-medium">Presets:</span>
            {presets && presets.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => onSelectPreset(preset)}
                className="px-2.5 py-0.5 rounded-full bg-slate-800 hover:bg-slate-700 border border-slate-700 text-[11px] text-slate-300 hover:text-white transition"
              >
                {preset.role.split(' ')[0]} {preset.role.split(' ')[1] || ''}
              </button>
            ))}
          </div>
        </div>

        {/* Target Role Input */}
        <div className="mb-3">
          <label className="block text-xs font-medium text-slate-400 mb-1">
            Target Job Title / Role:
          </label>
          <input
            type="text"
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
            placeholder="e.g. Senior Software Engineer"
            className="w-full rounded-xl bg-slate-950 border border-slate-800 px-3.5 py-2 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition"
          />
        </div>

        {/* Job Description Textarea */}
        <div className="mb-4">
          <label className="block text-xs font-medium text-slate-400 mb-1">
            Job Description / Requirements:
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste role requirements, tech stack (FastAPI, React, Python, Docker...), and responsibilities..."
            rows={5}
            className="w-full rounded-xl bg-slate-950 border border-slate-800 p-3 text-xs sm:text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition resize-none font-mono"
          />
        </div>
      </div>

      {/* Action Button */}
      <button
        type="button"
        onClick={onAnalyze}
        disabled={isLoading || !jobDescription.trim()}
        className={`w-full py-3 px-4 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition shadow-lg ${
          isLoading || !jobDescription.trim()
            ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-800'
            : 'bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white shadow-blue-500/25 cursor-pointer transform hover:-translate-y-0.5'
        }`}
      >
        {isLoading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin text-white" />
            <span>Analyzing & Benchmarking...</span>
          </>
        ) : (
          <>
            <Play className="w-4 h-4 fill-white" />
            <span>Benchmark Resume & Generate AI Prep</span>
          </>
        )}
      </button>

    </div>
  );
}
