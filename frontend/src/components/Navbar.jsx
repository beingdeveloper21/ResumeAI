import React from 'react';
import { Sparkles, FileText, Cpu, Github, Download, CheckCircle2 } from 'lucide-react';

export default function Navbar({ onOpenArchitecture, onDownloadGuide, isBackendHealthy }) {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 p-[1px] shadow-lg shadow-blue-500/20">
            <div className="h-full w-full bg-slate-950 rounded-xl flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-blue-400 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                ResumeAI
              </span>
              <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wider uppercase rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                v1.0 Production
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">AI-Powered Resume Analyzer & Job Matcher</p>
          </div>
        </div>

        {/* Status Pill & Actions */}
        <div className="flex items-center gap-3">
          {/* Engine Status */}
          <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs">
            <span className={`w-2 h-2 rounded-full ${isBackendHealthy ? 'bg-emerald-400 shadow-sm shadow-emerald-400' : 'bg-amber-400 animate-ping'}`} />
            <span className="text-slate-300">
              {isBackendHealthy ? 'FastAPI + MiniLM Active' : 'Connecting to Engine...'}
            </span>
          </div>

          {/* Architecture Modal Button */}
          <button
            onClick={onOpenArchitecture}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 hover:border-slate-700 transition"
            title="Inspect System Architecture, Stack Justification & Data Pipeline"
          >
            <Cpu className="w-3.5 h-3.5 text-blue-400" />
            <span className="hidden sm:inline">System Architecture</span>
          </button>

          {/* Master Guide PDF */}
          <button
            onClick={onDownloadGuide}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/30 hover:border-blue-500/50 transition"
            title="Download Master Architecture & Interview Preparation PDF"
          >
            <Download className="w-3.5 h-3.5 text-blue-400" />
            <span className="hidden sm:inline">Master Guide PDF</span>
          </button>

          {/* GitHub Repo */}
          <a
            href="https://github.com/beingdeveloper21/ResumeAI"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 rounded-lg text-slate-400 hover:text-white bg-slate-900 hover:bg-slate-800 border border-slate-800 transition"
            title="View Source on GitHub"
          >
            <Github className="w-4 h-4" />
          </a>
        </div>

      </div>
    </header>
  );
}
