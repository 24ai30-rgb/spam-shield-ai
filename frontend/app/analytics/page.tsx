"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import {
  Shield,
  ShieldCheck,
  TrendingUp,
  Activity,
  Sparkles,
  Download,
  BarChart3,
} from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";

import {
  VerdictDistributionChart,
  CategoryBreakdownChart,
} from "@/components/charts/DashboardCharts";

import { dashboardApi } from "@/lib/api";

export default function AnalyticsPage() {

  const {
    data: stats,
    isLoading,
  } = useQuery({

    queryKey: ["dashboard-stats"],

    queryFn: () =>
      dashboardApi
        .stats()
        .then((r) => r.data),

  });

  const total =
    stats?.total_scans ?? 0;

  const blocked =
    stats?.scams_blocked ?? 0;

  const blockRate =
    total > 0
      ? Math.round((blocked / total) * 100)
      : 0;

  const safetyScore =
    stats?.cyber_safety_score ?? 70;

  return (

    <AppShell
      title="Analytics"
      subtitle="Enterprise Cyber Threat Analytics Dashboard"
    >

      {/* HERO */}

      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700 p-8 mb-8">

        <div className="absolute right-0 top-0 opacity-10">

          <Shield
            size={220}
            className="text-cyan-400"
          />

        </div>

        <div className="relative z-10">

          <div className="flex items-center gap-2 text-cyan-400">

            <Sparkles size={18} />

            <span className="text-sm font-semibold">

              Enterprise Threat Analytics

            </span>

          </div>

          <h1 className="text-5xl font-bold mt-4 text-white">

            Cyber Security Analytics

          </h1>

          <p className="mt-4 max-w-2xl text-slate-300 leading-7">

            Monitor threat detection,
            AI performance,
            scam trends,
            protection score
            and investigation history
            in one place.

          </p>

          <div className="grid md:grid-cols-4 gap-5 mt-8">

            <MetricTile
              icon={Activity}
              label="Total Scans"
              value={total}
              color="text-green-400"
            />

            <MetricTile
              icon={ShieldCheck}
              label="Threats Blocked"
              value={blocked}
              color="text-red-400"
            />

            <MetricTile
              icon={TrendingUp}
              label="Block Rate"
              value={`${blockRate}%`}
              color="text-cyan-400"
            />

            <MetricTile
              icon={Shield}
              label="Safety Score"
              value={`${safetyScore}%`}
              color="text-yellow-400"
            />

          </div>

        </div>

      </div>
            {/* AI STATUS */}

      <div className="card p-6 mb-8">

        <div className="flex justify-between items-center">

          <div>

            <h2 className="text-xl font-bold">

              AI Protection Status

            </h2>

            <p className="text-fog-400 mt-2">

              Spam Shield AI is continuously monitoring
              phishing attacks, malicious websites,
              fake banking portals and scam messages.

            </p>

          </div>

          <Link
            href="/history"
            className="btn-primary flex items-center gap-2"
          >

            <Download size={18} />

            View Reports

          </Link>

        </div>

      </div>

      {/* SUMMARY */}

      <div className="grid lg:grid-cols-4 gap-5 mb-8">

        <div className="card p-6">

          <BarChart3
            className="text-cyan-400 mb-3"
            size={28}
          />

          <p className="text-3xl font-bold">

            {total}

          </p>

          <p className="text-fog-400 text-sm mt-2">

            Investigations

          </p>

        </div>

        <div className="card p-6">

          <ShieldCheck
            className="text-green-400 mb-3"
            size={28}
          />

          <p className="text-3xl font-bold">

            {blocked}

          </p>

          <p className="text-fog-400 text-sm mt-2">

            Threats Blocked

          </p>

        </div>

        <div className="card p-6">

          <TrendingUp
            className="text-yellow-400 mb-3"
            size={28}
          />

          <p className="text-3xl font-bold">

            {blockRate}%

          </p>

          <p className="text-fog-400 text-sm mt-2">

            Detection Rate

          </p>

        </div>

        <div className="card p-6">

          <Shield
            className="text-red-400 mb-3"
            size={28}
          />

          <p className="text-3xl font-bold">

            {safetyScore}%

          </p>

          <p className="text-fog-400 text-sm mt-2">

            Security Score

          </p>

        </div>

      </div>

      {/* CHARTS */}

      <div className="grid lg:grid-cols-2 gap-6">

        <div className="card p-6">

          <h2 className="text-lg font-bold mb-4">

            Verdict Distribution

          </h2>

          <VerdictDistributionChart
            data={
              stats?.verdict_distribution ?? {}
            }
          />

        </div>

        <div className="card p-6">

          <h2 className="text-lg font-bold mb-4">

            Scam Category Breakdown

          </h2>

          <CategoryBreakdownChart
            data={
              stats?.scans_by_category ?? {}
            }
          />

        </div>

      </div>

      {/* AI INSIGHTS */}

      <div className="grid lg:grid-cols-3 gap-6 mt-8">

        <div className="card p-6">

          <h3 className="font-bold text-green-400">

            System Health

          </h3>

          <p className="mt-3 text-fog-400">

            All AI agents are operational.
            Detection engine is running normally.

          </p>

        </div>

        <div className="card p-6">

          <h3 className="font-bold text-red-400">

            Highest Threat

          </h3>

          <p className="mt-3 text-fog-400">

            URL phishing remains the most
            frequently detected scam category.

          </p>

        </div>

        <div className="card p-6">

          <h3 className="font-bold text-cyan-400">

            Recommendation

          </h3>

          <p className="mt-3 text-fog-400">

            Continue scanning unknown links
            before opening them to reduce
            phishing risk.

          </p>

        </div>

      </div>

            {/* PERFORMANCE SUMMARY */}

      <div className="card p-6 mt-8">

        <h2 className="text-xl font-bold mb-6">

          Performance Summary

        </h2>

        <div className="grid md:grid-cols-4 gap-6">

          <div>

            <p className="text-4xl font-bold text-green-400">

              {blocked}

            </p>

            <p className="text-sm text-fog-400 mt-2">

              Threats Prevented

            </p>

          </div>

          <div>

            <p className="text-4xl font-bold text-cyan-400">

              {total}

            </p>

            <p className="text-sm text-fog-400 mt-2">

              Total Investigations

            </p>

          </div>

          <div>

            <p className="text-4xl font-bold text-yellow-400">

              {blockRate}%

            </p>

            <p className="text-sm text-fog-400 mt-2">

              Success Rate

            </p>

          </div>

          <div>

            <p className="text-4xl font-bold text-red-400">

              {safetyScore}%

            </p>

            <p className="text-sm text-fog-400 mt-2">

              Security Rating

            </p>

          </div>

        </div>

      </div>

      {/* FOOTER */}

      <div className="card p-6 mt-8 text-center">

        <Shield
          className="mx-auto text-cyan-400 mb-4"
          size={42}
        />

        <h2 className="text-xl font-bold">

          Spam Shield AI Analytics

        </h2>

        <p className="text-fog-400 mt-3">

          Enterprise-grade cyber security analytics
          powered by Multi-Agent Artificial Intelligence.

        </p>

      </div>

    </AppShell>

  );

}

type MetricTileProps = {

  icon: any;
  label: string;
  value: any;
  color?: string;

};

function MetricTile({

  icon: Icon,
  label,
  value,
  color = "text-current",

}: MetricTileProps) {

  return (

    <div className="card p-6 hover:scale-[1.02] transition-all duration-300">

      <div
        className={`h-12 w-12 rounded-xl bg-current/10 flex items-center justify-center ${color}`}
      >

        <Icon size={22} />

      </div>

      <p
        className={`text-3xl font-bold mt-4 ${color}`}
      >

        {value}

      </p>

      <p className="text-sm text-fog-400 mt-2">

        {label}

      </p>

    </div>

  );

}