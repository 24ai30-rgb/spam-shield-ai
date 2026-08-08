// app/training/page.tsx
"use client";
import jsPDF from "jspdf";
import { useMemo, useState } from "react";
import {
  Shield,
  GraduationCap,
  Trophy,
  Brain,
  Play,
  CheckCircle,
  XCircle,
  AlertTriangle,
  RotateCcw,
  ChevronRight,
  Sparkles,
} from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";
import {
  trainingQuestions,
  type Difficulty,
  type TrainingQuestion,
} from "@/lib/trainingData";

function shuffleArray<T>(array: T[]): T[] {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function getBadge(percentage: number): {
  label: string;
  color: string;
  glow: string;
} {
  if (percentage >= 90) {
    return {
      label: "Excellent",
      color: "text-green-400",
      glow: "shadow-[0_0_30px_rgba(74,222,128,0.35)]",
    };
  }
  if (percentage >= 70) {
    return {
      label: "Good",
      color: "text-cyan-400",
      glow: "shadow-[0_0_30px_rgba(34,211,238,0.35)]",
    };
  }
  if (percentage >= 50) {
    return {
      label: "Average",
      color: "text-yellow-400",
      glow: "shadow-[0_0_30px_rgba(250,204,21,0.35)]",
    };
  }
  return {
    label: "Needs Improvement",
    color: "text-red-400",
    glow: "shadow-[0_0_30px_rgba(248,113,113,0.35)]",
  };
}

type Stage = "intro" | "quiz" | "result";

interface AnsweredRecord {
  question: TrainingQuestion;
  selected: "Safe" | "Scam";
  isCorrect: boolean;
}

const TOTAL_QUESTIONS = 10;

export default function TrainingPage() {
  const [difficulty, setDifficulty] = useState<Difficulty>("Easy");
  const [stage, setStage] = useState<Stage>("intro");
  const [quizQuestions, setQuizQuestions] = useState<TrainingQuestion[]>([]);
  const [current, setCurrent] = useState(0);
  const [score, setScore] = useState(0);
  const [selected, setSelected] = useState<"Safe" | "Scam" | null>(null);
  const [answered, setAnswered] = useState<AnsweredRecord[]>([]);

  const question = quizQuestions[current];

  const progressPercent = useMemo(() => {
    if (quizQuestions.length === 0) return 0;
    return Math.round(((current + (selected ? 1 : 0)) / quizQuestions.length) * 100);
  }, [current, selected, quizQuestions.length]);

  const finalPercentage = useMemo(() => {
    if (quizQuestions.length === 0) return 0;
    return Math.round((score / quizQuestions.length) * 100);
  }, [score, quizQuestions.length]);

  const badge = getBadge(finalPercentage);

  const aiTips =
    finalPercentage >= 90
      ? [
          "Excellent! You can identify most cyber scams.",
          "Always verify URLs before clicking.",
          "Enable Two-Factor Authentication everywhere.",
        ]
      : finalPercentage >= 70
      ? [
          "Good awareness.",
          "Double-check unknown payment requests.",
          "Verify every banking message.",
        ]
      : finalPercentage >= 50
      ? [
          "Practice more phishing examples.",
          "Avoid shortened URLs.",
          "Never share OTP or UPI PIN.",
        ]
      : [
          "Complete this training again.",
          "Never trust urgent banking alerts.",
          "Always verify before making payments.",
        ];

  const weakTopics = answered
    .filter((item) => !item.isCorrect)
    .reduce((acc, item) => {
      const topic = item.question.type;
      acc[topic] = (acc[topic] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

  const recommendedTopics = Object.entries(weakTopics)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3);

  const circleCircumference = 2 * Math.PI * 70;
  const circleOffset =
    circleCircumference - (finalPercentage / 100) * circleCircumference;

  function handleStart(): void {
    const pool = trainingQuestions.filter((q) => q.difficulty === difficulty);
    const sourcePool = pool.length >= TOTAL_QUESTIONS ? pool : trainingQuestions;
    const shuffled = shuffleArray(sourcePool).slice(0, TOTAL_QUESTIONS);

    setQuizQuestions(shuffled);
    setCurrent(0);
    setScore(0);
    setSelected(null);
    setAnswered([]);
    setStage("quiz");
  }

  function handleAnswer(option: "Safe" | "Scam"): void {
    if (selected !== null || !question) return;

    const isCorrect = option === question.answer;
    setSelected(option);

    if (isCorrect) {
      setScore((prev) => prev + 1);
    }

    setAnswered((prev) => [
      ...prev,
      { question, selected: option, isCorrect },
    ]);
  }

  function handleNext(): void {
    if (current + 1 < quizQuestions.length) {
      setCurrent((prev) => prev + 1);
      setSelected(null);
    } else {
      setStage("result");
    }
  }

  const downloadCertificate = async () => {
    const doc = new jsPDF({
      orientation: "landscape",
      unit: "mm",
      format: "a4",
    });

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    const loadImageBase64 = (src: string): Promise<string> => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => {
          const canvas = document.createElement("canvas");
          canvas.width = img.naturalWidth || img.width;
          canvas.height = img.naturalHeight || img.height;
          const ctx = canvas.getContext("2d");
          if (ctx) {
            ctx.drawImage(img, 0, 0);
            resolve(canvas.toDataURL("image/png"));
          } else {
            reject(new Error("Canvas context unavailable"));
          }
        };
        img.onerror = (err) => reject(err);
        img.src = src;
      });
    };

    try {
      const bgDataUrl = await loadImageBase64("/certificate/certificate_template.png");
      doc.addImage(bgDataUrl, "PNG", 0, 0, pageWidth, pageHeight);
    } catch (error) {
      console.error("Failed to load certificate background template:", error);
    }

    let rank = "Needs Improvement";
    if (finalPercentage >= 90) {
      rank = "Elite Cyber Guardian";
    } else if (finalPercentage >= 80) {
      rank = "Cyber Defender";
    } else if (finalPercentage >= 60) {
      rank = "Scam Spotter";
    }

    const randomDigits = Math.floor(100000 + Math.random() * 900000);
    const certId = `SSAI-2026-${randomDigits}`;
    const currentDate = new Date().toLocaleDateString();
    
    // Safely check if 'user' is present in scope/context
    const recipientName =
      typeof user !== "undefined" && (user as { full_name?: string })?.full_name
        ? (user as { full_name: string }).full_name
        : "Participant";
    
    const totalQuestions = quizQuestions.length || 10;

    doc.setFont("times", "bold");
    doc.setFontSize(30);
    doc.setTextColor(11, 18, 32);
    doc.text(recipientName, pageWidth / 2, 82, { align: "center" });

    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.setTextColor(212, 175, 55);
    doc.text(rank, pageWidth / 2, 105, { align: "center" });

    doc.setFont("helvetica", "bold");
    doc.setFontSize(14);
    doc.setTextColor(11, 18, 32);
    doc.text(`${score} / ${totalQuestions}`, 75, 123, {
  align: "center",
});
    doc.text(`${finalPercentage}%`, 148, 123, {
  align: "center",
});

    doc.setFont("helvetica", "normal");
    doc.setFontSize(11);
    doc.setTextColor(11, 18, 32);
    doc.text(currentDate, 92, 158, {
  align: "center",
});
    doc.text(certId, 208, 158, {
  align: "center",
});

    doc.save("SpamShield-Certificate.pdf");
  };

  function handleRestart(): void {
    setStage("intro");
    setQuizQuestions([]);
    setCurrent(0);
    setScore(0);
    setSelected(null);
    setAnswered([]);
  }

  return (
    <AppShell
      title="AI Scam Training"
      subtitle="Learn to identify cyber scams with realistic AI-generated scenarios."
    >
      <div className="space-y-6">
        {stage === "intro" && (
          <>
            <div className="card p-8 relative overflow-hidden">
              <div className="absolute -top-24 -right-24 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl" />
              <div className="absolute -bottom-24 -left-24 w-72 h-72 bg-yellow-500/5 rounded-full blur-3xl" />

              <div className="flex items-center justify-between relative z-10">
                <div className="max-w-2xl">
                  <p className="text-cyan-400 font-semibold text-sm mb-2 flex items-center gap-2">
                    <Sparkles size={16} />
                    AI Cyber Awareness Platform
                  </p>

                  <h1 className="text-4xl font-bold mb-4">
                    Become a Scam Detection Expert
                  </h1>

                  <p className="text-fog-400 leading-7">
                    Practice with realistic phishing emails, fake websites,
                    banking scams, WhatsApp fraud, QR scams and investment
                    scams. Improve your cyber awareness before real attackers
                    target you.
                  </p>

                  <button className="btn-primary mt-6" onClick={handleStart}>
                    <Play size={18} />
                    Start Training
                  </button>
                </div>

                <Shield
                  size={140}
                  className="text-cyan-500 opacity-40 hidden lg:block"
                />
              </div>
            </div>

            <div className="card p-6">
              <h2 className="text-xl font-semibold mb-4">Select Difficulty</h2>

              <div className="flex gap-4 flex-wrap">
                {(["Easy", "Medium", "Hard"] as Difficulty[]).map((item) => (
                  <button
                    key={item}
                    onClick={() => setDifficulty(item)}
                    className={`px-6 py-3 rounded-xl border transition-all duration-200 font-medium ${
                      difficulty === item
                        ? "bg-yellow-500 text-black border-yellow-500 shadow-[0_0_20px_rgba(250,204,21,0.4)]"
                        : "border-fog-400/20 hover:border-yellow-500 hover:bg-yellow-500/5"
                    }`}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-5">
              <div className="card p-5 hover:border-cyan-400/40 transition-all duration-200 hover:-translate-y-1">
                <Brain className="text-cyan-400 mb-4" />
                <h3 className="font-semibold text-lg">AI Scenarios</h3>
                <p className="text-fog-400 mt-2 text-sm">
                  Practice using realistic cyber scam examples.
                </p>
              </div>

              <div className="card p-5 hover:border-green-400/40 transition-all duration-200 hover:-translate-y-1">
                <GraduationCap className="text-green-400 mb-4" />
                <h3 className="font-semibold text-lg">Learn Instantly</h3>
                <p className="text-fog-400 mt-2 text-sm">
                  AI explains why every answer is correct or wrong.
                </p>
              </div>

              <div className="card p-5 hover:border-blue-400/40 transition-all duration-200 hover:-translate-y-1">
                <CheckCircle className="text-blue-400 mb-4" />
                <h3 className="font-semibold text-lg">Real Examples</h3>
                <p className="text-fog-400 mt-2 text-sm">
                  Emails, SMS, URLs, QR Codes and fake banking alerts.
                </p>
              </div>

              <div className="card p-5 hover:border-yellow-400/40 transition-all duration-200 hover:-translate-y-1">
                <Trophy className="text-yellow-500 mb-4" />
                <h3 className="font-semibold text-lg">Awareness Score</h3>
                <p className="text-fog-400 mt-2 text-sm">
                  Get your Cyber Awareness Score after training.
                </p>
              </div>
            </div>
          </>
        )}

        {stage === "quiz" && question && (
          <div className="space-y-6">
            <div className="card p-6">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium text-fog-400">
                  Question {current + 1} of {quizQuestions.length}
                </span>
                <span className="text-sm font-semibold text-yellow-400">
                  Score: {score}
                </span>
              </div>

              <div className="w-full h-2 bg-fog-400/10 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-400 to-yellow-400 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>

            <div className="card p-8 backdrop-blur-xl bg-white/5 border border-white/10">
              <div className="flex items-center gap-3 mb-5">
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                  {question.type}
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-fog-400/10 text-fog-400 border border-fog-400/20">
                  {question.difficulty}
                </span>
              </div>

              <h3 className="text-xl font-semibold leading-8 mb-8">
                {question.question}
              </h3>

              <div className="grid sm:grid-cols-2 gap-4">
                <button
                  onClick={() => handleAnswer("Safe")}
                  disabled={selected !== null}
                  className={`flex items-center justify-center gap-2 px-6 py-4 rounded-xl border-2 font-semibold text-lg transition-all duration-200 ${
                    selected === null
                      ? "border-green-500/30 text-green-400 hover:bg-green-500/10 hover:border-green-500 hover:-translate-y-0.5"
                      : selected === "Safe" && question.answer === "Safe"
                      ? "border-green-500 bg-green-500/20 text-green-300"
                      : selected === "Safe" && question.answer !== "Safe"
                      ? "border-red-500 bg-red-500/20 text-red-300"
                      : question.answer === "Safe"
                      ? "border-green-500 bg-green-500/10 text-green-300"
                      : "border-fog-400/10 text-fog-400/40"
                  } ${selected !== null ? "cursor-not-allowed" : "cursor-pointer"}`}
                >
                  <CheckCircle size={20} />
                  Safe
                </button>

                <button
                  onClick={() => handleAnswer("Scam")}
                  disabled={selected !== null}
                  className={`flex items-center justify-center gap-2 px-6 py-4 rounded-xl border-2 font-semibold text-lg transition-all duration-200 ${
                    selected === null
                      ? "border-red-500/30 text-red-400 hover:bg-red-500/10 hover:border-red-500 hover:-translate-y-0.5"
                      : selected === "Scam" && question.answer === "Scam"
                      ? "border-green-500 bg-green-500/20 text-green-300"
                      : selected === "Scam" && question.answer !== "Scam"
                      ? "border-red-500 bg-red-500/20 text-red-300"
                      : question.answer === "Scam"
                      ? "border-green-500 bg-green-500/10 text-green-300"
                      : "border-fog-400/10 text-fog-400/40"
                  } ${selected !== null ? "cursor-not-allowed" : "cursor-pointer"}`}
                >
                  <XCircle size={20} />
                  Scam
                </button>
              </div>

              {selected !== null && (
                <div className="mt-8 space-y-5 animate-[fadeIn_0.3s_ease-out]">
                  <div
                    className={`flex items-center gap-3 p-4 rounded-xl border ${
                      selected === question.answer
                        ? "bg-green-500/10 border-green-500/30"
                        : "bg-red-500/10 border-red-500/30"
                    }`}
                  >
                    {selected === question.answer ? (
                      <CheckCircle className="text-green-400 shrink-0" size={22} />
                    ) : (
                      <XCircle className="text-red-400 shrink-0" size={22} />
                    )}
                    <p className="font-semibold">
                      {selected === question.answer
                        ? "Correct! "
                        : "Incorrect. "}
                      The right answer is{" "}
                      <span
                        className={
                          question.answer === "Scam"
                            ? "text-red-300"
                            : "text-green-300"
                        }
                      >
                        {question.answer}
                      </span>
                      .
                    </p>
                  </div>

                  <div className="card p-5 bg-cyan-500/5 border border-cyan-500/20">
                    <div className="flex items-center gap-2 mb-2">
                      <Brain size={18} className="text-cyan-400" />
                      <h4 className="font-semibold text-cyan-400">
                        AI Explanation
                      </h4>
                    </div>
                    <p className="text-fog-400 text-sm leading-6">
                      {question.explanation}
                    </p>
                  </div>

                  {question.threatIndicators.length > 0 && (
                    <div className="card p-5 bg-yellow-500/5 border border-yellow-500/20">
                      <div className="flex items-center gap-2 mb-3">
                        <AlertTriangle size={18} className="text-yellow-400" />
                        <h4 className="font-semibold text-yellow-400">
                          Threat Indicators
                        </h4>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {question.threatIndicators.map((indicator) => (
                          <span
                            key={indicator}
                            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-yellow-500/10 text-yellow-300 border border-yellow-500/20"
                          >
                            {indicator}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <button
                    className="btn-primary w-full sm:w-auto"
                    onClick={handleNext}
                  >
                    {current + 1 < quizQuestions.length
                      ? "Next Question"
                      : "View Results"}
                    <ChevronRight size={18} />
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {stage === "result" && (
          <div className="space-y-6">
            <div className="card p-10 flex flex-col items-center text-center relative overflow-hidden">
              <div
                className={`absolute inset-0 opacity-20 blur-3xl ${badge.glow}`}
              />

              <p className="text-cyan-400 font-semibold text-sm mb-2 relative z-10">
                🎯 Training Complete
              </p>

              <h2 className="text-3xl font-bold mb-8 relative z-10">
                Your Cyber Awareness Score
              </h2>

              <div className="relative w-48 h-48 mb-8 z-10">
                <svg className="w-full h-full -rotate-90" viewBox="0 0 160 160">
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="12"
                    className="text-fog-400/10"
                  />
                  <circle
                    cx="80"
                    cy="80"
                    r="70"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="12"
                    strokeLinecap="round"
                    strokeDasharray={circleCircumference}
                    strokeDashoffset={circleOffset}
                    className={`${badge.color} transition-all duration-1000 ease-out`}
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-4xl font-bold">
                    {finalPercentage}%
                  </span>
                  <span className="text-sm text-fog-400 mt-1">
                    {score}/{quizQuestions.length} Correct
                  </span>
                </div>
              </div>

              <span
                className={`px-6 py-2.5 rounded-full font-semibold text-lg border relative z-10 ${badge.color} border-current bg-current/10`}
              >
                {badge.label}
              </span>

              <button
                className="btn-primary mt-8 relative z-10"
                onClick={handleRestart}
              >
                <RotateCcw size={18} />
                Restart Training
              </button>

              {finalPercentage >= 80 && (
                <button
                  onClick={downloadCertificate}
                  className="btn-primary mt-4 relative z-10"
                >
                  🏆 Download Certificate
                </button>
              )}
            </div>

            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-5 flex items-center gap-2">
                <Brain className="text-cyan-400" />
                AI Personalized Tips
              </h3>

              <div className="space-y-3">
                {aiTips.map((tip, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4"
                  >
                    {tip}
                  </div>
                ))}
              </div>
            </div>

            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-5">
                📊 Weak Topics Analysis
              </h3>

              {recommendedTopics.length === 0 ? (
                <div className="rounded-xl border border-green-500/20 bg-green-500/10 p-4">
                  🎉 Excellent! No weak topics found.
                </div>
              ) : (
                <div className="space-y-3">
                  {recommendedTopics.map(([topic, count]) => (
                    <div
                      key={topic}
                      className="flex items-center justify-between rounded-xl border border-yellow-500/20 bg-yellow-500/5 p-4"
                    >
                      <div>
                        <p className="font-semibold">{topic}</p>
                        <p className="text-sm text-fog-400">
                          Incorrect Answers: {count}
                        </p>
                      </div>

                      <span className="rounded-full bg-red-500/20 px-3 py-1 text-sm text-red-400">
                        Needs Practice
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-5">Question Review</h3>
              <div className="space-y-3">
                {answered.map((record, index) => (
                  <div
                    key={record.question.id}
                    className={`p-4 rounded-xl border flex items-start gap-3 ${
                      record.isCorrect
                        ? "bg-green-500/5 border-green-500/20"
                        : "bg-red-500/5 border-red-500/20"
                    }`}
                  >
                    {record.isCorrect ? (
                      <CheckCircle
                        size={20}
                        className="text-green-400 shrink-0 mt-0.5"
                      />
                    ) : (
                      <XCircle
                        size={20}
                        className="text-red-400 shrink-0 mt-0.5"
                      />
                    )}
                    <div className="flex-1">
                      <p className="text-sm font-medium text-fog-400 mb-1">
                        Question {index + 1} • {record.question.type}
                      </p>
                      <p className="text-sm leading-6">
                        {record.question.question}
                      </p>
                      <p className="text-xs text-fog-400 mt-2">
                        Your answer:{" "}
                        <span
                          className={
                            record.isCorrect ? "text-green-300" : "text-red-300"
                          }
                        >
                          {record.selected}
                        </span>{" "}
                        • Correct answer:{" "}
                        <span className="text-cyan-300">
                          {record.question.answer}
                        </span>
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}