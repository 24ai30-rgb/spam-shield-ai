"use client";

import React from "react";
import {
  ArrowRight,
  Bot,
  CheckCircle2,
  Globe2,
  Lock,
  Mail,
  MessageSquare,
  Phone,
  QrCode,
  ShieldCheck,
  Sparkles,
  Activity,
  Clock3,
} from "lucide-react";

export default function Hero() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[#050b18] text-white">

      {/* ================= BACKGROUND ================= */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">

        {/* Cyber Grid */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.025)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.025)_1px,transparent_1px)] bg-[size:55px_55px]" />

        {/* Blue Glow */}
        <div className="absolute left-[30%] top-[15%] h-[500px] w-[500px] rounded-full bg-blue-500/10 blur-[130px] animate-pulse" />

        {/* Purple Glow */}
        <div className="absolute right-[5%] top-[20%] h-[450px] w-[450px] rounded-full bg-purple-500/10 blur-[130px] animate-pulse" />

        {/* Orange Glow */}
        <div className="absolute bottom-0 left-[10%] h-[350px] w-[500px] rounded-full bg-orange-500/5 blur-[120px]" />

        {/* Moving Glow */}
        <div className="absolute left-[45%] top-[40%] h-2 w-2 rounded-full bg-cyan-400 shadow-[0_0_30px_10px_rgba(34,211,238,0.35)] animate-ping" />
      </div>

      {/* ================= HERO ================= */}
      <section className="relative mx-auto max-w-7xl px-6 pb-16 pt-20 lg:px-8 lg:pt-28">

        <div className="grid items-center gap-16 lg:grid-cols-[1.05fr_0.95fr]">

          {/* ================= LEFT SIDE ================= */}
          <div className="relative z-10">

            {/* Badge */}
            <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-300 shadow-[0_0_25px_rgba(16,185,129,0.08)] transition-all duration-300 hover:border-emerald-400/70 hover:bg-emerald-500/15">

              <Sparkles className="h-4 w-4 animate-pulse" />

              AI-Powered Scam Protection
            </div>

            {/* ================= HEADING ================= */}
            <h1 className="max-w-3xl font-bold tracking-[-0.045em]">

              {/* Line 1 */}
              <span className="block text-5xl leading-[1.05] text-slate-100 sm:text-6xl lg:text-[72px]">
                The Future of
              </span>

              {/* Line 2 */}
              <span className="mt-2 block text-5xl leading-[1.05] text-[#ffb21c] sm:text-6xl lg:text-[72px]">
                Cyber Security
              </span>

              {/* Line 3 */}
              <span className="mt-2 block text-5xl leading-[1.05] text-slate-100 sm:text-6xl lg:text-[72px]">
                Starts Here.
              </span>

            </h1>

            {/* Description */}
            <p className="mt-8 max-w-xl text-base leading-7 text-slate-400 sm:text-lg">
              Spam Shield AI analyzes suspicious URLs, emails, SMS,
              WhatsApp messages, QR codes, phone numbers and images
              to detect scams and explain the threat in real time.
            </p>

            {/* ================= BUTTONS ================= */}
            <div className="mt-9 flex flex-col gap-4 sm:flex-row">

              <button
                className="group flex items-center justify-center gap-3 rounded-xl bg-[#ffb21c] px-7 py-4 font-semibold text-[#07101f] shadow-[0_0_30px_rgba(255,178,28,0.2)] transition-all duration-300 hover:-translate-y-1 hover:bg-[#ffc044] hover:shadow-[0_0_45px_rgba(255,178,28,0.35)]"
              >
                Start Scanning

                <ArrowRight className="h-5 w-5 transition-transform duration-300 group-hover:translate-x-2" />
              </button>

              <button
                className="group flex items-center justify-center gap-3 rounded-xl border border-slate-700 bg-slate-900/50 px-7 py-4 font-semibold text-slate-200 backdrop-blur transition-all duration-300 hover:-translate-y-1 hover:border-cyan-400/40 hover:bg-slate-800/70"
              >
                Explore Protection

                <ShieldCheck className="h-5 w-5 text-cyan-400 transition-transform duration-300 group-hover:rotate-12" />
              </button>

            </div>

            {/* ================= TRUST ================= */}
            <div className="mt-9 flex flex-wrap gap-x-6 gap-y-3 text-sm text-slate-400">

              <span className="flex items-center gap-2">
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
                Enterprise Grade
              </span>

              <span className="hidden h-5 w-px bg-slate-700 sm:block" />

              <span className="flex items-center gap-2">
                <Lock className="h-4 w-4 text-emerald-400" />
                Your Data is Secure
              </span>

              <span className="hidden h-5 w-px bg-slate-700 sm:block" />

              <span className="flex items-center gap-2">
                <Activity className="h-4 w-4 text-emerald-400" />
                Real-time Protection
              </span>

            </div>
          </div>

          {/* ================= RIGHT SIDE ================= */}
          <div className="relative mx-auto w-full max-w-xl">

            {/* ================= CENTRAL SHIELD ================= */}
            <div className="pointer-events-none absolute left-1/2 top-1/2 z-0 -translate-x-1/2 -translate-y-1/2">

              <div className="flex h-72 w-72 items-center justify-center rounded-full border border-blue-500/20 bg-blue-500/5 shadow-[0_0_120px_rgba(37,99,235,0.12)] animate-pulse">

                <div className="flex h-52 w-52 items-center justify-center rounded-full border border-cyan-400/20">

                  <ShieldCheck className="h-24 w-24 text-cyan-400/70" />

                </div>

              </div>

            </div>

            {/* ================= CARDS ================= */}
            <div className="relative z-10 grid grid-cols-2 gap-4">

              {/* CARD 1 */}
              <div className="group min-h-[205px] rounded-2xl border border-emerald-400/30 bg-[#0b1628]/90 p-6 shadow-[0_0_35px_rgba(16,185,129,0.06)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-emerald-400/70 hover:bg-[#0e1d32] hover:shadow-[0_0_50px_rgba(16,185,129,0.18)]">

                <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-full border border-emerald-400/40 bg-emerald-400/10 transition-transform duration-300 group-hover:scale-110">

                  <Activity className="h-6 w-6 text-emerald-400" />

                </div>

                <p className="text-3xl font-bold text-emerald-400">
                  AI
                </p>

                <p className="mt-2 font-medium text-white">
                  Threat Detection
                </p>

                <p className="mt-2 text-sm leading-5 text-slate-400">
                  Intelligent scam analysis
                </p>

              </div>

              {/* CARD 2 */}
              <div className="group min-h-[205px] rounded-2xl border border-cyan-400/30 bg-[#0b1628]/90 p-6 shadow-[0_0_35px_rgba(34,211,238,0.06)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-cyan-400/70 hover:bg-[#0e1d32] hover:shadow-[0_0_50px_rgba(34,211,238,0.18)]">

                <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-full border border-cyan-400/40 bg-cyan-400/10 transition-transform duration-300 group-hover:scale-110">

                  <Bot className="h-6 w-6 text-cyan-400" />

                </div>

                <p className="text-2xl font-bold text-cyan-400">
                  Multi-Agent
                </p>

                <p className="mt-2 font-medium text-white">
                  AI Protection
                </p>

                <p className="mt-2 text-sm leading-5 text-slate-400">
                  Specialized detection agents
                </p>

              </div>

              {/* CARD 3 */}
              <div className="group min-h-[205px] rounded-2xl border border-orange-400/30 bg-[#0b1628]/90 p-6 shadow-[0_0_35px_rgba(251,146,60,0.06)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-orange-400/70 hover:bg-[#0e1d32] hover:shadow-[0_0_50px_rgba(251,146,60,0.18)]">

                <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-full border border-orange-400/40 bg-orange-400/10 transition-transform duration-300 group-hover:scale-110">

                  <Clock3 className="h-6 w-6 text-orange-400" />

                </div>

                <p className="text-3xl font-bold text-orange-400">
                  24/7
                </p>

                <p className="mt-2 font-medium text-white">
                  AI Monitoring
                </p>

                <p className="mt-2 text-sm leading-5 text-slate-400">
                  Always-on threat analysis
                </p>

              </div>

              {/* CARD 4 */}
              <div className="group min-h-[205px] rounded-2xl border border-purple-400/30 bg-[#0b1628]/90 p-6 shadow-[0_0_35px_rgba(168,85,247,0.06)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-purple-400/70 hover:bg-[#0e1d32] hover:shadow-[0_0_50px_rgba(168,85,247,0.18)]">

                <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-full border border-purple-400/40 bg-purple-400/10 transition-transform duration-300 group-hover:scale-110">

                  <Globe2 className="h-6 w-6 text-purple-400" />

                </div>

                <p className="text-3xl font-bold text-purple-400">
                  Global
                </p>

                <p className="mt-2 font-medium text-white">
                  Threat Intelligence
                </p>

                <p className="mt-2 text-sm leading-5 text-slate-400">
                  Threat intelligence analysis
                </p>

              </div>

            </div>
          </div>
        </div>

        {/* ================= ATTACK SURFACE ================= */}
        <div className="mt-16 rounded-2xl border border-slate-800 bg-[#081221]/80 p-6 backdrop-blur-xl transition-all duration-500 hover:border-slate-700">

          <div className="mb-7 text-center">

            <p className="text-xs font-semibold uppercase tracking-[0.35em] text-slate-400">
              Protecting Every Attack Surface
            </p>

          </div>

          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">

            <AttackSurface
              icon={<Globe2 />}
              title="URL"
              subtitle="Analysis"
              color="text-emerald-400"
            />

            <AttackSurface
              icon={<Mail />}
              title="Email"
              subtitle="Detection"
              color="text-cyan-400"
            />

            <AttackSurface
              icon={<MessageSquare />}
              title="SMS"
              subtitle="Scanning"
              color="text-yellow-400"
            />

            <AttackSurface
              icon={<MessageSquare />}
              title="WhatsApp"
              subtitle="Analysis"
              color="text-green-400"
            />

            <AttackSurface
              icon={<QrCode />}
              title="QR Code"
              subtitle="Scanning"
              color="text-purple-400"
            />

            <AttackSurface
              icon={<Phone />}
              title="Phone"
              subtitle="Intelligence"
              color="text-red-400"
            />

          </div>
        </div>

        {/* ================= BOTTOM ================= */}
        <div className="mt-14 text-center">

          <div className="inline-flex items-center gap-2 text-sm text-slate-500">

            <CheckCircle2 className="h-4 w-4 text-emerald-400" />

            Detect it. Understand it. Stay protected.

          </div>

        </div>

      </section>
    </main>
  );
}


/* =====================================================
   ATTACK SURFACE COMPONENT
===================================================== */

function AttackSurface({
  icon,
  title,
  subtitle,
  color,
}: {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
  color: string;
}) {
  return (
    <div className="group flex cursor-pointer items-center gap-3 rounded-xl p-3 transition-all duration-300 hover:bg-white/[0.04]">

      <div
        className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-slate-700 bg-slate-900/80 ${color} transition-all duration-300 group-hover:scale-110 group-hover:border-current`}
      >
        {React.cloneElement(icon as React.ReactElement, {
          className: "h-5 w-5",
        })}
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-200">
          {title}
        </p>

        <p className="text-xs text-slate-500">
          {subtitle}
        </p>
      </div>

    </div>
  );
}