"use client";

import { useState } from "react";
import Results from "./components/Results";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<null | Record<string, unknown>>(null);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) return;
    setLoading(true);
    setData(null);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url.trim() }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const json = await res.json();
      setData(json);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex flex-col items-center min-h-screen px-4 py-16">
      <div className="w-full max-w-2xl mb-12 text-center">
        <h1 className="text-5xl font-bold tracking-tight mb-3">
          <span className="text-emerald-400">Geo</span>zilla
        </h1>
        <p className="text-zinc-400 text-lg">
          Audit how AI-ready your platform is — GEO & AIO analysis
        </p>
      </div>

      <form onSubmit={handleSubmit} className="w-full max-w-2xl flex gap-3 mb-10">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://empik.com"
          className="flex-1 bg-zinc-900 border border-zinc-700 rounded-xl px-5 py-3 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-emerald-500 transition-colors"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed text-zinc-950 font-semibold rounded-xl px-6 py-3 transition-colors"
        >
          {loading ? "Analyzing…" : "Analyze"}
        </button>
      </form>

      {loading && (
        <div className="flex flex-col items-center gap-4 mt-8">
          <div className="w-12 h-12 border-4 border-zinc-700 border-t-emerald-400 rounded-full animate-spin" />
          <p className="text-zinc-400 text-sm">Running full GEO audit — this may take 30–60s</p>
        </div>
      )}

      {error && (
        <div className="w-full max-w-2xl bg-red-950 border border-red-800 rounded-xl px-5 py-4 text-red-300 text-sm">
          {error}
        </div>
      )}

      {data && <Results data={data} />}
    </main>
  );
}
