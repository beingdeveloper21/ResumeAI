import React, { useState } from 'react';
import { CheckCircle2, AlertTriangle, Key, Search, Layers } from 'lucide-react';

export default function SkillsBreakdown({ match, resume }) {
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const categories = [
    { id: 'all', label: 'All Items' },
    { id: 'Language', label: 'Languages' },
    { id: 'Framework/Lib', label: 'Frameworks' },
    { id: 'Cloud/DB/DevOps', label: 'Cloud & DB' },
    { id: 'AI/ML/Data', label: 'AI & Data' },
    { id: 'Tool/Platform', label: 'Tools' },
  ];

  const filteredSkills = (match.skills_breakdown || []).filter((item) => {
    const matchesCategory = activeCategory === 'all' || item.category === activeCategory;
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-5">
        <div>
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base sm:text-lg font-bold text-white">Skills & Competency Matrix</h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Automated alignment of extracted candidate skills against target job requirements.
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search skills..."
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition"
          />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-1.5 flex-wrap mb-5">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`px-3 py-1 rounded-lg text-xs font-medium transition ${
              activeCategory === cat.id
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-slate-950 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Skills Badges Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        {/* Matched Skills */}
        <div className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/20">
          <div className="flex items-center justify-between mb-3">
            <span className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 uppercase tracking-wider">
              <CheckCircle2 className="w-4 h-4" />
              Matched Skills ({match.matched_skills?.length || 0})
            </span>
            <span className="text-[11px] text-slate-400">Present in Resume</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {match.matched_skills && match.matched_skills.length > 0 ? (
              match.matched_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-950/40 text-emerald-300 border border-emerald-500/30 flex items-center gap-1"
                >
                  <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                  {skill}
                </span>
              ))
            ) : (
              <p className="text-xs text-slate-500 italic">No direct matching skills detected.</p>
            )}
          </div>
        </div>

        {/* Missing / Gap Skills */}
        <div className="p-4 rounded-xl bg-slate-950/60 border border-rose-500/20">
          <div className="flex items-center justify-between mb-3">
            <span className="flex items-center gap-1.5 text-xs font-bold text-rose-400 uppercase tracking-wider">
              <AlertTriangle className="w-4 h-4" />
              Missing / Gap Skills ({match.missing_skills?.length || 0})
            </span>
            <span className="text-[11px] text-slate-400">Required by Role</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {match.missing_skills && match.missing_skills.length > 0 ? (
              match.missing_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="px-2.5 py-1 rounded-md text-xs font-medium bg-rose-950/40 text-rose-300 border border-rose-500/30 flex items-center gap-1"
                >
                  <AlertTriangle className="w-3 h-3 text-rose-400" />
                  {skill}
                </span>
              ))
            ) : (
              <p className="text-xs text-emerald-400 italic">Zero required skill gaps! Outstanding match.</p>
            )}
          </div>
        </div>

      </div>

      {/* Critical Keywords Box */}
      {match.critical_missing_keywords && match.critical_missing_keywords.length > 0 && (
        <div className="mt-4 p-4 rounded-xl bg-slate-950/60 border border-amber-500/20">
          <div className="flex items-center gap-1.5 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">
            <Key className="w-4 h-4" />
            Critical Job Description Keywords to Add
          </div>
          <p className="text-xs text-slate-400 mb-3">
            Incorporating these terms naturally into your bullet points will maximize ATS lexical score:
          </p>
          <div className="flex flex-wrap gap-2">
            {match.critical_missing_keywords.map((kw, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 rounded text-xs font-mono bg-amber-950/30 text-amber-300 border border-amber-500/20"
              >
                +{kw}
              </span>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
