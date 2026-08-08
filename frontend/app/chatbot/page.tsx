"use client";

import { useState, useRef, useEffect } from "react";

import {
  Bot,
  Loader2,
  Send,
  User,
  Sparkles,
  Shield,
  Copy,
  ThumbsUp,
  ThumbsDown,
} from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";

import { chatbotApi } from "@/lib/api";

interface Message {

  role: "user" | "assistant";

  content: string;

}

export default function ChatbotPage() {

  const [messages, setMessages] = useState<Message[]>([

    {

      role: "assistant",

      content: `👋 Welcome to Spam Shield AI

I am your AI Cyber Security Assistant.

I can help you analyze:

• URLs

• Emails

• Phone Numbers

• UPI IDs

• QR Codes

• WhatsApp Messages

• SMS

• Banking Fraud

• Fake Shopping Websites

• Investment Scams

Paste anything suspicious below.`,

    },

  ]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({

      behavior: "smooth",

    });

  }, [messages]);

  async function send() {

    if (!input.trim() || loading) return;

    const userMessage: Message = {

      role: "user",

      content: input,

    };

    const history = messages.map(

      (m) => `${m.role}: ${m.content}`

    );

    setMessages((m) => [

      ...m,

      userMessage,

    ]);

    setInput("");

    setLoading(true);

    try {

      const { data } =

        await chatbotApi.sendMessage(

          userMessage.content,

          history,

        );

      setMessages((m) => [

        ...m,

        {

          role: "assistant",

          content: data.reply,

        },

      ]);

    } catch {

      setMessages((m) => [

        ...m,

        {

          role: "assistant",

          content:
            "⚠️ AI service is temporarily unavailable.",

        },

      ]);

    } finally {

      setLoading(false);

    }

  }

  return (

    <AppShell
      title="AI Assistant"
      subtitle="Enterprise Cyber Security Assistant"
    >

      {/* HERO */}

      <div className="mb-6 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-white/10 p-8">

        <div className="flex items-center gap-4">

          <div className="h-16 w-16 rounded-2xl bg-cyan-500/10 flex items-center justify-center">

            <Shield

              className="text-cyan-400"

              size={32}

            />

          </div>

          <div>

            <div className="flex items-center gap-2">

              <Sparkles

                className="text-yellow-400"

                size={18}

              />

              <span className="text-cyan-400 text-sm font-semibold">

                Multi-Agent AI Assistant

              </span>

            </div>

            <h2 className="text-3xl font-bold mt-2">

              Spam Shield AI Chat

            </h2>

            <p className="text-fog-400 mt-2">

              Powered by Gemini AI +
              Enterprise Threat Intelligence

            </p>

          </div>

        </div>

      </div>

      {/* QUICK PROMPTS */}

      <div className="grid md:grid-cols-3 gap-4 mb-6">

        {[
          "Is this URL safe?",
          "Analyze this email",
          "How can I avoid UPI scams?",
        ].map((prompt) => (

          <button

            key={prompt}

            onClick={() => setInput(prompt)}

            className="card p-5 hover:border-cyan-500 transition-all text-left"

          >

            <p className="font-semibold">

              {prompt}

            </p>

          </button>

        ))}

      </div>

      {/* CHAT CONTAINER */}

      <div className="card flex flex-col h-[68vh]">
              <div className="flex-1 overflow-y-auto p-6 space-y-6">

          {messages.map((message, index) => (

            <div
              key={index}
              className={`flex gap-4 ${
                message.role === "user"
                  ? "justify-end"
                  : ""
              }`}
            >

              {message.role === "assistant" && (

                <div className="h-10 w-10 rounded-2xl bg-cyan-500/10 flex items-center justify-center shrink-0">

                  <Bot
                    className="text-cyan-400"
                    size={18}
                  />

                </div>

              )}

              <div
                className={`max-w-[78%] rounded-2xl px-5 py-4 shadow-lg ${
                  message.role === "user"
                    ? "bg-cyan-500 text-slate-950"
                    : "bg-slate-800 border border-white/10"
                }`}
              >

                <p className="whitespace-pre-wrap leading-7 text-sm">

                  {message.content}

                </p>

                {message.role === "assistant" && (

                  <div className="flex items-center gap-3 mt-4">

                    <button className="hover:text-cyan-400 transition">

                      <Copy size={15} />

                    </button>

                    <button className="hover:text-green-400 transition">

                      <ThumbsUp size={15} />

                    </button>

                    <button className="hover:text-red-400 transition">

                      <ThumbsDown size={15} />

                    </button>

                  </div>

                )}

              </div>

              {message.role === "user" && (

                <div className="h-10 w-10 rounded-2xl bg-white/10 flex items-center justify-center shrink-0">

                  <User size={18} />

                </div>

              )}

            </div>

          ))}

          {loading && (

            <div className="flex gap-4">

              <div className="h-10 w-10 rounded-2xl bg-cyan-500/10 flex items-center justify-center">

                <Bot
                  className="text-cyan-400"
                  size={18}
                />

              </div>

              <div className="rounded-2xl bg-slate-800 border border-white/10 px-5 py-4">

                <div className="flex items-center gap-3">

                  <Loader2
                    className="animate-spin"
                    size={18}
                  />

                  <span className="text-sm text-fog-400">

                    AI is analyzing...

                  </span>

                </div>

              </div>

            </div>

          )}

          <div ref={bottomRef} />

        </div>

        {/* INPUT */}

        <div className="border-t border-white/10 p-5">

          <div className="flex items-center gap-3">

            <input
              value={input}
              onChange={(e) =>
                setInput(e.target.value)
              }
              onKeyDown={(e) =>
                e.key === "Enter" && send()
              }
              placeholder="Paste URL, Email, SMS, QR, Phone Number or ask a cyber security question..."
              className="flex-1 rounded-2xl border border-white/10 bg-slate-900 px-5 py-4 outline-none focus:border-cyan-500 transition"
            />

            <button
              onClick={send}
              disabled={loading}
              className="btn-primary px-6 py-4"
            >

              <Send size={18} />

            </button>

          </div>

          <p className="text-xs text-fog-400 mt-3">

            Your conversations are processed securely.
            Never share passwords, OTPs or sensitive personal information.

          </p>

        </div>

      </div>
            {/* AI CAPABILITIES */}

      <div className="grid md:grid-cols-4 gap-4 mt-6">

        <div className="card p-5">

          <Shield
            className="text-green-400 mb-3"
            size={24}
          />

          <h3 className="font-semibold">

            URL Detection

          </h3>

          <p className="text-xs text-fog-400 mt-2">

            Detect phishing, fake login pages,
            malicious redirects and suspicious domains.

          </p>

        </div>

        <div className="card p-5">

          <Bot
            className="text-cyan-400 mb-3"
            size={24}
          />

          <h3 className="font-semibold">

            AI Reasoning

          </h3>

          <p className="text-xs text-fog-400 mt-2">

            Gemini AI explains every decision
            using understandable language.

          </p>

        </div>

        <div className="card p-5">

          <Sparkles
            className="text-yellow-400 mb-3"
            size={24}
          />

          <h3 className="font-semibold">

            Scam Intelligence

          </h3>

          <p className="text-xs text-fog-400 mt-2">

            Detect fake banking,
            investment,
            shopping,
            QR and UPI scams.

          </p>

        </div>

        <div className="card p-5">

          <Shield
            className="text-red-400 mb-3"
            size={24}
          />

          <h3 className="font-semibold">

            Safety Advisor

          </h3>

          <p className="text-xs text-fog-400 mt-2">

            Get personalized cyber security
            recommendations after every analysis.

          </p>

        </div>

      </div>

      {/* QUICK QUESTIONS */}

      <div className="card p-6 mt-6">

        <h3 className="text-lg font-bold mb-4">

          Suggested Questions

        </h3>

        <div className="flex flex-wrap gap-3">

          {[
            "Is this website safe?",
            "Analyze this UPI ID",
            "Check this email",
            "Is this SMS a scam?",
            "How to avoid phishing?",
            "Banking fraud tips",
          ].map((item) => (

            <button
              key={item}
              onClick={() => setInput(item)}
              className="rounded-xl border border-white/10 px-4 py-2 hover:border-cyan-500 hover:text-cyan-400 transition"
            >

              {item}

            </button>

          ))}

        </div>

      </div>

      {/* FOOTER */}

      <div className="mt-8 rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6 text-center">

        <h2 className="text-xl font-bold">

          🛡 Spam Shield AI Assistant

        </h2>

        <p className="text-fog-400 mt-3">

          Powered by Multi-Agent AI,
          Gemini AI,
          Threat Intelligence,
          Explainable AI
          and Enterprise Cyber Security Models.

        </p>

      </div>

    </AppShell>

  );

}