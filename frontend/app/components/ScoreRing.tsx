"use client";

interface Props {
  score: number;
  max: number;
  size?: number;
}

export default function ScoreRing({ score, max, size = 140 }: Props) {
  const pct = max > 0 ? score / max : 0;
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  const dash = pct * circumference;
  const color = pct >= 0.75 ? "#34d399" : pct >= 0.5 ? "#fbbf24" : "#f87171";

  return (
    <svg width={size} height={size} viewBox="0 0 120 120" className="rotate-[-90deg]">
      <circle cx="60" cy="60" r={radius} fill="none" stroke="#27272a" strokeWidth="10" />
      <circle
        cx="60" cy="60" r={radius} fill="none"
        stroke={color} strokeWidth="10"
        strokeDasharray={`${dash} ${circumference}`}
        strokeLinecap="round"
        style={{ transition: "stroke-dasharray 0.8s ease" }}
      />
      <text
        x="60" y="60" textAnchor="middle" dominantBaseline="central"
        className="rotate-[90deg]"
        style={{ transform: "rotate(90deg) translate(0px, -120px)", fill: color, fontSize: 22, fontWeight: 700 }}
      >
        {score}
      </text>
      <text
        x="60" y="80" textAnchor="middle"
        style={{ transform: "rotate(90deg) translate(0px, -120px)", fill: "#71717a", fontSize: 11 }}
      >
        / {max}
      </text>
    </svg>
  );
}
