"use client";

import ScoreRing from "./ScoreRing";
import SectionBar from "./SectionBar";
import LLMQueryResults from "./LLMQueryResults";
import CompetitorComparison from "./CompetitorComparison";
import Recommendations from "./Recommendations";

interface SectionResult {
  score: number;
  max: number;
  details?: Record<string, unknown>;
  error?: string;
}

interface AnalysisData {
  url: string;
  total_score: number;
  total_max: number;
  sections: Record<string, SectionResult>;
  llm_queries: {
    queries: unknown[];
    summary: Record<string, unknown>;
  };
  recommendations: unknown[];
}

const SECTION_META: Record<string, { label: string; icon: string }> = {
  brand_authority: { label: "Brand Authority", icon: "🌐" },
  structured_data: { label: "Structured Data", icon: "🧩" },
  content_eeat: { label: "Content & E-E-A-T", icon: "✍️" },
  llm_access: { label: "LLM Access", icon: "🤖" },
  discoverability: { label: "Discoverability", icon: "🔍" },
};

function getVerdict(pct: number) {
  if (pct >= 80) return { text: "Excellent", color: "text-emerald-400" };
  if (pct >= 65) return { text: "Good", color: "text-emerald-500" };
  if (pct >= 50) return { text: "Needs work", color: "text-amber-400" };
  return { text: "Poor", color: "text-red-400" };
}

export default function Results({ data }: { data: Record<string, unknown> }) {
  const d = data as unknown as AnalysisData;
  const pct = d.total_max > 0 ? Math.round((d.total_score / d.total_max) * 100) : 0;
  const verdict = getVerdict(pct);

  return (
    <div className="w-full max-w-4xl space-y-6 mt-4">
      {/* Overall score */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 flex flex-col sm:flex-row items-center gap-8">
        <div className="relative">
          <ScoreRing score={d.total_score} max={d.total_max} size={160} />
        </div>
        <div className="text-center sm:text-left">
          <p className="text-zinc-500 text-sm mb-1">{d.url}</p>
          <h2 className="text-3xl font-bold mb-1">
            GEO Score: <span className={verdict.color}>{verdict.text}</span>
          </h2>
          <p className="text-zinc-400">
            {d.total_score} out of {d.total_max} points — {pct}% AI optimization readiness
          </p>
        </div>
      </div>

      {/* Section scores */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-5">Section Breakdown</h2>
        <div className="space-y-4">
          {Object.entries(SECTION_META).map(([key, { label, icon }]) => {
            const s = d.sections[key];
            if (!s) return null;
            return <SectionBar key={key} label={label} icon={icon} score={s.score} max={s.max} />;
          })}
        </div>
      </div>

      {/* LLM visibility */}
      <LLMQueryResults data={d.llm_queries as Parameters<typeof LLMQueryResults>[0]["data"]} />

      {/* Recommendations */}
      <Recommendations recs={d.recommendations as Parameters<typeof Recommendations>[0]["recs"]} />

      {/* Competitor comparison */}
      <CompetitorComparison target={d.url} sections={d.sections} />
    </div>
  );
}
