import { Check } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";

const TIERS = [
  {
    name: "Free",
    price: "$0",
    tier: "free",
    features: [
      "20 scans / hour",
      "All 13 AI agents",
      "Basic PDF reports",
      "7-day scan history",
      "Community reporting",
    ],
  },
  {
    name: "Premium",
    price: "$9/mo",
    tier: "premium",
    highlighted: true,
    features: [
      "Unlimited scans",
      "Real-time monitoring & watchlists",
      "Full detailed PDF reports",
      "Unlimited history",
      "Priority AI chatbot",
      "Browser extension",
    ],
  },
  {
    name: "Business",
    price: "Custom",
    tier: "business",
    features: [
      "Everything in Premium",
      "API access with SLA",
      "Bulk scanning",
      "Webhook alerts",
      "White-labeled reports",
      "Dedicated account manager",
    ],
  },
];

export default function PremiumPage() {
  return (
    <AppShell>
      <div className="min-h-screen bg-void-900 px-6 py-12">
        <div className="mx-auto max-w-6xl">
          {/* Header */}
          <div className="mb-12 text-center">
            <p className="mb-3 text-sm font-semibold uppercase tracking-widest text-beacon-500">
              Pricing
            </p>

            <h1 className="font-display text-4xl font-bold text-paper md:text-5xl">
              Choose Your Protection
            </h1>

            <p className="mx-auto mt-4 max-w-2xl text-fog-400">
              Choose the plan that fits your cybersecurity needs.
              Start protecting yourself with Spam Shield AI.
            </p>
          </div>

          {/* Pricing Cards */}
          <div className="grid gap-6 md:grid-cols-3">
            {TIERS.map((t) => (
              <div
                key={t.tier}
                className={`relative flex flex-col rounded-2xl border p-6 transition-all duration-300 hover:-translate-y-1 ${
                  t.highlighted
                    ? "border-beacon-500 bg-void-800 shadow-[0_0_30px_rgba(212,175,55,0.12)]"
                    : "border-void-600 bg-void-800"
                }`}
              >
                {/* Popular Badge */}
                {t.highlighted && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-beacon-500 px-4 py-1 text-xs font-bold text-void-950">
                    Most Popular
                  </div>
                )}

                {/* Plan Name */}
                <h2 className="font-display text-2xl font-bold text-paper">
                  {t.name}
                </h2>

                {/* Price */}
                <div className="mt-3">
                  <span className="text-4xl font-bold text-beacon-500">
                    {t.price}
                  </span>
                </div>

                {/* Features */}
                <div className="mt-8 flex-1 space-y-4">
                  {t.features.map((f) => (
                    <div key={f} className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-signal-500/15">
                        <Check className="h-3.5 w-3.5 text-signal-500" />
                      </div>

                      <span className="text-sm text-fog-300">{f}</span>
                    </div>
                  ))}
                </div>

                {/* Button */}
                <button
                  className={
                    t.highlighted
                      ? "btn-primary mt-8 w-full"
                      : "btn-ghost mt-8 w-full"
                  }
                >
                  {t.tier === "free" ? "Current Plan" : "Upgrade"}
                </button>
              </div>
            ))}
          </div>

          {/* Bottom Note */}
          <div className="mt-10 text-center">
            <p className="text-sm text-fog-400">
              Secure your digital life with{" "}
              <span className="font-semibold text-beacon-500">
                Spam Shield AI
              </span>
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}