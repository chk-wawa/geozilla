"use client";

interface Props {
  label: string;
  score: number;
  max: number;
  icon: string;
}

export default function SectionBar({ label, score, max, icon }: Props) {
  const pct = max > 0 ? (score / max) * 100 : 0;
  const color = pct >= 75 ? "bg-emerald-400" : pct >= 50 ? "bg-amber-400" : "bg-red-400";

  return (
    <div className="flex items-center gap-4">
      <span className="text-xl w-7 shrink-0">{icon}</span>
      <div className="flex-1">
        <div className="flex justify-between text-sm mb-1">
          <span className="text-zinc-300 font-medium">{label}</span>
          <span className="text-zinc-400">{score}/{max}</span>
        </div>
        <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-700 ${color}`}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </div>
  );
}
