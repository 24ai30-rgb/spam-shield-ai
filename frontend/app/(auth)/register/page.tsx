"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shield, Loader2 } from "lucide-react";
import { authApi } from "../../../lib/api";
import { useAuthStore } from "../../../lib/store";

export default function RegisterPage() {
  const router = useRouter();
  const setUser = useAuthStore((s) => s.setUser);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    setLoading(true);

    try {
      const { data } = await authApi.register({
        full_name: fullName,
        email,
        password,
      });

      if (data?.access_token) {
        localStorage.setItem("access_token", data.access_token);
      }

      if (data?.refresh_token) {
        localStorage.setItem("refresh_token", data.refresh_token);
      }

      if (data?.user) {
        setUser(data.user);
        router.push("/dashboard");
      } else {
        router.push("/login");
      }
    } catch (err: any) {
      setError(
        err?.response?.data?.error?.message ||
          err?.response?.data?.message ||
          "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-void-950 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">
        <div className="flex items-center justify-center gap-2 mb-6">
          <Shield className="text-beacon-500" size={28} />

          <span className="text-xl font-bold text-paper">
            Spam Shield AI
          </span>
        </div>

        <div className="card bg-void-800 border-void-600 p-8 text-paper">
          <h1 className="text-xl font-bold mb-1">
            Create your account
          </h1>

          <p className="text-sm text-fog-400 mb-6">
            Start protecting yourself from online scams.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="text-xs font-medium text-fog-300">
                Full Name
              </label>

              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="mt-1 w-full rounded-lg border border-void-600 bg-void-900 px-3 py-2.5 text-sm text-paper focus:border-beacon-500 focus:outline-none"
                placeholder="Your full name"
              />
            </div>

            <div>
              <label className="text-xs font-medium text-fog-300">
                Email
              </label>

              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full rounded-lg border border-void-600 bg-void-900 px-3 py-2.5 text-sm text-paper focus:border-beacon-500 focus:outline-none"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label className="text-xs font-medium text-fog-300">
                Password
              </label>

              <input
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 w-full rounded-lg border border-void-600 bg-void-900 px-3 py-2.5 text-sm text-paper focus:border-beacon-500 focus:outline-none"
                placeholder="••••••••"
              />
            </div>

            <div>
              <label className="text-xs font-medium text-fog-300">
                Confirm Password
              </label>

              <input
                type="password"
                required
                minLength={6}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="mt-1 w-full rounded-lg border border-void-600 bg-void-900 px-3 py-2.5 text-sm text-paper focus:border-beacon-500 focus:outline-none"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <p className="text-xs text-alert-500">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full flex items-center justify-center gap-2"
            >
              {loading && (
                <Loader2
                  className="animate-spin"
                  size={16}
                />
              )}

              {loading ? "Creating Account..." : "Create Account"}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-fog-400">
            Already have an account?{" "}
            <Link
              href="/login"
              className="text-beacon-500 font-medium"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}