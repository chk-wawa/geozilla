"use client";

import { useState } from "react";

interface LLMMention {
  target_mentioned: boolean;
  competitors_mentioned: string[];
  response_snippet: string;
}

interface QueryResult {
  query: string;
  llms: Record<string, LLMMention | null>;
}

interface Props {
  data: {
    queries: QueryResult[];
    summary: {
      total_queries: number;
      mention_counts: Record<string, number>;
      competitors: string[];
    };
  };
}

const LLM_LABELS: Record<string, string> = {
  openai: "ChatGPT",
  claude: "Claude",
  gemini: "Gemini",
};

export default function LLMQueryResults({ data }: Props) {
  const [expanded, setExpanded] = useState<number | null>(null);
  const { queries, summary } = data;

  const allNull = queries?.length > 0 && queries.every((q) =>
    Object.values(q.llms).every((r) => r === null)
  );

  if (!queries?.length || allNull) {
    return (
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
        <h2 className="text-xl font-semibold mb-2">LLM Visibility</h2>
        <p className="text-zinc-500 text-sm mb-3">No LLM API keys configured — queries ran but got no responses.</p>
        <div className="bg-zinc-800 rounded-xl px-4 py-3 text-xs text-zinc-400 font-mono">
          <p className="mb-1">Create <span className="text-zinc-200">backend/.env</span> with:</p>
          <p>OPENAI_API_KEY=sk-...</p>
          <p>ANTHROPIC_API_KEY=sk-ant-...</p>
          <p>GEMINI_API_KEY=AI...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6">
      <h2 className="text-xl font-semibold mb-1">LLM Visibility</h2>
      <p className="text-zinc-500 text-sm mb-5">How often the brand appears in AI responses to relevant queries</p>

      {/* Summary row */}
      <div className="flex gap-4 mb-6 flex-wrap">
        {Object.entries(summary.mention_counts || {}).map(([llm, count]) => (
          <div key={llm} className="bg-zinc-800 rounded-xl px-4 py-3 text-center min-w-[100px]">
            <div className={`text-2xl font-bold ${(count as number) > 0 ? "text-emerald-400" : "text-zinc-500"}`}>{count}/{summary.total_queries}</div>
            <div className="text-xs text-zinc-400 mt-1">{LLM_LABELS[llm] ?? llm}</div>
          </div>
        ))}
      </div>

      {/* Per-query table */}
      <div className="space-y-2">
        {queries.map((q, i) => {
          const anyMention = Object.values(q.llms).some((r) => r?.target_mentioned);
          return (
            <div key={i} className="border border-zinc-800 rounded-xl overflow-hidden">
              <button
                onClick={() => setExpanded(expanded === i ? null : i)}
                className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-zinc-800/50 transition-colors"
              >
                <span className="text-sm text-zinc-300">{q.query}</span>
                <div className="flex items-center gap-3 shrink-0">
                  {Object.entries(q.llms).map(([llm, r]) =>
                    r ? (
                      <span
                        key={llm}
                        title={LLM_LABELS[llm]}
                        className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                          r.target_mentioned ? "bg-emerald-900 text-emerald-300" : "bg-zinc-800 text-zinc-500"
                        }`}
                      >
                        {LLM_LABELS[llm]}
                      </span>
                    ) : null
                  )}
                  <span className="text-zinc-600 text-xs">{expanded === i ? "▲" : "▼"}</span>
                </div>
              </button>

              {expanded === i && (
                <div className="border-t border-zinc-800 px-4 py-4 space-y-4">
                  {Object.entries(q.llms).map(([llm, r]) =>
                    r ? (
                      <div key={llm}>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-medium text-zinc-300">{LLM_LABELS[llm]}</span>
                          {r.target_mentioned ? (
                            <span className="text-xs bg-emerald-900 text-emerald-300 px-2 py-0.5 rounded-full">Mentioned</span>
                          ) : (
                            <span className="text-xs bg-zinc-800 text-zinc-500 px-2 py-0.5 rounded-full">Not mentioned</span>
                          )}
                          {r.competitors_mentioned.length > 0 && (
                            <span className="text-xs text-amber-400">Competitors: {r.competitors_mentioned.join(", ")}</span>
                          )}
                        </div>
                        <p className="text-xs text-zinc-500 font-mono leading-relaxed">{r.response_snippet}…</p>
                      </div>
                    ) : null
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
