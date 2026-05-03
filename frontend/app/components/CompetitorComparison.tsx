"use client";

interface SectionData {
  score: number;
  max: number;
}

interface Props {
  target: string;
  sections: Record<string, SectionData>;
}

const SECTION_LABELS: Record<string, { label: string; icon: string }> = {
  brand_authority: { label: "Brand Authority", icon: "🌐" },
  structured_data: { label: "Structured Data", icon: "🧩" },
  content_eeat: { label: "Content & E-E-A-T", icon: "✍️" },
  llm_access: { label: "LLM Access", icon: "🤖" },
  discoverability: { label: "Discoverability", icon: "🔍" },
};

// Static hardcoded competitor benchmark data for empik.com
const COMPETITOR_BENCHMARKS: Record<string, Record<string, number>> = {
  "taniaksiazka.pl": { brand_authority: 16, structured_data: 12, content_eeat: 11, llm_access: 3, discoverability: 11 },
  "bonito.pl": { brand_authority: 12, structured_data: 10, content_eeat: 10, llm_access: 2, discoverability: 10 },
  "gandalf.com.pl": { brand_authority: 10, structured_data: 8, content_eeat: 9, llm_access: 2, discoverability: 9 },
  "merlin.pl": { brand_authority: 14, structured_data: 11, content_eeat: 10, llm_access: 3, discoverability: 10 },
};

const MAX_SCORES: Record<string, number> = {
  brand_authority: 30, structured_data: 20, content_eeat: 20, llm_access: 15, discoverability: 15,
};

export default function CompetitorComparison({ target, sections }: Props) {
  const domain = target.replace(/https?:\/\/(www\.)?/, "").split("/")[0];
  const benchmarks = COMPETITOR_BENCHMARKS;
  const sectionKeys = Object.keys(SECTION_LABELS);

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-1">Competitive Comparison</h2>
      <p className="text-zinc-500 text-sm mb-6">How <span className="text-zinc-300">{domain}</span> stacks up vs key players</p>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-800">
              <th className="text-left text-zinc-500 font-normal pb-3 pr-4">Section</th>
              <th className="text-center text-emerald-400 font-semibold pb-3 px-3">{domain}</th>
              {Object.keys(benchmarks).map((comp) => (
                <th key={comp} className="text-center text-zinc-400 font-normal pb-3 px-3 whitespace-nowrap">{comp}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sectionKeys.map((key) => {
              const { label, icon } = SECTION_LABELS[key];
              const targetPct = sections[key] ? Math.round((sections[key].score / sections[key].max) * 100) : 0;
              return (
                <tr key={key} className="border-b border-zinc-800/50">
                  <td className="py-3 pr-4 text-zinc-400 whitespace-nowrap">
                    {icon} {label}
                  </td>
                  <td className="py-3 px-3 text-center">
                    <ScoreCell pct={targetPct} highlight />
                  </td>
                  {Object.entries(benchmarks).map(([comp, scores]) => {
                    const pct = Math.round((scores[key] / MAX_SCORES[key]) * 100);
                    const diff = targetPct - pct;
                    return (
                      <td key={comp} className="py-3 px-3 text-center">
                        <ScoreCell pct={pct} diff={diff} />
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-zinc-600 mt-4">* Competitor scores are representative benchmarks and may not reflect real-time data.</p>
    </div>
  );
}

function ScoreCell({ pct, highlight = false, diff }: { pct: number; highlight?: boolean; diff?: number }) {
  const color = pct >= 75 ? "text-emerald-400" : pct >= 50 ? "text-amber-400" : "text-red-400";
  return (
    <div className="flex flex-col items-center">
      <span className={`font-semibold ${highlight ? color : "text-zinc-300"}`}>{pct}%</span>
      {diff !== undefined && (
        <span className={`text-xs ${diff > 0 ? "text-emerald-500" : diff < 0 ? "text-red-500" : "text-zinc-600"}`}>
          {diff > 0 ? `+${diff}` : diff}
        </span>
      )}
    </div>
  );
}
