"use client";

import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/layout/AppShell";
import { ScanCard } from "@/components/charts/ScanCard";
import { scanApi } from "@/lib/api";

export default function HistoryPage() {
  const { data: scans, isLoading } = useQuery({
    queryKey: ["scan-history"],
    queryFn: () => scanApi.history().then((r) => r.data),
  });

  return (
    <AppShell title="Threat History" subtitle="Every scan you've run, with saved reports and verdicts">
      <div className="space-y-2">
        {isLoading && <p className="text-sm text-fog-400">Loading…</p>}
        {scans?.length === 0 && (
          <div className="card p-10 text-center text-fog-400 text-sm">
            No scans yet. Head to the Upload Center to run your first scan.
          </div>
        )}
        {scans?.map((s: any) => (
          <ScanCard
            key={s.id} id={s.id} inputType={s.input_type}
            riskScore={s.risk_score} verdictLabel={s.verdict_label} createdAt={s.created_at}
          />
        ))}
      </div>
    </AppShell>
  );
}
