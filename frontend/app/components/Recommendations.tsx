"use client";

import { useState } from "react";

interface Rec {
  section: string;
  priority: "high" | "medium" | "low";
  title: string;
  detail: string;
  effort: "low" | "medium" | "high";
}

const SECTION_LABELS: Record<string, string> = {
  brand_authority: "Brand Authority",
  structured_data: "Structured Data",
  content_eeat: "Content & E-E-A-T",
  llm_access: "LLM Access",
  discoverability: "Discoverability",
};

const PRIORITY_STYLE: Record<string, string> = {
  high: "bg-red-900/60 text-red-300 border-red-800",
  medium: "bg-amber-900/60 text-amber-300 border-amber-800",
  low: "bg-zinc-800 text-zinc-400 border-zinc-700",
};

const EFFORT_LABEL: Record<string, string> = {
  low: "Quick win",
  medium: "Some effort",
  high: "Major effort",
};

export default function Recommendations({ recs }: { recs: Rec[] }) {
  const [expanded, setExpanded] = useState<number | null>(null);
  const [filter, setFilter] = useState<string>("all");

  if (!recs?.length) return null;

  const filters = ["all", "high", "medium", "low"];
  const filtered = filter === "all" ? recs : recs.filter((r) => r.priority === filter);

  const counts = { high: recs.filter((r) => r.priority === "high").length, medium: recs.filter((r) => r.priority === "medium").length, low: recs.filter((r) => r.priority === "low").length };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-1">Actionable Recommendations</h2>
      <p className="text-zinc-500 text-sm mb-5">Prioritized steps to improve your GEO/AIO score</p>

      {/* Filter tabs */}
      <div className="flex gap-2 mb-5 flex-wrap">
        {filters.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === f ? "bg-zinc-700 text-zinc-100" : "bg-zinc-800 text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {f === "all" ? `All (${recs.length})` : f === "high" ? `High priority (${counts.high})` : f === "medium" ? `Medium (${counts.medium})` : `Low (${counts.low})`}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {filtered.map((rec, i) => {
          const idx = recs.indexOf(rec);
          return (
            <div key={idx} className={`border rounded-xl overflow-hidden ${PRIORITY_STYLE[rec.priority]}`}>
              <button
                onClick={() => setExpanded(expanded === idx ? null : idx)}
                className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-white/5 transition-colors"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <span className={`shrink-0 text-xs font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full border ${PRIORITY_STYLE[rec.priority]}`}>
                    {rec.priority}
                  </span>
                  <span className="text-sm font-medium text-zinc-100 truncate">{rec.title}</span>
                </div>
                <div className="flex items-center gap-3 shrink-0 ml-3">
                  <span className="text-xs text-zinc-500 hidden sm:block">{SECTION_LABELS[rec.section]}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${rec.effort === "low" ? "bg-emerald-900/50 text-emerald-400" : rec.effort === "medium" ? "bg-amber-900/50 text-amber-400" : "bg-red-900/50 text-red-400"}`}>
                    {EFFORT_LABEL[rec.effort]}
                  </span>
                  <span className="text-zinc-600 text-xs">{expanded === idx ? "▲" : "▼"}</span>
                </div>
              </button>

              {expanded === idx && (
                <div className="px-4 pb-4 pt-1 border-t border-white/10">
                  <p className="text-sm text-zinc-300 leading-relaxed">{rec.detail}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
