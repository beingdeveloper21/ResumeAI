import React, { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, Copy, Check, Terminal, Brain, MessageSquare, Award } from 'lucide-react';

export default function InterviewPrepHub({ questions }) {
  const [expandedIndices, setExpandedIndices] = useState([0]); // Open first by default
  const [copiedIndex, setCopiedIndex] = useState(null);

  const toggleExpand = (idx) => {
    setExpandedIndices((prev) =>
      prev.includes(idx) ? prev.filter((i) => i !== idx) : [...prev, idx]
    );
  };

  const handleCopyAnswer = (answerText, idx) => {
    navigator.clipboard.writeText(answerText);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const getTypeIcon = (type) => {
    if (type?.toLowerCase().includes('system')) return <Terminal className="w-4 h-4 text-purple-400" />;
    if (type?.toLowerCase().includes('behavioral')) return <MessageSquare className="w-4 h-4 text-amber-400" />;
    return <Brain className="w-4 h-4 text-cyan-400" />;
  };

  const getTypeBadge = (type) => {
    if (type?.toLowerCase().includes('system')) return 'bg-purple-950/40 text-purple-300 border-purple-500/30';
    if (type?.toLowerCase().includes('behavioral')) return 'bg-amber-950/40 text-amber-300 border-amber-500/30';
    return 'bg-cyan-950/40 text-cyan-300 border-cyan-500/30';
  };

  const getDifficultyBadge = (diff) => {
    if (diff?.toLowerCase() === 'hard') return 'bg-rose-950/40 text-rose-300 border-rose-500/30';
    if (diff?.toLowerCase() === 'medium') return 'bg-blue-950/40 text-blue-300 border-blue-500/30';
    return 'bg-emerald-950/40 text-emerald-300 border-emerald-500/30';
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
      
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-indigo-400" />
          <h3 className="text-base sm:text-lg font-bold text-white">AI Technical Interview Preparation Hub</h3>
        </div>
        <p className="text-xs text-slate-400 mt-0.5">
          Custom interview questions tailored to your exact resume skills, target role gaps, and real-world system design tradeoffs.
        </p>
      </div>

      {/* Questions List */}
      <div className="space-y-3.5">
        {questions && questions.map((q, idx) => {
          const isExpanded = expandedIndices.includes(idx);

          return (
            <div
              key={idx}
              className="rounded-xl border border-slate-800 bg-slate-950/70 overflow-hidden transition"
            >
              {/* Question Clickable Header */}
              <div
                onClick={() => toggleExpand(idx)}
                className="p-4 flex items-start justify-between gap-4 cursor-pointer hover:bg-slate-900/40 transition select-none"
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 shrink-0">
                    {getTypeIcon(q.type)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${getTypeBadge(q.type)}`}>
                        {q.type}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${getDifficultyBadge(q.difficulty)}`}>
                        {q.difficulty}
                      </span>
                      <span className="text-[10px] text-slate-500">Question {idx + 1}</span>
                    </div>
                    <h4 className="text-xs sm:text-sm font-semibold text-slate-100 leading-snug">
                      {q.question}
                    </h4>
                  </div>
                </div>

                <div className="text-slate-400 hover:text-white mt-1 shrink-0">
                  {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </div>
              </div>

              {/* Expandable Content */}
              {isExpanded && (
                <div className="px-4 pb-4 pt-1 border-t border-slate-800/80 bg-slate-950/40 space-y-3 text-xs">
                  
                  {/* Why Asked */}
                  <div className="p-3 rounded-lg bg-slate-900/50 border border-slate-800">
                    <span className="font-semibold text-slate-300 block mb-0.5">Why Recruiters Ask This:</span>
                    <p className="text-slate-400 italic">{q.why_asked}</p>
                  </div>

                  {/* Key Talking Points */}
                  {q.key_talking_points && q.key_talking_points.length > 0 && (
                    <div>
                      <span className="font-semibold text-slate-300 block mb-1">Key Talking Points to Hit:</span>
                      <ul className="space-y-1">
                        {q.key_talking_points.map((pt, pIdx) => (
                          <li key={pIdx} className="text-slate-400 flex items-start gap-2">
                            <span className="text-indigo-400 font-bold">&bull;</span>
                            <span>{pt}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Suggested Model Answer */}
                  <div className="p-3.5 rounded-lg bg-indigo-950/20 border border-indigo-500/30 relative">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-indigo-300 flex items-center gap-1.5">
                        <Award className="w-3.5 h-3.5 text-indigo-400" />
                        Suggested Model Answer Framework:
                      </span>
                      <button
                        type="button"
                        onClick={() => handleCopyAnswer(q.suggested_answer, idx)}
                        className="text-slate-400 hover:text-white p-1 rounded transition"
                        title="Copy Answer"
                      >
                        {copiedIndex === idx ? (
                          <span className="text-[10px] text-emerald-400 flex items-center gap-1 font-mono">
                            <Check className="w-3 h-3" /> Copied
                          </span>
                        ) : (
                          <Copy className="w-3.5 h-3.5" />
                        )}
                      </button>
                    </div>
                    <p className="text-slate-300 leading-relaxed font-sans">{q.suggested_answer}</p>
                  </div>

                </div>
              )}

            </div>
          );
        })}
      </div>

    </div>
  );
}
