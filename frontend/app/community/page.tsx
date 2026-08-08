"use client";

import { useState } from "react";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {

  Flag,
  Loader2,
  TrendingUp,
  Shield,
  Sparkles,
  AlertTriangle,
  Users,
  Search,

} from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";

import { communityApi } from "@/lib/api";

export default function CommunityPage() {

  const queryClient = useQueryClient();

  const [inputType, setInputType] =
    useState("url");

  const [rawValue, setRawValue] =
    useState("");

  const [description, setDescription] =
    useState("");

  const [search, setSearch] =
    useState("");

  const { data: trending } = useQuery({

    queryKey: ["trending-scams"],

    queryFn: () =>
      communityApi.trending().then(
        (r) => r.data
      ),

  });

  const submitMutation = useMutation({

    mutationFn: () =>

      communityApi.submitReport({

        input_type: inputType,

        raw_value: rawValue,

        description,

      }),

    onSuccess: () => {

      setRawValue("");

      setDescription("");

      queryClient.invalidateQueries({

        queryKey: ["trending-scams"],

      });

    },

  });

  const filteredTrending =
    trending?.filter((item: any) =>
      item.raw_value
        ?.toLowerCase()
        .includes(search.toLowerCase())
    ) ?? [];

  return (

<AppShell

title="Community Intelligence"

subtitle="Crowdsourced Cyber Threat Network"

>

{/* HERO */}

<div className="mb-8 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-white/10 p-8">

<div className="flex justify-between items-center">

<div>

<div className="flex items-center gap-2 text-cyan-400">

<Sparkles size={18}/>

<span>

Community Powered Threat Intelligence

</span>

</div>

<h1 className="text-4xl font-bold mt-3">

Help Protect Millions

</h1>

<p className="mt-4 text-fog-400 max-w-2xl">

Every scam report strengthens
Spam Shield AI and helps
protect the entire community
from cyber criminals.

</p>

</div>

<Shield

size={90}

className="text-cyan-500 opacity-30"

/>

</div>

</div>

{/* STATS */}

<div className="grid md:grid-cols-3 gap-5 mb-8">

<div className="card p-6">

<Users

className="text-cyan-400 mb-4"

size={28}

/>

<h2 className="text-4xl font-bold">

{trending?.length ?? 0}

</h2>

<p className="text-fog-400">

Community Reports

</p>

</div>

<div className="card p-6">

<AlertTriangle

className="text-red-400 mb-4"

size={28}

/>

<h2 className="text-4xl font-bold">

LIVE

</h2>

<p className="text-fog-400">

Threat Feed

</p>

</div>

<div className="card p-6">

<TrendingUp

className="text-green-400 mb-4"

size={28}

/>

<h2 className="text-4xl font-bold">

24/7

</h2>

<p className="text-fog-400">

AI Monitoring

</p>

</div>

</div>

<div className="grid lg:grid-cols-2 gap-6">
        {/* REPORT FORM */}

        <div className="card p-6">

          <div className="flex items-center gap-3 mb-6">

            <Flag
              className="text-red-400"
              size={24}
            />

            <div>

              <h2 className="text-xl font-bold">

                Report a Scam

              </h2>

              <p className="text-fog-400 text-sm">

                Help protect the community by reporting cyber scams.

              </p>

            </div>

          </div>

          <div className="space-y-4">

            <select
              value={inputType}
              onChange={(e) =>
                setInputType(e.target.value)
              }
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3"
            >

              {[
                "url",
                "email",
                "phone",
                "sms",
                "job",
                "banking",
                "shopping",
                "investment",
              ].map((type) => (

                <option
                  key={type}
                  value={type}
                >

                  {type}

                </option>

              ))}

            </select>

            <input
              value={rawValue}
              onChange={(e) =>
                setRawValue(e.target.value)
              }
              placeholder="Enter suspicious URL, phone number or message..."
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3"
            />

            <textarea
              rows={5}
              value={description}
              onChange={(e) =>
                setDescription(
                  e.target.value
                )
              }
              placeholder="Describe what happened..."
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 resize-none"
            />

            <button
              onClick={() =>
                submitMutation.mutate()
              }
              disabled={
                submitMutation.isPending ||
                !rawValue
              }
              className="btn-primary w-full"
            >

              {submitMutation.isPending && (

                <Loader2
                  className="animate-spin"
                  size={18}
                />

              )}

              Submit Community Report

            </button>

            {submitMutation.isSuccess && (

              <div className="rounded-xl bg-green-500/10 border border-green-500/20 p-4">

                <p className="text-green-400">

                  ✅ Thank you!

                </p>

                <p className="text-fog-400 text-sm mt-2">

                  Your report has been shared with the community.

                </p>

              </div>

            )}

          </div>

        </div>

        {/* TRENDING */}

        <div className="card p-6">

          <div className="flex items-center justify-between mb-6">

            <div>

              <h2 className="text-xl font-bold">

                Trending Threats

              </h2>

              <p className="text-fog-400 text-sm">

                Live community intelligence

              </p>

            </div>

            <TrendingUp
              className="text-cyan-400"
              size={24}
            />

          </div>

          <div className="relative mb-5">

            <Search
              className="absolute left-3 top-3 text-fog-400"
              size={18}
            />

            <input
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              placeholder="Search reported scams..."
              className="w-full rounded-xl border border-white/10 bg-slate-900 pl-10 pr-4 py-3"
            />

          </div>

          <div className="space-y-4">

            {filteredTrending.length === 0 && (

              <p className="text-fog-400">

                No reports found.

              </p>

            )}

            {filteredTrending.map(
              (item: any, index: number) => (

                <div
                  key={index}
                  className="rounded-2xl border border-white/10 bg-slate-900 p-5 hover:border-cyan-500 transition"
                >

                  <div className="flex justify-between items-start">

                    <div className="min-w-0">

                      <p className="font-mono text-sm break-all">

                        {item.raw_value}

                      </p>

                      <p className="text-fog-400 text-xs mt-2 capitalize">

                        {item.input_type}

                      </p>

                    </div>

                    <span
                      className={`badge ${
                        item.severity === "high"
                          ? "badge-high_risk"
                          : "badge-suspicious"
                      }`}
                    >

                      {item.severity}

                    </span>

                  </div>

                  <div className="flex justify-between mt-4 text-sm">

                    <span>

                      👥 {item.report_count} Reports

                    </span>

                    <span className="text-cyan-400">

                      LIVE

                    </span>

                  </div>

                </div>

              )
            )}

          </div>

        </div>

      </div>
            {/* COMMUNITY SAFETY */}

      <div className="mt-8 rounded-3xl border border-cyan-500/20 bg-gradient-to-r from-cyan-500/10 to-slate-900 p-8">

        <div className="flex items-center gap-3 mb-6">

          <Shield
            className="text-cyan-400"
            size={28}
          />

          <h2 className="text-2xl font-bold">

            Community Safety Guidelines

          </h2>

        </div>

        <div className="grid md:grid-cols-2 gap-6">

          <div>

            <h3 className="font-semibold mb-3">

              Before Reporting

            </h3>

            <ul className="space-y-2 text-sm text-fog-400">

              <li>✅ Verify the information first.</li>

              <li>✅ Include useful details.</li>

              <li>✅ Report only genuine scams.</li>

              <li>✅ Protect your personal information.</li>

            </ul>

          </div>

          <div>

            <h3 className="font-semibold mb-3">

              Never Share

            </h3>

            <ul className="space-y-2 text-sm text-fog-400">

              <li>❌ OTPs</li>

              <li>❌ Passwords</li>

              <li>❌ Bank PIN</li>

              <li>❌ Debit/Credit Card CVV</li>

            </ul>

          </div>

        </div>

      </div>

      {/* THREAT INTELLIGENCE */}

      <div className="card p-6 mt-6">

        <div className="flex items-center gap-3 mb-4">

          <TrendingUp
            className="text-red-400"
            size={24}
          />

          <h2 className="text-xl font-bold">

            Live Threat Intelligence

          </h2>

        </div>

        <p className="text-fog-400 leading-7">

          Every verified report submitted by the community strengthens
          Spam Shield AI's detection engine.

          As reports increase, our AI becomes better at identifying:

        </p>

        <div className="grid md:grid-cols-3 gap-4 mt-6">

          {[
            "🎣 Phishing Websites",
            "💳 Banking Fraud",
            "📱 Fake SMS",
            "🛒 Shopping Scams",
            "💼 Fake Jobs",
            "📈 Investment Fraud",
          ].map((item) => (

            <div
              key={item}
              className="rounded-xl border border-white/10 bg-slate-900 p-4 text-center"
            >

              {item}

            </div>

          ))}

        </div>

      </div>

      {/* FOOTER */}

      <div className="mt-8 rounded-2xl border border-green-500/20 bg-green-500/5 p-6 text-center">

        <h2 className="text-xl font-bold">

          🌍 Together We Build a Safer Internet

        </h2>

        <p className="text-fog-400 mt-3">

          Community reports help Spam Shield AI detect new cyber threats
          faster and protect users worldwide.

        </p>

      </div>

    </AppShell>

  );

}