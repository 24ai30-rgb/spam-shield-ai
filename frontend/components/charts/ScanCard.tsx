import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { formatDate, verdictDisplay, VerdictLabel } from "@/lib/utils";

export function ScanCard({
  id, inputType, riskScore, verdictLabel, createdAt,
}: {
  id: string; inputType: string; riskScore: number | null; verdictLabel: VerdictLabel | null; createdAt: string;
}) {
  return (
    <Link
      href={`/history/${id}`}
      className="card flex items-center justify-between px-5 py-4 transition hover:border-beacon-500/40"
    >
      <div className="flex items-center gap-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-void-900/5 dark:bg-white/5 text-xs font-mono uppercase">
          {inputType.slice(0, 3)}
        </div>
        <div>
          <p className="text-sm font-semibold capitalize">{inputType.replace("_", " ")} Scan</p>
          <p className="text-xs text-fog-400">{formatDate(createdAt)}</p>
        </div>
      </div>
      <div className="flex items-center gap-3">
        {verdictLabel && <span className={`badge badge-${verdictLabel}`}>{verdictDisplay[verdictLabel]}</span>}
        {riskScore !== null && <span className="font-mono text-sm font-bold">{Math.round(riskScore)}</span>}
        <ChevronRight size={16} className="text-fog-400" />
      </div>
    </Link>
  );
}
