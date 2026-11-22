import React from 'react';
import { Sparkles, ArrowRight, CheckCircle2, TrendingUp, Zap, HelpCircle } from 'lucide-react';

export default function SuggestionsSection({ feedback }) {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
      
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-blue-400" />
          <h3 className="text-base sm:text-lg font-bold text-white">LLM Resume Optimization & Bullet Rewrites</h3>
        </div>
        <p className="text-xs text-slate-400 mt-0.5">
          Actionable bullet-point transformations engineered using Google's XYZ formula to convert passive duties into quantified achievements.
        </p>
      </div>

      {/* Bullet Point Rewrites */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-blue-400 mb-3 flex items-center gap-1.5">
          <TrendingUp className="w-4 h-4" />
          High-Impact Bullet Transformations (Google XYZ Formula)
        </h4>

        <div className="space-y-4">
          {feedback.bullet_improvements && feedback.bullet_improvements.map((b, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-slate-950/70 border border-slate-800">
              
              {/* Before */}
              <div className="mb-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Original Passive Phrasing:</span>
                <p className="text-xs text-slate-400 line-through mt-0.5 italic">"{b.original}"</p>
              </div>

              {/* After */}
              <div className="p-3 rounded-lg bg-blue-950/30 border border-blue-500/30 mb-2">
                <span className="text-[10px] font-bold uppercase tracking-wider text-blue-400 flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  Optimized Achievement Rewrite:
                </span>
                <p className="text-xs sm:text-sm font-medium text-slate-100 mt-1">"{b.improved}"</p>
              </div>

              {/* Rationale */}
              <div className="flex items-start gap-1.5 text-[11px] text-slate-400">
                <HelpCircle className="w-3.5 h-3.5 text-blue-400 shrink-0 mt-0.5" />
                <span><b>Why this works:</b> {b.rationale}</span>
              </div>

            </div>
          ))}
        </div>
      </div>

      {/* Strengths & Priority Improvements Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
        
        {/* Strengths */}
        <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
          <h5 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            Candidate Core Strengths
          </h5>
          <ul className="space-y-2">
            {feedback.key_strengths && feedback.key_strengths.map((str, idx) => (
              <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0 mt-1.5" />
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Priority Improvements */}
        <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
          <h5 className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-3 flex items-center gap-1.5">
            <Zap className="w-4 h-4" />
            Targeted Resume Enhancements
          </h5>
          <ul className="space-y-2">
            {feedback.key_improvements && feedback.key_improvements.map((imp, idx) => (
              <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0 mt-1.5" />
                <span>{imp}</span>
              </li>
            ))}
          </ul>
        </div>

      </div>

      {/* Action Verbs Bar */}
      {feedback.action_verbs_recommended && feedback.action_verbs_recommended.length > 0 && (
        <div className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
          <span className="font-semibold text-slate-300">Recommended Power Action Verbs:</span>
          <div className="flex flex-wrap gap-1.5">
            {feedback.action_verbs_recommended.map((verb, idx) => (
              <span key={idx} className="px-2 py-0.5 rounded bg-blue-950/40 text-blue-300 border border-blue-500/20 font-medium">
                {verb}
              </span>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
