"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import {
  Loader2,
  UploadCloud,
  Search,
  Shield,
  CheckCircle2,
  Sparkles,
} from "lucide-react";

import * as Icons from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";

import { scanApi } from "@/lib/api";

import {
  cx,
  FILE_INPUT_TYPES,
  INPUT_TYPES,
} from "@/lib/utils";

export default function UploadCenterPage() {

  const router = useRouter();

  const [selectedType, setSelectedType] =
    useState("url");

  const [textValue, setTextValue] =
    useState("");

  const [file, setFile] =
    useState<File | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [progress, setProgress] =
    useState(0);

  const [currentStep, setCurrentStep] =
    useState("");

  const isFileType =
    FILE_INPUT_TYPES.has(selectedType);

  const scanSteps = [

    "Input Validation",

    "Extracting Information",

    "Google Safe Browsing",

    "SSL Verification",

    "WHOIS Lookup",

    "Threat Intelligence",

    "AI Agent 1 / 13",

    "AI Agent 2 / 13",

    "AI Agent 3 / 13",

    "AI Agent 4 / 13",

    "AI Agent 5 / 13",

    "AI Agent 6 / 13",

    "AI Agent 7 / 13",

    "AI Agent 8 / 13",

    "AI Agent 9 / 13",

    "AI Agent 10 / 13",

    "AI Agent 11 / 13",

    "AI Agent 12 / 13",

    "AI Agent 13 / 13",

    "Risk Calculation",

    "Generating PDF Report",

  ];

  useEffect(() => {

    if (!loading) return;

    let index = 0;

    setCurrentStep(scanSteps[0]);

    setProgress(0);

    const timer = setInterval(() => {

      index++;

      if (index < scanSteps.length) {

        setCurrentStep(scanSteps[index]);

        setProgress(
          Math.round(
            ((index + 1) / scanSteps.length) * 100
          )
        );

      } else {

        clearInterval(timer);

      }

    }, 350);

    return () => clearInterval(timer);

  }, [loading]);

  async function handleSubmit() {

    setError(null);

    if (isFileType && !file) {

      return setError(
        "Please upload a file."
      );

    }

    if (!isFileType && !textValue.trim()) {

      return setError(
        "Please enter something to scan."
      );

    }

    setLoading(true);

    try {
           const { data } = isFileType
  ? await scanApi.createFileScan(selectedType, file as File)
  : await scanApi.createTextScan(selectedType, textValue);

toast.success("Scan Completed Successfully!");

router.push(`/history/${data.id}`);

    } catch (err: any) {

      setError(
        err?.response?.data?.error?.message ||
        "Scan failed. Please try again."
      );

    } finally {

      setLoading(false);

      setProgress(0);

      setCurrentStep("");

    }

  }

  return (

    <AppShell
      title="Upload Center"
      subtitle="Submit any content for instant multi-agent scam analysis"
    >

      {/* HERO */}

      <div className="mb-6 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-white/10 p-8">

        <div className="flex items-center justify-between">

          <div>

            <div className="flex items-center gap-2 text-cyan-400">

              <Sparkles size={18} />

              <span className="text-sm font-semibold">

                AI Powered Scan Center

              </span>

            </div>

            <h2 className="text-4xl font-bold mt-3">

              Scan Anything

            </h2>

            <p className="text-fog-400 mt-3 max-w-2xl">

              Upload URLs, emails, QR codes,
              screenshots, banking messages,
              shopping links, investment offers
              and more.

            </p>

          </div>

          <Shield
            size={90}
            className="text-cyan-500 opacity-20"
          />

        </div>

      </div>

      {/* PROGRESS */}

      {loading && (

        <div className="card p-6 mb-6">

          <div className="flex justify-between mb-3">

            <span className="font-semibold">

              AI Scan Progress

            </span>

            <span>

              {progress}%

            </span>

          </div>

          <div className="h-3 rounded-full bg-slate-700 overflow-hidden">

            <div
              className="h-full bg-cyan-500 transition-all duration-300"
              style={{
                width: `${progress}%`,
              }}
            />

          </div>

          <div className="mt-4 flex items-center gap-2">

            <Loader2
              className="animate-spin text-cyan-400"
              size={18}
            />

            <span>

              {currentStep}

            </span>

          </div>

        </div>

      )}

      {/* QUICK SEARCH */}

      <div className="card p-4 mb-6 flex items-center gap-3">

        <Search
          size={18}
          className="text-fog-400"
        />

        <input
          placeholder="Paste URL, phone number or message..."
          className="flex-1 bg-transparent outline-none"
          onChange={(e) => {

            setTextValue(e.target.value);

            if (isFileType)
              setSelectedType("url");

          }}
        />

      </div>

      <div className="grid lg:grid-cols-3 gap-6">

             {/* TYPE SELECTOR */}

        <div className="lg:col-span-1">

          <h3 className="text-sm font-semibold mb-3">

            What are you scanning?

          </h3>

          <div className="grid grid-cols-2 gap-3">

            {INPUT_TYPES.map(({ value, label, icon }) => {

              const Icon =
                (Icons as any)[icon] ||
                Icons.HelpCircle;

              const active =
                selectedType === value;

              return (

                <button
                  key={value}
                  onClick={() => {

                    setSelectedType(value);

                    setError(null);

                  }}
                  className={cx(

                    "card flex flex-col items-center gap-3 py-5 transition",

                    active
                      ? "border-cyan-500 bg-cyan-500/10 text-cyan-400"
                      : "hover:border-white/20"

                  )}
                >

                  <Icon size={24} />

                  <span>

                    {label}

                  </span>

                </button>

              );

            })}

          </div>

        </div>

        {/* SCAN PANEL */}

        <div className="lg:col-span-2">

          <div className="card p-6">

            <h3 className="text-lg font-bold mb-5">

              {
                INPUT_TYPES.find(
                  t => t.value === selectedType
                )?.label
              }

            </h3>

            {isFileType ? (

              <label className="flex flex-col items-center justify-center border-2 border-dashed border-white/10 rounded-2xl py-16 cursor-pointer hover:border-cyan-500 transition">

                <UploadCloud
                  size={36}
                  className="text-cyan-400"
                />

                <p className="mt-4 text-sm text-fog-400">

                  {
                    file
                      ? file.name
                      : "Click to upload or drag & drop"
                  }

                </p>

                <input
                  type="file"
                  className="hidden"
                  accept="image/*,.pdf,.doc,.docx"
                  onChange={(e) =>
                    setFile(
                      e.target.files?.[0] || null
                    )
                  }
                />

              </label>

            ) : (

              <textarea

                rows={8}

                value={textValue}

                onChange={(e) =>
                  setTextValue(e.target.value)
                }

                placeholder={placeholderFor(selectedType)}

                className="w-full rounded-xl border border-white/10 bg-transparent px-4 py-3 resize-none"

              />

            )}

            {loading && (

              <div className="mt-6 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-5">

                <div className="flex items-center gap-2 mb-4">

                  <Loader2
                    className="animate-spin text-cyan-400"
                    size={18}
                  />

                  <span className="font-semibold">

                    AI Agents Working...

                  </span>

                </div>

                <div className="space-y-2">

                  {scanSteps
                    .slice(0, Math.ceil(progress / 5))
                    .map((step) => (

                      <div
                        key={step}
                        className="flex items-center gap-2 text-sm"
                      >

                        <CheckCircle2
                          size={16}
                          className="text-green-400"
                        />

                        <span>

                          {step}

                        </span>

                      </div>

                  ))}

                </div>

              </div>

            )}

            {error && (

              <p className="mt-4 text-red-400 text-sm">

                {error}

              </p>

            )}

            <button
              onClick={handleSubmit}
              disabled={loading}
              className="btn-primary w-full mt-6"
            >

              {loading ? (

                <Loader2
                  className="animate-spin"
                  size={18}
                />

              ) : (

                <Search
                  size={18}
                />

              )}

              {loading
                ? "Running 13 AI Agents..."
                : "Run Scan"}

            </button>

          </div>

        </div>

      </div> 
          </AppShell>

  );

}

function placeholderFor(type: string): string {

  switch (type) {

    case "url":
      return "https://example.com/suspicious-link";

    case "email":
      return "Paste the complete email here...";

    case "phone":
      return "+91 9876543210";

    case "sms":
      return "Paste the SMS here...";

    case "whatsapp":
      return "Paste the WhatsApp message here...";

    case "job":
      return "Paste the job offer...";

    case "banking":
      return "Paste the banking message...";

    case "shopping":
      return "Paste the shopping website or product link...";

    case "investment":
      return "Paste the investment offer...";

    case "upi":
      return "example@upi";

    case "document":
      return "Upload your PDF or document...";

    case "image":
      return "Upload an image...";

    case "qr":
      return "Upload the QR code image...";

    default:
      return "Paste content to scan...";
  }

}