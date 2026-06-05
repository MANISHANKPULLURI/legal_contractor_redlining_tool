"use client";

import { useState } from "react";
import RiskCard from "@/components/RiskCard";
import { 
  Gavel, 
  UploadCloud, 
  Zap, 
  Bot, 
  Send, 
  AlertTriangle, 
  FileWarning, 
  CheckCircle2, 
  Sparkles, 
  FileText
} from "lucide-react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState<any>(null);
  const [file, setFile] = useState<File | null>(null);
  const [review, setReview] = useState<any>(null);
  const [reviewQuery, setReviewQuery] = useState("");
  const [redlineFile, setRedlineFile] = useState("");
  const [selected, setSelected] = useState<any>(null);
  const [chat, setChat] = useState<any[]>([]);

  // ======================
  // LEGAL CHAT
  // ======================
  async function sendMessage() {
    if (!message.trim()) return;

    setChat(prev => [
      ...prev,
      {
        role: "user",
        text: message
      }
    ]);

    const response = await fetch(
      "http://127.0.0.1:8000/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: message
        })
      }
    );

    const data = await response.json();

    let finalAnswer =
      typeof data.answer === "string"
        ? data.answer
        : JSON.stringify(data.answer, null, 2);

    setAnswer(finalAnswer);

    setChat(prev => [
      ...prev,
      {
        role: "assistant",
        text: finalAnswer
      }
    ]);

    setMessage("");
  }

  // ======================
  // CONTRACT REVIEW
  // ======================
  async function uploadContract() {
    if (!file) {
      alert("Please upload contract");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("query", reviewQuery || "Review this contract");

    const response = await fetch(
      "http://127.0.0.1:8000/review",
      {
        method: "POST",
        body: formData
      }
    );

    const data = await response.json();

    setReview(data.review);
    setRedlineFile(data.redline_file);

    if (data.review?.risks?.length > 0) {
      setSelected(data.review.risks[0]);
    }
  }

  function downloadRedline() {
    window.open(
      `http://127.0.0.1:8000/download/${redlineFile}`,
      "_blank"
    );
  }

  const risks = review?.risks || [];

  const count = (type: string) =>
    risks.filter((x: any) => x.analysis?.risk_level === type).length;

  return (
    <div className="h-screen w-screen grid grid-cols-[340px_1fr_400px] bg-[#fbfaee] text-[#1b1c15] overflow-hidden relative selection:bg-[#secondary-fixed]">
      
      {/* ================= LEFT SIDEBAR PANEL ================= */}
      <aside className="bg-[#f5f4e8] border-r border-neutral-300/40 z-40 flex flex-col overflow-hidden h-full">
        <div className="p-6 flex flex-col h-full gap-6 overflow-y-auto custom-scrollbar">
          
          {/* Brand Header */}
          <div className="flex items-center gap-3 shrink-0">
            <div className="w-10 h-10 bg-[#1b1c15] flex items-center justify-center rounded-xl shadow-sm">
              <Gavel className="text-[#fbfaee] w-5 h-5" />
            </div>
            <div>
              <h1 className="font-serif-legal text-xl font-bold tracking-tight text-[#1b1c15]">LegalContractor AI</h1>
              <p className="text-[10px] font-bold uppercase tracking-widest text-neutral-500">Agentic Intelligence</p>
            </div>
          </div>

          {/* Action Area */}
          <div className="flex flex-col gap-5 shrink-0">
            <label className="group relative flex flex-col items-center justify-center border-2 border-dashed border-neutral-300 rounded-2xl p-6 bg-[#efeee3] hover:bg-[#e9e9dd] transition-all cursor-pointer">
              <input
                type="file"
                hidden
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              <UploadCloud className="text-[#745853] w-8 h-8 mb-2 transition-transform group-hover:scale-105" />
              <p className="font-bold text-sm text-[#1b1c15] text-center">Upload Contract</p>
              <p className="text-xs text-neutral-400 text-center mt-0.5">PDF or DOCX (Max 25MB)</p>
              {file && (
                <p className="text-emerald-700 font-bold mt-3 text-xs bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200 text-center max-w-full truncate">
                  ✓ {file.name}
                </p>
              )}
            </label>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-neutral-500 ml-1">Review Instructions</label>
              <textarea
                className="w-full h-24 p-3 bg-[#fbfaee] border border-neutral-300 rounded-xl text-sm focus:ring-1 focus:ring-[#745853]/40 focus:border-[#745853] transition-all resize-none outline-none text-[#1b1c15]"
                placeholder="e.g., Review liability clauses for indemnification caps"
                value={reviewQuery}
                onChange={(e) => setReviewQuery(e.target.value)}
              />
            </div>

            <button
              onClick={uploadContract}
              className="w-full bg-[#745853] text-[#ffffff] py-3.5 px-4 rounded-xl font-bold text-sm flex items-center justify-center gap-2 hover:opacity-95 active:scale-[0.98] transition-all shadow-md"
            >
              <Zap className="w-4 h-4 text-[#ffffff] fill-current" />
              Analyze Contract
            </button>
          </div>

          {/* AI Chat Assistant Workspace */}
          <div className="flex-1 flex flex-col bg-[#fbfaee] border border-neutral-300/60 rounded-2xl overflow-hidden shadow-sm min-h-[220px]">
            <div className="p-4 border-b border-neutral-200 flex items-center gap-2 bg-[#efeee3]/40 shrink-0">
              <Bot className="w-4 h-4 text-[#745853]" />
              <span className="text-xs font-bold uppercase tracking-wider text-[#1b1c15]">Legal Assistant</span>
            </div>

            {/* Chat History View */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-4">
              {chat.length === 0 ? (
                <div className="h-full flex items-center justify-center text-center p-4">
                  <p className="text-xs text-neutral-400 italic">Ask Lexo anything about the contract!</p>
                </div>
              ) : (
                chat.map((c, i) => (
                  <div key={i} className="flex flex-col gap-1.5">
                    <p className="text-[10px] font-bold text-neutral-400 uppercase ml-1">
                      {c.role === "user" ? "You" : "AI Assistant"}
                    </p>
                    <div className={`p-3.5 rounded-2xl text-xs leading-relaxed border ${
                      c.role === "user" 
                        ? "bg-[#745853]/5 border-[#745853]/10 rounded-tr-none ml-4" 
                        : "bg-[#f5f4e8] border-neutral-200/50 rounded-tl-none mr-4"
                    }`}>
                      <span className="whitespace-pre-wrap">{c.text}</span>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Chat Interactive Area */}
            <div className="p-3 bg-[#f5f4e8] border-t border-neutral-200/60 shrink-0">
              <div className="relative flex items-center">
                <input
                  className="w-full pl-4 pr-10 py-2.5 bg-[#fbfaee] border border-neutral-300 rounded-xl text-xs focus:outline-none focus:ring-1 focus:ring-[#745853]/40"
                  placeholder="Ask a legal question..."
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                />
                <button 
                  onClick={sendMessage}
                  className="absolute right-3 text-[#745853] hover:scale-105 transition-transform"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

        </div>
      </aside>

      {/* ================= CENTER MAIN WORKSPACE ================= */}
      <main className="flex flex-col overflow-hidden relative h-full">
        
        {/* Sticky App Bar Header */}
        <header className="h-20 flex items-center justify-between px-10 bg-[#fbfaee]/95 border-b border-neutral-300/30 sticky top-0 z-30 shrink-0">
          <div className="flex items-center gap-6">
            <h2 className="font-serif-legal text-2xl font-bold text-[#1b1c15]">Contract Risk Dashboard</h2>
            {file && (
              <div className="px-4 py-1.5 bg-[#e4e3d7] rounded-full text-xs font-medium text-neutral-700 flex items-center gap-2">
                <span className="w-2 h-2 bg-emerald-600 rounded-full animate-pulse"></span>
                {file.name}
              </div>
            )}
          </div>
          {/* Removed the "Review Workspace Active" badge here to clean up the header */}
        </header>

        {/* Scrollable Feed Container */}
        <div className="flex-1 overflow-y-auto p-10 custom-scrollbar bg-[#fbfaee]/30 flex flex-col pb-32">
          
          {/* Risk Metrics Cards Panel */}
          <div className="grid grid-cols-3 gap-8 mb-12 shrink-0">
            
            {/* High Severity Panel Card */}
            <div className="bg-[#fbfaee] p-7 rounded-2xl border border-neutral-300/50 shadow-sm flex items-center justify-between group hover:shadow-md transition-all">
              <div>
                <p className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-2">High Risk</p>
                <h3 className="font-serif-legal text-4xl text-[#ba1a1a] font-bold">{count("HIGH")}</h3>
              </div>
              <div className="w-14 h-14 rounded-full bg-[#ffdad4]/40 flex items-center justify-center text-[#ba1a1a]">
                <FileWarning className="w-7 h-7 fill-current" />
              </div>
            </div>

            {/* Medium Severity Panel Card */}
            <div className="bg-[#fbfaee] p-7 rounded-2xl border border-neutral-300/50 shadow-sm flex items-center justify-between group hover:shadow-md transition-all">
              <div>
                <p className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-2">Medium Risk</p>
                <h3 className="font-serif-legal text-4xl text-[#745853] font-bold">{count("MEDIUM")}</h3>
              </div>
              <div className="w-14 h-14 rounded-full bg-[#fed7d0]/40 flex items-center justify-center text-[#745853]">
                <AlertTriangle className="w-7 h-7 fill-current" />
              </div>
            </div>

            {/* Low Severity Panel Card */}
            <div className="bg-[#fbfaee] p-7 rounded-2xl border border-neutral-300/50 shadow-sm flex items-center justify-between group hover:shadow-md transition-all">
              <div>
                <p className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-2">Low Risk</p>
                <h3 className="font-serif-legal text-4xl text-emerald-700 font-bold">{count("LOW")}</h3>
              </div>
              <div className="w-14 h-14 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-700">
                <CheckCircle2 className="w-7 h-7 fill-current" />
              </div>
            </div>

          </div>

          {/* Key Findings Feed Section */}
          <div className="flex flex-col gap-6">
            <h4 className="text-xs font-bold text-neutral-400 uppercase tracking-[0.2em] ml-1">Key Findings</h4>
            
            {risks.length > 0 ? (
              <div className="space-y-6">
                {risks.map((item: any) => (
                  <RiskCard
                    key={item.clause_number}
                    item={item}
                    isSelected={selected?.clause_number === item.clause_number}
                    onClick={() => setSelected(item)}
                  />
                ))}
              </div>
            ) : (
              <div className="border-2 border-dashed border-neutral-300/50 rounded-2xl p-16 text-center bg-white/40">
                <p className="text-neutral-400 text-sm">No contract reviewed yet. Upload a contract to view structural findings.</p>
              </div>
            )}
          </div>

        </div>
      </main>

      {/* ================= RIGHT REDLINE IMPROVEMENT SIDEBAR ================= */}
      <aside className="bg-[#fbfaee] border-l border-neutral-300/50 z-40 flex flex-col overflow-hidden h-full">
        
        {/* Sidebar Header Block */}
        <div className="p-8 border-b border-neutral-300/30 bg-[#f5f4e8]/50 shrink-0">
          <h3 className="font-serif-legal text-xl font-bold text-[#1b1c15] flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-[#745853]" />
            AI Redline
          </h3>
          <p className="text-xs font-medium text-neutral-500 mt-1">Clause-by-clause intelligent optimization</p>
        </div>

        {/* Dynamic scroll containers to absorb extra text cleanly without pushing container bounds */}
        <div className="flex-1 overflow-y-auto p-8 flex flex-col gap-6 custom-scrollbar pb-32 justify-start">
          {selected ? (
            <>
              {/* Active Diff Split Workspace Layout */}
              <div className="flex flex-col gap-3 flex-1 min-h-[260px]">
                <div className="flex items-center justify-between px-1">
                  <h4 className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest">Active Comparison</h4>
                  <span className="text-[#745853] font-bold text-[10px] uppercase tracking-wide">Diff View Active</span>
                </div>
                
                <div className="rounded-2xl overflow-hidden border border-neutral-300/50 shadow-sm bg-white flex flex-col h-full min-h-[240px]">
                  {/* Scrollable Current Original Clause Box */}
                  <div className="p-5 bg-[#ba1a1a]/5 border-b border-neutral-200/50 max-h-[160px] overflow-y-auto custom-scrollbar">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 rounded-full bg-[#ba1a1a]"></span>
                      <span className="text-[10px] font-bold text-neutral-500 uppercase">Current Clause</span>
                    </div>
                    <p className="text-xs text-neutral-600 italic leading-relaxed">
                      "{selected.clause}"
                    </p>
                  </div>

                  {/* Scrollable Proposed AI Revision Box */}
                  <div className="p-5 bg-emerald-50/40 flex-1 max-h-[160px] overflow-y-auto custom-scrollbar">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
                      <span className="text-[10px] font-bold text-[#1b1c15] uppercase">Proposed Revision</span>
                    </div>
                    <p className="text-xs text-[#1b1c15] leading-relaxed">
                      {selected.analysis?.rewritten_clause || "No revision generated for this risk context."}
                    </p>
                  </div>
                </div>
              </div>

              {/* Scrollable Final Preview Workspace Panel */}
              <div className="flex flex-col gap-3 flex-1 min-h-[180px]">
                <h4 className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest px-1">Final Clause Preview</h4>
                <div className="p-5 bg-[#f5f4e8] rounded-2xl border border-neutral-300/50 max-h-[160px] overflow-y-auto custom-scrollbar">
                  <p className="text-xs text-[#1b1c15] leading-relaxed">
                    {selected.analysis?.rewritten_clause || selected.clause}
                  </p>
                </div>
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center p-6 my-auto">
              <FileText className="w-8 h-8 text-neutral-300 mb-2" />
              <p className="text-xs text-neutral-400">Analyze contract and choose findings to view targeted optimization redlines.</p>
            </div>
          )}
        </div>
      </aside>

      {/* ================= FIXED BOTTOM OVERLAY ACTION BAR ================= */}
      {/* Changed justify-between to justify-end since we removed the left-side elements */}
      <footer className="fixed bottom-0 right-0 h-20 bg-[#fbfaee]/95 border-t border-neutral-300/40 px-10 flex items-center justify-end z-50 left-[340px]">
        <button
          onClick={downloadRedline}
          disabled={!redlineFile}
          className="bg-[#745853] text-[#ffffff] px-8 py-3.5 rounded-xl font-bold text-sm flex items-center gap-2.5 shadow-lg hover:translate-y-[-1px] active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none transition-all"
        >
          <FileText className="w-4 h-4" />
          Download Redlined Contract
        </button>
      </footer>

    </div>
  );
}