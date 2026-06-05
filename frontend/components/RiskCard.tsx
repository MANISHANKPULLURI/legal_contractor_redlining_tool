import { AlertCircle, CheckCircle2, AlertTriangle, ShieldAlert, Lightbulb } from "lucide-react";

export default function RiskCard({ item, isSelected, onClick }: { item: any; isSelected?: boolean; onClick?: () => void }) {
  const analysis = item.analysis || {};
  const level = analysis.risk_level || "UNKNOWN";
  const issue = analysis.issues?.[0];

  function severityStyle() {
    if (level === "HIGH") {
      return {
        border: "border-l-[#ba1a1a]",
        badge: "bg-[#ba1a1a]/5 text-[#ba1a1a] border-[#ba1a1a]/10",
        icon: <ShieldAlert className="w-3.5 h-3.5 text-[#ba1a1a]" />
      };
    }

    if (level === "MEDIUM") {
      return {
        border: "border-l-[#745853]",
        badge: "bg-[#745853]/10 text-[#745853] border-[#745853]/10",
        icon: <AlertTriangle className="w-3.5 h-3.5 text-[#745853]" />
      };
    }

    if (level === "LOW") {
      return {
        border: "border-l-emerald-700",
        badge: "bg-emerald-50 text-emerald-700 border-emerald-100",
        icon: <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
      };
    }

    return {
      border: "border-l-gray-400",
      badge: "bg-gray-100 text-gray-700 border-gray-200",
      icon: <AlertCircle className="w-3.5 h-3.5 text-gray-600" />
    };
  }

  const style = severityStyle();

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-2xl border-y border-r ${style.border} border-l-[6px] border-neutral-200/60 p-8 shadow-sm transition-all duration-200 cursor-pointer ${
        isSelected ? 'ring-2 ring-[#745853] translate-x-1 shadow-md' : 'hover:translate-x-1 hover:shadow-md'
      }`}
    >
      {/* HEADER */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <span className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 border ${style.badge}`}>
            {style.icon}
            {level.charAt(0) + level.slice(1).toLowerCase()} Severity
          </span>
          <span className="text-sm font-bold text-[#1b1c15]">Clause {item.clause_number}</span>
          {item.clause_title && (
            <>
              <span className="w-1 h-1 bg-neutral-300 rounded-full"></span>
              <span className="text-sm font-semibold text-neutral-500">{item.clause_title}</span>
            </>
          )}
        </div>
      </div>

      {/* ISSUE */}
      <div className="flex flex-col gap-6">
        <div>
          <p className="text-[11px] font-bold text-neutral-400 uppercase tracking-wider mb-2">ISSUE</p>
          <h3 className="text-lg font-serif-legal font-bold text-[#1b1c15] leading-snug">
            {issue?.issue || analysis.issue || "Not detected"}
          </h3>
        </div>

        {/* EXPLANATION */}
        <div>
          <p className="text-[11px] font-bold text-neutral-400 uppercase tracking-wider mb-2">LEGAL CONTEXT & EXPLANATION</p>
          <p className="text-sm text-neutral-600 leading-relaxed">
            {issue?.why_risky || analysis.explanation || "No explanation available"}
          </p>
        </div>

        {/* RECOMMENDATION */}
        <div className="bg-emerald-50/50 p-6 rounded-2xl border border-emerald-100/50 flex gap-4">
          <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center shrink-0">
            <Lightbulb className="w-5 h-5 text-emerald-700" />
          </div>
          <div>
            <p className="text-sm text-emerald-900 font-bold mb-1">Expert Recommendation</p>
            <p className="text-sm text-emerald-800 leading-relaxed">
              {analysis.recommendation || analysis.suggestion || "No recommendation"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}