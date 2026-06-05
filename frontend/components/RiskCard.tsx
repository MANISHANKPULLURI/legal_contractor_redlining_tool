export default function RiskCard({
  item,
  isSelected,
  onClick,
}: {
  item: any;
  isSelected?: boolean;
  onClick?: () => void;
}) {
  const analysis = item.analysis || {};
  const level = analysis.risk_level || "UNKNOWN";
  const issue = analysis.issues?.[0];

  function severityStyle() {
    if (level === "HIGH") {
      return {
        border: "border-l-[#c41e3a]",
        badge: "bg-[#c41e3a]/5 text-[#c41e3a] border-[#c41e3a]/20",
        indicator: "⚠",
      };
    }

    if (level === "MEDIUM") {
      return {
        border: "border-l-[#e8843a]",
        badge: "bg-[#e8843a]/10 text-[#e8843a] border-[#e8843a]/20",
        indicator: "◆",
      };
    }

    if (level === "LOW") {
      return {
        border: "border-l-[#2d5016]",
        badge: "bg-[#2d5016]/5 text-[#2d5016] border-[#2d5016]/20",
        indicator: "✓",
      };
    }

    return {
      border: "border-l-slate-400",
      badge: "bg-slate-100 text-slate-700 border-slate-200",
      indicator: "•",
    };
  }

  const style = severityStyle();

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-lg border-y border-r ${style.border} border-l-[6px] border-slate-200 p-8 shadow-sm transition-all duration-200 cursor-pointer ${
        isSelected
          ? "ring-2 ring-[#1a2d5c] translate-x-1 shadow-md"
          : "hover:translate-x-1 hover:shadow-md"
      }`}
    >
      {/* HEADER */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <span
            className={`px-3 py-1.5 rounded-lg text-xs font-bold border ${style.badge}`}
          >
            {level.charAt(0) + level.slice(1).toLowerCase()} Severity
          </span>
          <span className="text-sm font-bold text-[#1a2d5c]">
            Clause {item.clause_number}
          </span>
          {item.clause_title && (
            <>
              <span className="w-1 h-1 bg-slate-300 rounded-full"></span>
              <span className="text-sm font-semibold text-[#2c3e50]">
                {item.clause_title}
              </span>
            </>
          )}
        </div>
      </div>

      {/* ISSUE */}
      <div className="flex flex-col gap-6">
        <div>
          <p className="text-[11px] font-bold text-[#2c3e50] uppercase tracking-wider mb-2">
            ISSUE
          </p>
          <h3 className="text-lg font-serif-legal font-bold text-[#1a2d5c] leading-snug">
            {issue?.issue || analysis.issue || "Not detected"}
          </h3>
        </div>

        {/* EXPLANATION */}
        <div>
          <p className="text-[11px] font-bold text-[#2c3e50] uppercase tracking-wider mb-2">
            LEGAL CONTEXT & EXPLANATION
          </p>
          <p className="text-sm text-slate-600 leading-relaxed">
            {issue?.why_risky ||
              analysis.explanation ||
              "No explanation available"}
          </p>
        </div>

        {/* RECOMMENDATION */}
        <div className="bg-[#2d5016]/5 p-6 rounded-lg border border-[#2d5016]/20 flex gap-4">
          <div className="w-2 h-2 rounded-full bg-[#2d5016] shrink-0 mt-1.5"></div>
          <div>
            <p className="text-sm text-[#2d5016] font-bold mb-1">
              Expert Recommendation
            </p>
            <p className="text-sm text-[#2d5016]/90 leading-relaxed">
              {analysis.recommendation ||
                analysis.suggestion ||
                "No recommendation"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
