"use client";

import { useState } from "react";
import RiskCard from "@/components/RiskCard";
import { UploadCloud, Send, FileText } from "lucide-react";

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

    setChat((prev) => [
      ...prev,
      {
        role: "user",
        text: message,
      },
    ]);

    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });

    const data = await response.json();

    let finalAnswer =
      typeof data.answer === "string"
        ? data.answer
        : JSON.stringify(data.answer, null, 2);

    setAnswer(finalAnswer);

    setChat((prev) => [
      ...prev,
      {
        role: "assistant",
        text: finalAnswer,
      },
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

    const response = await fetch("http://127.0.0.1:8000/review", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    setReview(data.review);
    setRedlineFile(data.redline_file);

    if (data.review?.risks?.length > 0) {
      setSelected(data.review.risks[0]);
    }
  }

  function downloadRedline() {
    window.open(`http://127.0.0.1:8000/download/${redlineFile}`, "_blank");
  }

  const risks = review?.risks || [];

  const count = (type: string) =>
    risks.filter((x: any) => x.analysis?.risk_level === type).length;

  return (
    <div className="h-screen w-screen grid grid-cols-[340px_1fr_400px] bg-[#f7f8fb] text-[#1a2d5c] overflow-hidden relative selection:bg-[#1a2d5c]/10">
      {/* ================= LEFT SIDEBAR PANEL ================= */}
      <aside className="bg-white border-r border-slate-200 z-40 flex flex-col overflow-hidden h-full">
        <div className="p-6 flex flex-col h-full gap-6 overflow-y-auto custom-scrollbar">
          {/* Brand Header */}
          <div className="flex items-center gap-3 shrink-0">
            <div className="w-10 h-10 bg-[#1a2d5c] flex items-center justify-center rounded-lg shadow-sm">
              <span className="text-white text-lg font-serif-legal font-bold">
                ⚖
              </span>
            </div>
            <div>
              <h1 className="font-serif-legal text-xl font-bold tracking-tight text-[#1a2d5c]">
                LegalContractor
              </h1>
              <p className="text-[10px] font-bold uppercase tracking-widest text-[#2c3e50]">
                AI Contract Review
              </p>
            </div>
          </div>

          {/* Action Area */}
          <div className="flex flex-col gap-5 shrink-0">
            <label className="group relative flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-xl p-6 bg-slate-50 hover:bg-slate-100 transition-all cursor-pointer">
              <input
                type="file"
                hidden
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              <UploadCloud className="text-[#1a2d5c] w-8 h-8 mb-2 transition-transform group-hover:scale-105" />
              <p className="font-bold text-sm text-[#1a2d5c] text-center">
                Upload Contract
              </p>
              <p className="text-xs text-slate-500 text-center mt-0.5">
                PDF or DOCX (Max 25MB)
              </p>
              {file && (
                <p className="text-[#2d5016] font-bold mt-3 text-xs bg-[#2d5016]/5 px-2.5 py-1 rounded-md border border-[#2d5016]/20 text-center max-w-full truncate">
                  ✓ {file.name}
                </p>
              )}
            </label>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-[#2c3e50] ml-1">
                Review Instructions
              </label>
              <textarea
                className="w-full h-24 p-3 bg-[#f7f8fb] border border-slate-300 rounded-lg text-sm focus:ring-1 focus:ring-[#1a2d5c]/20 focus:border-[#1a2d5c] transition-all resize-none outline-none text-[#1a2d5c]"
                placeholder="e.g., Review liability clauses for indemnification caps"
                value={reviewQuery}
                onChange={(e) => setReviewQuery(e.target.value)}
              />
            </div>

            <button
              onClick={uploadContract}
              className="w-full bg-[#1a2d5c] text-white py-3.5 px-4 rounded-lg font-bold text-sm flex items-center justify-center gap-2 hover:bg-[#0f1f42] active:scale-[0.98] transition-all shadow-md"
            >
              Analyze Contract
            </button>
          </div>

          {/* AI Chat Assistant Workspace */}
          <div className="flex-1 flex flex-col bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm min-h-[220px]">
            <div className="p-4 border-b border-slate-200 flex items-center gap-2 bg-slate-50 shrink-0">
              <span className="text-xs font-bold uppercase tracking-wider text-[#2c3e50]">
                Legal Assistant
              </span>
            </div>

            {/* Chat History View */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-4">
              {chat.length === 0 ? (
                <div className="h-full flex items-center justify-center text-center p-4">
                  <p className="text-xs text-slate-400 italic">
                    Ask a question about the contract
                  </p>
                </div>
              ) : (
                chat.map((c, i) => (
                  <div key={i} className="flex flex-col gap-1.5">
                    <p className="text-[10px] font-bold text-[#2c3e50] uppercase ml-1">
                      {c.role === "user" ? "You" : "Assistant"}
                    </p>
                    <div
                      className={`p-3.5 rounded-lg text-xs leading-relaxed border ${
                        c.role === "user"
                          ? "bg-[#1a2d5c]/5 border-[#1a2d5c]/10 rounded-tr-none ml-4"
                          : "bg-slate-50 border-slate-200 rounded-tl-none mr-4"
                      }`}
                    >
                      <span className="whitespace-pre-wrap">{c.text}</span>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Chat Interactive Area */}
            <div className="p-3 bg-slate-50 border-t border-slate-200 shrink-0">
              <div className="relative flex items-center">
                <input
                  className="w-full pl-4 pr-10 py-2.5 bg-white border border-slate-300 rounded-lg text-xs focus:outline-none focus:ring-1 focus:ring-[#1a2d5c]/20"
                  placeholder="Ask a legal question..."
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                />
                <button
                  onClick={sendMessage}
                  className="absolute right-3 text-[#1a2d5c] hover:scale-105 transition-transform"
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
        <header className="h-20 flex items-center justify-between px-10 bg-white border-b border-slate-200 sticky top-0 z-30 shrink-0">
          <div className="flex items-center gap-6">
            <h2 className="font-serif-legal text-2xl font-bold text-[#1a2d5c]">
              Contract Risk Dashboard
            </h2>
            {file && (
              <div className="px-3 py-2 bg-white border border-slate-300 rounded-lg text-sm text-[#2c3e50] font-medium flex items-center h-fit">
                <span className="inline-block truncate max-w-[250px]">
                  {file.name}
                </span>
              </div>
            )}
          </div>
        </header>

        {/* Scrollable Feed Container */}
        <div className="flex-1 overflow-y-auto p-10 custom-scrollbar bg-[#f7f8fb] flex flex-col pb-32">
          {/* Risk Metrics Cards Panel */}
          <div className="grid grid-cols-3 gap-8 mb-12 shrink-0">
            {/* High Severity Panel Card */}
            <div className="bg-white p-7 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between group hover:shadow-md transition-all">
              <div>
                <p className="text-xs font-bold text-[#2c3e50] uppercase tracking-wider mb-2">
                  High Risk
                </p>
                <h3 className="font-serif-legal text-4xl text-[#c41e3a] font-bold">
                  {count("HIGH")}
                </h3>
              </div>
              <div className="w-14 h-14 rounded-lg bg-[#c41e3a]/5 flex items-center justify-center text-[#c41e3a]">
                <span className="text-2xl">⚠</span>
              </div>
            </div>

            {/* Medium Severity Panel Card */}
            <div className="bg-white p-7 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between group hover:shadow-md transition-all">
              <div>
                <p className="text-xs font-bold text-[#2c3e50] uppercase tracking-wider mb-2">
                  Medium Risk
                </p>
                <h3 className="font-serif-legal text-4xl text-[#e8843a] font-bold">
                  {count("MEDIUM")}
                </h3>
              </div>
              <div className="w-14 h-14 rounded-lg bg-[#e8843a]/5 flex items-center justify-center text-[#e8843a]">
                <span className="text-2xl">◆</span>
              </div>
            </div>

            {/* Low Severity Panel Card */}
            <div className="bg-white p-7 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between group hover:shadow-md transition-all">
              <div>
                <p className="text-xs font-bold text-[#2c3e50] uppercase tracking-wider mb-2">
                  Low Risk
                </p>
                <h3 className="font-serif-legal text-4xl text-[#2d5016] font-bold">
                  {count("LOW")}
                </h3>
              </div>
              <div className="w-14 h-14 rounded-lg bg-[#2d5016]/5 flex items-center justify-center text-[#2d5016]">
                <span className="text-2xl">✓</span>
              </div>
            </div>
          </div>

          {/* Key Findings Feed Section */}
          <div className="flex flex-col gap-6">
            <h4 className="text-xs font-bold text-[#2c3e50] uppercase tracking-[0.2em] ml-1">
              Key Findings
            </h4>

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
              <div className="border-2 border-dashed border-slate-300 rounded-lg p-16 text-center bg-white">
                <p className="text-slate-400 text-sm">
                  No contract reviewed yet. Upload a contract to view structural
                  findings.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* ================= RIGHT REDLINE IMPROVEMENT SIDEBAR ================= */}
      <aside className="bg-white border-l border-slate-200 z-40 flex flex-col overflow-hidden h-full">
        {/* Sidebar Header Block */}
        <div className="p-8 border-b border-slate-200 bg-slate-50 shrink-0">
          <h3 className="font-serif-legal text-xl font-bold text-[#1a2d5c]">
            AI Redline
          </h3>
          <p className="text-xs font-medium text-[#2c3e50] mt-1">
            Clause-by-clause intelligent optimization
          </p>
        </div>

        {/* Dynamic scroll containers to absorb extra text cleanly without pushing container bounds */}
        <div className="flex-1 overflow-y-auto p-8 flex flex-col gap-6 custom-scrollbar pb-32 justify-start">
          {selected ? (
            <>
              {/* Active Diff Split Workspace Layout */}
              <div className="flex flex-col gap-3 flex-1 min-h-[260px]">
                <div className="flex items-center justify-between px-1">
                  <h4 className="text-[10px] font-bold text-[#2c3e50] uppercase tracking-widest">
                    Active Comparison
                  </h4>
                </div>

                <div className="rounded-lg overflow-hidden border border-slate-200 shadow-sm bg-white flex flex-col h-full min-h-[240px]">
                  {/* Scrollable Current Original Clause Box */}
                  <div className="p-5 bg-[#c41e3a]/5 border-b border-slate-200 max-h-[160px] overflow-y-auto custom-scrollbar">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 rounded-full bg-[#c41e3a]"></span>
                      <span className="text-[10px] font-bold text-[#2c3e50] uppercase">
                        Current Clause
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 italic leading-relaxed">
                      "{selected.clause}"
                    </p>
                  </div>

                  {/* Scrollable Proposed AI Revision Box */}
                  <div className="p-5 bg-[#2d5016]/5 flex-1 max-h-[160px] overflow-y-auto custom-scrollbar">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 rounded-full bg-[#2d5016]"></span>
                      <span className="text-[10px] font-bold text-[#2c3e50] uppercase">
                        Proposed Revision
                      </span>
                    </div>
                    <p className="text-xs text-[#1a2d5c] leading-relaxed">
                      {selected.analysis?.rewritten_clause ||
                        "No revision generated for this risk context."}
                    </p>
                  </div>
                </div>
              </div>

              {/* Scrollable Final Preview Workspace Panel */}
              <div className="flex flex-col gap-3 flex-1 min-h-[180px]">
                <h4 className="text-[10px] font-bold text-[#2c3e50] uppercase tracking-widest px-1">
                  Final Clause Preview
                </h4>
                <div className="p-5 bg-slate-50 rounded-lg border border-slate-200 max-h-[160px] overflow-y-auto custom-scrollbar">
                  <p className="text-xs text-[#1a2d5c] leading-relaxed">
                    {selected.analysis?.rewritten_clause || selected.clause}
                  </p>
                </div>
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center p-6 my-auto">
              <p className="text-xs text-slate-400">
                Analyze contract and choose findings to view targeted
                optimization redlines.
              </p>
            </div>
          )}
        </div>
      </aside>

      {/* ================= FIXED BOTTOM OVERLAY ACTION BAR ================= */}
      <footer className="fixed bottom-0 right-0 h-20 bg-white border-t border-slate-200 px-10 flex items-center justify-end z-50 left-[340px]">
        <button
          onClick={downloadRedline}
          disabled={!redlineFile}
          className="bg-[#1a2d5c] text-white px-8 py-3.5 rounded-lg font-bold text-sm flex items-center gap-2.5 shadow-lg hover:bg-[#0f1f42] active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none transition-all"
        >
          <FileText className="w-4 h-4" />
          Download Redlined Contract
        </button>
      </footer>
    </div>
  );
}
