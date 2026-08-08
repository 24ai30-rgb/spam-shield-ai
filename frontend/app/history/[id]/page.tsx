"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { Download, Loader2, ShieldAlert } from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";
import { RiskGauge } from "@/components/charts/RiskGauge";
import { scanApi } from "@/lib/api";

export default function ScanDetailPage() {
  const { id } = useParams<{ id: string }>();

  const { data: scan, isLoading } = useQuery({
    queryKey: ["scan", id],
    queryFn: () => scanApi.getScan(id).then((r) => r.data),
    refetchInterval: (query) =>
      query.state.data?.status === "completed"
        ? false
        : 1500,
  });

  if (isLoading || !scan) {
    return (
      <AppShell title="Scan Result">
        <div className="flex items-center gap-2 text-fog-400 text-sm">
          <Loader2
            className="animate-spin"
            size={16}
          />
          Loading scan...
        </div>
      </AppShell>
    );
  }

  if (scan.status !== "completed") {
    return (
      <AppShell title="Analyzing...">
        <div className="card p-10 flex flex-col items-center gap-4">
          <Loader2
            className="animate-spin text-beacon-500"
            size={28}
          />

          <p className="text-sm text-fog-400">
            13 specialist AI agents are analyzing
            your submission. This usually takes a
            few seconds.
          </p>
        </div>
      </AppShell>
    );
  }

  const { verdict, agent_results } = scan;

  return (
    <AppShell
      title="Scan Result"
      subtitle={`Input type: ${scan.input_type}`}
    >
      <div className="grid lg:grid-cols-3 gap-6">

        {/* LEFT PANEL */}

        <div className="card p-6 flex flex-col items-center lg:col-span-1">

          <RiskGauge
            score={verdict.risk_score}
            verdict={verdict.verdict_label}
            size={170}
          />

          {verdict.scam_category && (
            <div className="mt-4 flex items-center gap-2 text-sm text-alert-500">
              <ShieldAlert size={16} />
              {verdict.scam_category}
            </div>
          )}

          <p className="mt-2 text-xs text-fog-400">
            AI Confidence :{" "}
            {(verdict.confidence_score * 100).toFixed(
              0
            )}
            %
          </p>

          {/* PDF BUTTON */}

          <button
            onClick={() =>
              scanApi.downloadReport(id)
            }
            className="btn-ghost mt-6 w-full flex items-center justify-center gap-2"
          >
            <Download size={16} />
            Download Professional PDF
          </button>
        </div>

        {/* RIGHT PANEL */}

        <div className="lg:col-span-2 space-y-6">

          {/* SUMMARY */}

          <div className="card p-6">
            <h3 className="text-sm font-semibold mb-2">
              Threat Summary
            </h3>

            <p className="text-sm text-fog-300 leading-relaxed">
              {verdict.explanation_text}
            </p>
          </div>

          {/* REASONING */}

          <div className="card p-6">

            <h3 className="text-sm font-semibold mb-3">
              Explainable AI Reasoning
            </h3>

            <ol className="space-y-2">

              {verdict.reasoning_chain.map(
                (
                  step: string,
                  index: number
                ) => (
                  <li
                    key={index}
                    className="flex gap-3 text-sm"
                  >
                    <span className="font-mono text-beacon-500 shrink-0">
                      {String(index + 1).padStart(
                        2,
                        "0"
                      )}
                    </span>

                    <span className="text-fog-300">
                      {step}
                    </span>
                  </li>
                )
              )}

            </ol>

          </div>

          {/* EVIDENCE */}

          {verdict.evidence_summary?.key_evidence
            ?.length > 0 && (
            <div className="card p-6">

              <h3 className="text-sm font-semibold mb-3">
                Key Evidence
              </h3>

              <div className="space-y-2">

                {verdict.evidence_summary.key_evidence.map(
                  (
                    e: any,
                    index: number
                  ) => (
                    <div
                      key={index}
                      className="flex justify-between border-b border-fog-400/10 pb-2 last:border-0"
                    >
                      <span className="text-sm">
                        {e.description}
                      </span>

                      <span
                        className={`badge ${
                          e.severity === "high"
                            ? "badge-high_risk"
                            : "badge-suspicious"
                        }`}
                      >
                        {e.severity}
                      </span>
                    </div>
                  )
                )}

              </div>

            </div>
          )}

          {/* ACTIONS */}

          <div className="card p-6">

            <h3 className="text-sm font-semibold mb-3">
              Recommended Actions
            </h3>

            <ul className="space-y-2">

              {verdict.recommended_actions.map(
                (
                  action: string,
                  index: number
                ) => (
                  <li
                    key={index}
                    className="flex gap-2 text-sm text-fog-300"
                  >
                    <span className="text-beacon-500">
                      •
                    </span>

                    {action}
                  </li>
                )
              )}

            </ul>

          </div>

          {/* AGENTS */}

          <div className="card p-6">

            <h3 className="text-sm font-semibold mb-3">
              Agent Risk Breakdown
            </h3>

            <div className="space-y-3">

              {agent_results.map((agent: any) => (

                <div key={agent.agent_name}>

                  <div className="flex justify-between text-xs mb-1">

                    <span className="capitalize font-mono">
                      {agent.agent_name.replaceAll(
                        "_",
                        " "
                      )}
                    </span>

                    <span>
                      {Math.round(agent.raw_score)}
                      /100
                    </span>

                  </div>

                  <div className="h-1.5 rounded-full bg-fog-400/10 overflow-hidden">

                    <div
                      className="h-full bg-beacon-500"
                      style={{
                        width: `${agent.raw_score}%`,
                      }}
                    />

                  </div>

                </div>

              ))}

            </div>

          </div>

        </div>

      </div>
    </AppShell>
  );
}