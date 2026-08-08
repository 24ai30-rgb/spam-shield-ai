import Link from "next/link";

import {

  Shield,
  ArrowRight,
  Link2,
  Mail,
  Phone,
  QrCode,
  Image,
  Briefcase,
  Landmark,
  ShoppingBag,
  TrendingUp,
  Sparkles,
  ShieldCheck,
  Activity,
  BrainCircuit,
  Globe,
  Lock,

} from "lucide-react";

const MODULES = [

  { icon: Link2, label: "URL Shield" },

  { icon: Mail, label: "Email Shield" },

  { icon: Phone, label: "Phone Shield" },

  { icon: QrCode, label: "QR Shield" },

  { icon: Image, label: "Screenshot Shield" },

  { icon: Briefcase, label: "Job Shield" },

  { icon: Landmark, label: "Banking Shield" },

  { icon: ShoppingBag, label: "Shopping Shield" },

  { icon: TrendingUp, label: "Investment Shield" },

];

export default function LandingPage() {

  return (

<div className="min-h-screen bg-void-900 text-paper overflow-hidden">

<nav className="flex items-center justify-between px-6 md:px-16 py-6 border-b border-white/5">

<div className="flex items-center gap-3">

<div className="h-12 w-12 rounded-2xl bg-beacon-500/10 flex items-center justify-center">

<Shield
size={28}
className="text-beacon-500"
/>

</div>

<div>

<h1 className="font-bold text-xl">

Spam Shield AI

</h1>

<p className="text-xs text-fog-400">

Enterprise Cyber Defense

</p>

</div>

</div>

<div className="flex gap-4">

<Link
href="/login"
className="btn-ghost"
>

Sign In

</Link>

<Link
href="/register"
className="btn-primary"
>

Get Started

</Link>

</div>

</nav>

<section className="relative overflow-hidden px-6 py-24 md:px-16">

  {/* Animated background */}
  <div className="pointer-events-none absolute inset-0">

    <div className="absolute left-[15%] top-[10%] h-[500px] w-[500px] rounded-full bg-beacon-500/10 blur-[130px] animate-pulse" />

<div className="absolute right-[5%] top-[20%] h-[450px] w-[450px] rounded-full bg-cyan-500/10 blur-[130px] animate-pulse" />

    <div className="absolute left-[15%] top-[10%] h-[500px] w-[500px] rounded-full bg-beacon-500/10 blur-[130px] animate-pulse" />

    <div className="absolute right-[5%] top-[20%] h-[450px] w-[450px] rounded-full bg-cyan-500/10 blur-[130px] animate-pulse" />

    <div className="absolute bottom-0 left-[40%] h-[300px] w-[400px] rounded-full bg-purple-500/5 blur-[120px]" />

  </div>

  <div className="relative mx-auto grid max-w-7xl items-center gap-16 lg:grid-cols-[1.05fr_0.95fr]">

    {/* ================= LEFT ================= */}
    <div className="relative z-10">

      {/* Badge */}
      <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-green-500/30 bg-green-500/10 px-4 py-2 text-sm text-green-300 transition-all duration-300 hover:border-green-400/60 hover:bg-green-500/15">

        <Sparkles
          size={18}
          className="animate-pulse"
        />

        <span>13 AI Agents Protecting You</span>

      </div>

      {/* Heading */}
      <h1 className="font-bold tracking-[-0.04em]">

        <span className="block text-5xl leading-[1.05] text-paper sm:text-6xl lg:text-7xl">
          The Future of
        </span>

        <span className="mt-2 block text-5xl leading-[1.05] text-beacon-500 sm:text-6xl lg:text-7xl">
          Cyber Security
        </span>

        <span className="mt-2 block text-5xl leading-[1.05] text-paper sm:text-6xl lg:text-7xl">
          Starts Here.
        </span>

      </h1>

      {/* Description */}
      <p className="mt-8 max-w-xl text-lg leading-8 text-fog-300">
        Spam Shield AI is an enterprise-grade multi-agent
        cyber security platform that detects phishing,
        fake banking portals, investment fraud, job scams,
        QR attacks, malicious URLs, spam calls and social
        engineering in real time.
      </p>

      {/* Buttons */}
<div className="mt-10 flex flex-col gap-4 sm:flex-row">

  <Link
    href="/register"
    className="group btn-primary flex items-center justify-center gap-2 px-8 py-4 text-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_0_35px_rgba(255,178,28,0.25)]"
  >
    Start Scanning

    <ArrowRight
      size={20}
      className="transition-transform duration-300 group-hover:translate-x-1"
    />
  </Link>

  <Link
    href="/premium"
    className="group btn-ghost flex items-center justify-center gap-2 px-8 py-4 text-lg transition-all duration-300 hover:-translate-y-1"
  >
    Premium

    <ShieldCheck
      size={20}
      className="text-cyan-400 transition-transform duration-300 group-hover:rotate-12"
    />
  </Link>

  <a
    href="/extensions/safe_browse.zip"
    download="Spam-Shield-Browser-Extension.zip"
    className="group btn-ghost flex items-center justify-center gap-2 px-8 py-4 text-lg transition-all duration-300 hover:-translate-y-1"
  >
    Download Extension

    <ShieldCheck
      size={20}
      className="text-green-400 transition-transform duration-300 group-hover:scale-110"
    />
  </a>

</div>

      {/* Trust indicators */}
      <div className="mt-8 flex flex-wrap gap-x-6 gap-y-3 text-sm text-fog-400">

        <span className="flex items-center gap-2">
          <ShieldCheck
            size={16}
            className="text-green-400"
          />
          Enterprise Grade
        </span>

        <span className="hidden h-5 w-px bg-white/10 sm:block" />

        <span className="flex items-center gap-2">
          <Lock
            size={16}
            className="text-cyan-400"
          />
          Privacy First
        </span>

        <span className="hidden h-5 w-px bg-white/10 sm:block" />

        <span className="flex items-center gap-2">
          <Activity
            size={16}
            className="text-beacon-500"
          />
          Real-time Detection
        </span>

      </div>

    </div>

    {/* ================= RIGHT ================= */}
    <div className="relative mx-auto w-full max-w-xl">

      {/* Central glow */}
      <div className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">

        <div className="h-72 w-72 rounded-full border border-cyan-400/10 bg-cyan-400/5 shadow-[0_0_120px_rgba(34,211,238,0.12)] animate-pulse" />

      </div>

      {/* Cards */}
      <div className="relative z-10 grid grid-cols-2 gap-5">

        {/* Card 1 */}
        <div className="group rounded-2xl border border-green-400/20 bg-slate-950/70 p-6 shadow-[0_0_35px_rgba(16,185,129,0.04)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-green-400/60 hover:bg-slate-900/80 hover:shadow-[0_0_45px_rgba(16,185,129,0.15)]">

          <Activity
            size={30}
            className="mb-5 text-green-400 transition-transform duration-300 group-hover:scale-110"
          />

          <h2 className="text-4xl font-bold text-green-400">
            99.2%
          </h2>

          <p className="mt-2 text-sm leading-6 text-fog-400">
            Threat Detection Accuracy
          </p>

        </div>

        {/* Card 2 */}
        <div className="group rounded-2xl border border-cyan-400/20 bg-slate-950/70 p-6 shadow-[0_0_35px_rgba(34,211,238,0.04)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-cyan-400/60 hover:bg-slate-900/80 hover:shadow-[0_0_45px_rgba(34,211,238,0.15)]">

          <ShieldCheck
            size={30}
            className="mb-5 text-cyan-400 transition-transform duration-300 group-hover:scale-110"
          />

          <h2 className="text-4xl font-bold text-cyan-400">
            13
          </h2>

          <p className="mt-2 text-sm leading-6 text-fog-400">
            AI Detection Agents
          </p>

        </div>

        {/* Card 3 */}
        <div className="group rounded-2xl border border-yellow-400/20 bg-slate-950/70 p-6 shadow-[0_0_35px_rgba(250,204,21,0.04)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-yellow-400/60 hover:bg-slate-900/80 hover:shadow-[0_0_45px_rgba(250,204,21,0.15)]">

          <BrainCircuit
            size={30}
            className="mb-5 text-yellow-400 transition-transform duration-300 group-hover:scale-110"
          />

          <h2 className="text-4xl font-bold text-yellow-400">
            24/7
          </h2>

          <p className="mt-2 text-sm leading-6 text-fog-400">
            AI Monitoring
          </p>

        </div>

        {/* Card 4 */}
        <div className="group rounded-2xl border border-red-400/20 bg-slate-950/70 p-6 shadow-[0_0_35px_rgba(248,113,113,0.04)] backdrop-blur-xl transition-all duration-500 hover:-translate-y-2 hover:border-red-400/60 hover:bg-slate-900/80 hover:shadow-[0_0_45px_rgba(248,113,113,0.15)]">

          <Globe
            size={30}
            className="mb-5 text-red-400 transition-transform duration-300 group-hover:scale-110"
          />

          <h2 className="text-4xl font-bold text-red-400">
            Global
          </h2>

          <p className="mt-2 text-sm leading-6 text-fog-400">
            Threat Intelligence
          </p>

        </div>

      </div>

    </div>

  </div>

</section>
      {/* WHY SPAM SHIELD */}

      <section className="px-6 md:px-16 pb-24">

        <div className="max-w-6xl mx-auto">

          <div className="text-center mb-14">

            <span className="text-beacon-500 font-semibold">

              WHY CHOOSE US

            </span>

            <h2 className="text-5xl font-bold mt-3">

              Enterprise Grade Protection

            </h2>

            <p className="text-fog-300 mt-5 max-w-3xl mx-auto">

              Unlike traditional scam detectors,
              Spam Shield AI combines multiple AI agents,
              threat intelligence and explainable AI
              to produce accurate cyber threat reports.

            </p>

          </div>

          <div className="grid lg:grid-cols-3 gap-6">

            <div className="card p-8">

              <ShieldCheck
                className="text-green-400 mb-5"
                size={34}
              />

              <h3 className="text-xl font-bold">

                Multi-Agent Detection

              </h3>

              <p className="mt-4 text-fog-300">

                13 independent AI agents analyze every
                investigation and combine results
                into one intelligent verdict.

              </p>

            </div>

            <div className="card p-8">

              <BrainCircuit
                className="text-yellow-400 mb-5"
                size={34}
              />

              <h3 className="text-xl font-bold">

                Explainable AI

              </h3>

              <p className="mt-4 text-fog-300">

                Every decision includes reasoning,
                evidence,
                confidence score
                and recommended actions.

              </p>

            </div>

            <div className="card p-8">

              <Lock
                className="text-cyan-400 mb-5"
                size={34}
              />

              <h3 className="text-xl font-bold">

                Privacy First

              </h3>

              <p className="mt-4 text-fog-300">

                Your investigations remain private.
                Sensitive data is processed securely
                without unnecessary storage.

              </p>

            </div>

          </div>

        </div>

      </section>

      {/* MODULES */}

      <section className="px-6 md:px-16 pb-24">

        <div className="text-center">

          <span className="text-beacon-500 font-semibold">

            COMPLETE THREAT COVERAGE

          </span>

          <h2 className="text-5xl font-bold mt-4">

            Detect Every Type Of Scam

          </h2>

        </div>

        <div className="max-w-6xl mx-auto grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mt-14">

          {MODULES.map(({ icon: Icon, label }) => (

            <div
              key={label}
              className="card p-6 text-center hover:scale-105 transition-all duration-300"
            >

              <div className="mx-auto h-16 w-16 rounded-2xl bg-beacon-500/10 flex items-center justify-center">

                <Icon
                  size={30}
                  className="text-beacon-500"
                />

              </div>

              <h3 className="mt-5 font-semibold">

                {label}

              </h3>

            </div>

          ))}

        </div>

      </section>

      {/* LIVE STATS */}

      <section className="px-6 md:px-16 pb-24">

        <div className="max-w-6xl mx-auto rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-white/10 p-10">

          <div className="grid md:grid-cols-4 gap-8 text-center">

            <div>

              <h2 className="text-5xl font-bold text-green-400">

                99.2%

              </h2>

              <p className="text-fog-400 mt-3">

                Detection Accuracy

              </p>

            </div>

            <div>

              <h2 className="text-5xl font-bold text-cyan-400">

                13

              </h2>

              <p className="text-fog-400 mt-3">

                AI Agents

              </p>

            </div>

            <div>

              <h2 className="text-5xl font-bold text-yellow-400">

                24/7

              </h2>

              <p className="text-fog-400 mt-3">

                Monitoring

              </p>

            </div>

            <div>

              <h2 className="text-5xl font-bold text-red-400">

                Global

              </h2>

              <p className="text-fog-400 mt-3">

                Threat Intelligence

              </p>

            </div>

          </div>

        </div>

      </section>
            {/* HOW IT WORKS */}

      <section className="px-6 md:px-16 pb-24">

        <div className="max-w-6xl mx-auto">

          <div className="text-center mb-14">

            <span className="text-beacon-500 font-semibold">

              SIMPLE PROCESS

            </span>

            <h2 className="text-5xl font-bold mt-3">

              How Spam Shield AI Works

            </h2>

          </div>

          <div className="grid md:grid-cols-3 gap-8">

            {[
              {
                step: "01",
                title: "Upload",
                body: "Paste a URL, upload a screenshot, QR code, email or suspicious message.",
              },
              {
                step: "02",
                title: "AI Analysis",
                body: "13 specialized AI agents investigate using threat intelligence, WHOIS, SSL, Safe Browsing and Explainable AI.",
              },
              {
                step: "03",
                title: "Investigation Report",
                body: "Receive a professional cyber forensic report with risk score, evidence and recommended actions.",
              },
            ].map((item) => (

              <div
                key={item.step}
                className="card p-8 text-center hover:scale-105 transition-all duration-300"
              >

                <div className="mx-auto h-16 w-16 rounded-full bg-beacon-500/10 flex items-center justify-center text-2xl font-bold text-beacon-500">

                  {item.step}

                </div>

                <h3 className="mt-6 text-xl font-bold">

                  {item.title}

                </h3>

                <p className="mt-4 text-fog-300">

                  {item.body}

                </p>

              </div>

            ))}

          </div>

        </div>

      </section>

      {/* TESTIMONIALS */}

      <section className="px-6 md:px-16 pb-24">

        <div className="max-w-6xl mx-auto">

          <div className="text-center mb-14">

            <span className="text-beacon-500 font-semibold">

              TRUSTED AI PLATFORM

            </span>

            <h2 className="text-5xl font-bold mt-3">

              Why People Love Spam Shield AI

            </h2>

          </div>

          <div className="grid lg:grid-cols-3 gap-6">

            <div className="card p-8">

              <p className="text-fog-300 leading-7">

                "The explainable AI reports make it
                incredibly easy to understand why a
                website or message is dangerous."

              </p>

              <p className="mt-6 font-semibold">

                Cyber Security Student

              </p>

            </div>

            <div className="card p-8">

              <p className="text-fog-300 leading-7">

                "Professional PDF reports are useful
                for cyber crime investigations and
                documentation."

              </p>

              <p className="mt-6 font-semibold">

                Security Researcher

              </p>

            </div>

            <div className="card p-8">

              <p className="text-fog-300 leading-7">

                "The multi-agent architecture gives
                much more confidence than traditional
                scam detection systems."

              </p>

              <p className="mt-6 font-semibold">

                AI Developer

              </p>

            </div>

          </div>

        </div>

      </section>

      {/* FINAL CTA */}

      <section className="px-6 md:px-16 pb-24">

        <div className="max-w-6xl mx-auto rounded-3xl bg-gradient-to-r from-beacon-500/20 to-cyan-500/20 border border-beacon-500/30 p-12 text-center">

          <h2 className="text-5xl font-bold">

            Ready To Stay Safe Online?

          </h2>

          <p className="mt-6 text-lg text-fog-300 max-w-2xl mx-auto">

            Start scanning suspicious links,
            messages, QR codes and screenshots
            with enterprise-grade AI protection.

          </p>

          <div className="flex flex-wrap justify-center gap-5 mt-10">

            <Link
              href="/register"
              className="btn-primary px-8 py-4 text-lg"
            >

              Start Free Scan

              <ArrowRight size={20} />

            </Link>

            <Link
              href="/login"
              className="btn-ghost px-8 py-4 text-lg"
            >

              Sign In

            </Link>

          </div>

        </div>

      </section>

      {/* FOOTER */}

      <footer className="border-t border-white/10 px-6 md:px-16 py-10">

        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">

          <div>

            <div className="flex items-center gap-3">

              <Shield
                className="text-beacon-500"
                size={28}
              />

              <h2 className="text-xl font-bold">

                Spam Shield AI

              </h2>

            </div>

            <p className="text-fog-400 mt-3">

              Enterprise Multi-Agent Cyber Threat
              Detection Platform.

            </p>

          </div>

          <div className="text-sm text-fog-400">

            © {new Date().getFullYear()} Spam Shield AI

            <br />

            Built for Hackathon 2026

          </div>

        </div>

      </footer>

    </div>

  );

}