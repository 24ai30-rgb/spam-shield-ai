"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import {
  Shield,
  ShieldCheck,
  TrendingUp,
  Users,
  UploadCloud,
  Sparkles,
  Activity,
  ArrowUpRight,
  ScanLine,
} from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";
import { RiskGauge } from "@/components/charts/RiskGauge";
import { ScanCard } from "@/components/charts/ScanCard";

import {
  VerdictDistributionChart,
  CategoryBreakdownChart,
} from "@/components/charts/DashboardCharts";

import {
  dashboardApi,
  communityApi,
} from "@/lib/api";

import { useRequireAuth } from "@/lib/useRequireAuth";

export default function DashboardPage() {

  const { ready } = useRequireAuth();

  const {
    data: stats,
    isLoading,
  } = useQuery({

    enabled: ready,

    queryKey: ["dashboard-stats"],

    queryFn: () =>
      dashboardApi
        .stats()
        .then((r) => r.data),

  });

  const {
    data: trending,
  } = useQuery({

    queryKey: ["trending-scams"],

    queryFn: () =>
      communityApi
        .trending()
        .then((r) => r.data),

  });

  const safetyScore =
    stats?.cyber_safety_score ?? 70;

  const safetyVerdict =
    safetyScore >= 80
      ? "safe"
      : safetyScore >= 55
      ? "suspicious"
      : "high_risk";

  return (

    <AppShell
      title="Dashboard"
      subtitle="Your personal cyber threat overview"
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

              AI Powered Cyber Defense Platform

            </span>

          </div>

          <h1 className="mt-4 text-5xl font-bold text-white">

            Welcome Back 👋

          </h1>

          <p className="mt-4 max-w-2xl text-slate-300 leading-7">

            Spam Shield AI continuously protects
            against phishing websites,
            scam messages,
            malicious QR codes,
            fake banking portals
            and investment fraud.

          </p>

          <div className="grid md:grid-cols-4 gap-5 mt-8">

            <div className="rounded-2xl bg-white/5 border border-white/10 p-5">

              <Activity
                className="text-green-400 mb-3"
              />

              <h2 className="text-4xl font-bold">

                {stats?.total_scans ?? 0}

              </h2>

              <p className="text-slate-400 text-sm">

                Total Scans

              </p>

            </div>

            <div className="rounded-2xl bg-white/5 border border-white/10 p-5">

              <ShieldCheck
                className="text-red-400 mb-3"
              />

              <h2 className="text-4xl font-bold">

                {stats?.scams_blocked ?? 0}

              </h2>

              <p className="text-slate-400 text-sm">

                Threats Blocked

              </p>

            </div>

            <div className="rounded-2xl bg-white/5 border border-white/10 p-5">

              <Users
                className="text-cyan-400 mb-3"
              />

              <h2 className="text-4xl font-bold">

                {stats?.community_reports ?? 0}

              </h2>

              <p className="text-slate-400 text-sm">

                Community Reports

              </p>

            </div>

            <div className="rounded-2xl bg-white/5 border border-white/10 p-5">

              <ArrowUpRight
                className="text-yellow-400 mb-3"
              />

              <h2 className="text-4xl font-bold">

                {safetyScore}%

              </h2>

              <p className="text-slate-400 text-sm">

                AI Safety Score

              </p>

            </div>

          </div>

        </div>

      </div>

      {/* LIVE STATUS */}

      <div className="mb-8 rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-5 flex items-center justify-between">

        <div>

          <h3 className="font-semibold text-lg">

            🚀 Live Threat Monitoring Enabled

          </h3>

          <p className="text-sm text-slate-400">

            Your Spam Shield AI engine is actively
            monitoring URLs, Emails, QR Codes,
            SMS, Banking and Shopping scams.

          </p>

        </div>

        <ScanLine
          className="text-cyan-400"
          size={42}
        />

      </div>

      {/* QUICK STATS */}

      <div className="grid lg:grid-cols-3 gap-6">

        <div className="card p-6 flex flex-col items-center">

          <h3 className="text-sm font-semibold text-fog-400 mb-4">

            Cyber Safety Score

          </h3>

          <RiskGauge
            score={safetyScore}
            verdict={safetyVerdict as any}
            size={170}
          />

          <p className="mt-4 text-xs text-center text-fog-400">

            Based on your scan history and
            detected cyber threats.

          </p>

        </div>

        <div className="lg:col-span-2 grid sm:grid-cols-3 gap-4">

          <StatCard
            icon={ShieldCheck}
            label="Total Scans"
            value={stats?.total_scans ?? "—"}
            color="text-green-500"
          />

          <StatCard
            icon={TrendingUp}
            label="Threats Blocked"
            value={stats?.scams_blocked ?? "—"}
            color="text-red-500"
          />

          <StatCard
            icon={Users}
            label="Community Reports"
            value={stats?.community_reports ?? "—"}
            color="text-cyan-500"
          />

          <Link
            href="/upload"
            className="sm:col-span-3 card p-6 flex items-center justify-between bg-cyan-500/5 border border-cyan-500/20 hover:bg-cyan-500/10 transition-all"
          >

            <div className="flex items-center gap-4">

              <UploadCloud
                className="text-cyan-400"
                size={26}
              />

              <div>

                <p className="font-semibold">

                  Run New Investigation

                </p>

                <p className="text-sm text-fog-400">

                  Analyze URL,
                  Email,
                  Screenshot,
                  QR Code,
                  Phone Number
                  and Documents.

                </p>

              </div>

            </div>

            <span className="btn-primary">

              Scan Now

            </span>

          </Link>

        </div>

      </div>

      {/* ANALYTICS */}

      <div className="grid lg:grid-cols-2 gap-6 mt-8">

        <div className="card p-6">

          <div className="flex justify-between items-center mb-5">

            <div>

              <h2 className="text-lg font-bold">

                Threat Distribution

              </h2>

              <p className="text-sm text-fog-400">

                AI verdict breakdown

              </p>

            </div>

          </div>

          <VerdictDistributionChart
            data={
              stats?.verdict_distribution ?? {}
            }
          />

        </div>

        <div className="card p-6">

          <div className="flex justify-between items-center mb-5">

            <div>

              <h2 className="text-lg font-bold">

                Scam Categories

              </h2>

              <p className="text-sm text-fog-400">

                Threat category analysis

              </p>

            </div>

          </div>

          <CategoryBreakdownChart
            data={
              stats?.scans_by_category ?? {}
            }
          />

        </div>

      </div>

      {/* RECENT SCANS */}

      <div className="mt-10">

        <div className="flex justify-between items-center mb-5">

          <div>

            <h2 className="text-xl font-bold">

              Investigation Timeline

            </h2>

            <p className="text-sm text-fog-400">

              Latest investigations

            </p>

          </div>

          <span className="badge badge-safe">

            LIVE

          </span>

        </div>

        <div className="space-y-3">

          {isLoading && (
            <p className="text-sm text-fog-400">
              Loading investigations...
            </p>
          )}

          {stats?.recent_scans?.length === 0 && (
            <div className="card p-6 text-center">

              <Shield
                size={42}
                className="mx-auto text-fog-500 mb-3"
              />

              <h3 className="font-semibold">

                No Investigations Yet

              </h3>

              <p className="text-sm text-fog-400 mt-2">

                Run your first cyber threat
                investigation to see reports here.

              </p>

            </div>
          )}

          {stats?.recent_scans?.map((scan: any) => (

            <div
              key={scan.id}
              className="transition-all duration-300 hover:scale-[1.01]"
            >

              <ScanCard
                id={scan.id}
                inputType={scan.input_type}
                riskScore={scan.risk_score}
                verdictLabel={scan.verdict_label}
                createdAt={scan.created_at}
              />

            </div>

          ))}

        </div>

      </div>

      {/* COMMUNITY + AI */}

      <div className="grid lg:grid-cols-3 gap-6 mt-10">

        <div className="lg:col-span-2 card p-6">

          <h2 className="text-lg font-bold mb-4">

            🤖 AI Security Insights

          </h2>

          <div className="space-y-4">

            <div className="rounded-xl bg-green-500/10 border border-green-500/20 p-4">

              <h3 className="font-semibold">

                Protection Status

              </h3>

              <p className="text-sm text-fog-400 mt-2">

                Your account is currently protected by
                Spam Shield AI's multi-agent detection
                engine.

              </p>

            </div>

            <div className="rounded-xl bg-yellow-500/10 border border-yellow-500/20 p-4">

              <h3 className="font-semibold">

                AI Recommendation

              </h3>

              <p className="text-sm text-fog-400 mt-2">

                Avoid opening links received from
                unknown numbers. Always verify
                payment requests before sending money.

              </p>

            </div>

            <div className="rounded-xl bg-cyan-500/10 border border-cyan-500/20 p-4">

              <h3 className="font-semibold">

                System Status

              </h3>

              <p className="text-sm text-fog-400 mt-2">

                All AI agents are online and
                responding normally.

              </p>

            </div>

          </div>

        </div>

        <div>

          <h2 className="text-lg font-bold mb-4">

            🌍 Global Scam Feed

          </h2>

          <div className="card p-5 space-y-3">

            {(!trending || trending.length === 0) && (

              <p className="text-sm text-fog-400">

                No active community reports.

              </p>

            )}

            {trending?.slice(0,6).map((item:any,index:number)=>(

              <div
                key={index}
                className="border-b border-fog-400/10 pb-3 last:border-0"
              >

                <p className="font-mono text-xs truncate">

                  {item.raw_value}

                </p>

                <div className="flex justify-between mt-2">

                  <span className="text-xs text-fog-400 capitalize">

                    {item.input_type}

                  </span>

                  <span className="badge badge-high_risk">

                    🔥 {item.report_count}

                  </span>

                </div>

              </div>

            ))}

          </div>

        </div>

      </div>

    </AppShell>

  );

}

function StatCard({

  icon: Icon,
  label,
  value,
  color,

}:{

  icon:any;
  label:string;
  value:any;
  color:string;

}){

  return(

    <div className="card p-5 flex items-center gap-4 hover:scale-105 transition-all duration-300">

      <div className={`h-12 w-12 rounded-xl bg-current/10 flex items-center justify-center ${color}`}>

        <Icon size={22}/>

      </div>

      <div>

        <p className="text-2xl font-bold">

          {value}

        </p>

        <p className="text-xs text-fog-400">

          {label}

        </p>

      </div>

    </div>

  );

}