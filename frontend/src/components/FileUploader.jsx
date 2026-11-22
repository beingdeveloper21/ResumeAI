import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle2, X, Sparkles, AlertCircle } from 'lucide-react';

export default function FileUploader({
  file,
  setFile,
  resumeText,
  setResumeText,
  onLoadSampleResume
}) {
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'paste'
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  };

  const handleFileSelected = (selectedFile) => {
    if (!selectedFile.name.toLowerCase().endsWith('.pdf') && !selectedFile.name.toLowerCase().endsWith('.txt')) {
      alert("Please upload a PDF (.pdf) or text (.txt) file.");
      return;
    }
    setFile(selectedFile);
  };

  const handleRemoveFile = () => {
    setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl">
      
      {/* Header and Mode Tabs */}
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-blue-400" />
          <h2 className="font-semibold text-slate-100 text-sm sm:text-base">1. Candidate Resume</h2>
        </div>

        <div className="flex rounded-lg bg-slate-950 p-1 border border-slate-800 text-xs">
          <button
            type="button"
            onClick={() => setActiveTab('upload')}
            className={`px-3 py-1 rounded-md transition font-medium ${
              activeTab === 'upload' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Upload PDF
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('paste')}
            className={`px-3 py-1 rounded-md transition font-medium ${
              activeTab === 'paste' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Paste Text
          </button>
        </div>
      </div>

      {/* Tab: Upload File */}
      {activeTab === 'upload' && (
        <div>
          {!file ? (
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition flex flex-col items-center justify-center ${
                isDragging
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-slate-800 hover:border-slate-700 bg-slate-950/50 hover:bg-slate-950/80'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.txt"
                onChange={handleFileChange}
                className="hidden"
              />
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-3 text-blue-400">
                <Upload className="w-6 h-6" />
              </div>
              <p className="text-sm font-medium text-slate-200">
                Drag and drop your PDF resume here, or <span className="text-blue-400 underline">browse</span>
              </p>
              <p className="text-xs text-slate-500 mt-1">Supports PDF (PyPDF / PyMuPDF fallback) up to 15MB</p>
            </div>
          ) : (
            <div className="rounded-xl border border-blue-500/30 bg-blue-950/20 p-4 flex items-center justify-between">
              <div className="flex items-center gap-3 truncate">
                <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                  <FileText className="w-5 h-5" />
                </div>
                <div className="truncate">
                  <p className="text-sm font-semibold text-slate-100 truncate">{file.name}</p>
                  <p className="text-xs text-slate-400">{(file.size / 1024).toFixed(1)} KB &bull; Ready for NLP Analysis</p>
                </div>
              </div>
              <button
                type="button"
                onClick={handleRemoveFile}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition"
                title="Remove uploaded file"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Quick 1-Click Sample Resume Loader */}
          <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
            <span>Don't have a PDF ready?</span>
            <button
              type="button"
              onClick={onLoadSampleResume}
              className="inline-flex items-center gap-1.5 text-blue-400 hover:text-blue-300 font-medium hover:underline transition"
            >
              <Sparkles className="w-3.5 h-3.5" />
              Load Sample Software Engineer Resume
            </button>
          </div>
        </div>
      )}

      {/* Tab: Paste Text */}
      {activeTab === 'paste' && (
        <div>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste raw resume text here including skills, experience, and contact details..."
            rows={7}
            className="w-full rounded-xl bg-slate-950 border border-slate-800 p-3 text-xs sm:text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition resize-none font-mono"
          />
          <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
            <span>{resumeText.trim().split(/\s+/).filter(Boolean).length} words</span>
            <button
              type="button"
              onClick={() => setResumeText("")}
              className="text-slate-400 hover:text-slate-200"
            >
              Clear
            </button>
          </div>
        </div>
      )}

    </div>
  );
}
