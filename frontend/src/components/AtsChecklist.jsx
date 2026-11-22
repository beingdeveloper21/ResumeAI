import React from 'react';
import { ShieldCheck, CheckCircle2, AlertCircle, AlertTriangle } from 'lucide-react';

export default function AtsChecklist({ checks, atsScore }) {
  const getStatusBadge = (check) => {
    if (check.passed) {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-950/50 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
          Pass
        </span>
      );
    }
    if (check.impact === 'High') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-950/50 text-rose-300 border border-rose-500/30 flex items-center gap-1">
          <AlertCircle className="w-3 h-3 text-rose-400" />
          Needs Attention
        </span>
      );
    }
    return (
      <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-950/50 text-amber-300 border border-amber-500/30 flex items-center gap-1">
        <AlertTriangle className="w-3 h-3 text-amber-400" />
        Warning
      </span>
    );
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <h3 className="text-base sm:text-lg font-bold text-white">ATS Parsing & Compliance Audit</h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Deterministic check simulating enterprise Applicant Tracking System filters (Workday, Greenhouse, Lever).
          </p>
        </div>

        <div className="text-right">
          <span className="text-2xl font-extrabold text-emerald-400">{atsScore}</span>
          <span className="text-xs text-slate-400">/100</span>
        </div>
      </div>

      {/* Checks List */}
      <div className="space-y-3">
        {checks && checks.map((c, idx) => (
          <div
            key={idx}
            className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
          >
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs sm:text-sm font-semibold text-slate-200">{c.check_name}</span>
                <span className="text-[10px] text-slate-500 font-mono">Impact: {c.impact}</span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">{c.details}</p>
            </div>

            <div className="shrink-0">
              {getStatusBadge(c)}
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
