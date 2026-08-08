"use client";

import { verdictColor, verdictDisplay, VerdictLabel } from "@/lib/utils";

/**
 * The platform's signature visual element: a radar-sweep risk dial.
 * Ties the "Shield" watch/vigilance concept to a concrete, recognizable
 * UI motif used consistently across the dashboard, scan results, and PDF.
 */
export function RiskGauge({
  score,
  verdict,
  size = 180,
}: {
  score: number;
  verdict: VerdictLabel;
  size?: number;
}) {
  const radius = size / 2 - 12;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = verdictColor[verdict];

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative" style={{ width: size, height: size }}>
        {/* Radar sweep background rings */}
        <div className="absolute inset-0 rounded-full border border-fog-400/10" />
        <div className="absolute inset-4 rounded-full border border-fog-400/10" />
        <div className="absolute inset-8 rounded-full border border-fog-400/10" />

        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={10}
            fill="none"
            className="text-fog-400/10"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={10}
            strokeLinecap="round"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{ transition: "stroke-dashoffset 0.8s ease, stroke 0.3s ease" }}
          />
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-mono text-4xl font-bold" style={{ color }}>
            {Math.round(score)}
          </span>
          <span className="text-xs text-fog-400">/ 100</span>
        </div>
      </div>
      <span className={`badge badge-${verdict}`}>{verdictDisplay[verdict]}</span>
    </div>
  );
}
