"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shield, Loader2 } from "lucide-react";
import { authApi } from "@/lib/api";
import { useAuthStore } from "@/lib/store";

export default function LoginPage() {
  const router = useRouter();
  const setUser = useAuthStore((s) => s.setUser);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { data } = await authApi.login({ email, password });
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      const me = await authApi.me();
      setUser(me.data);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err?.response?.data?.error?.message || "Invalid email or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-void-900 px-4">
      <div className="w-full max-w-sm">
        <div className="flex items-center justify-center gap-2 mb-8">
          <Shield className="h-8 w-8 text-beacon-500" strokeWidth={2.5} />
          <span className="font-display text-xl font-bold text-paper">Spam Shield AI</span>
        </div>

        <div className="card bg-void-800 border-void-600 p-8 text-paper">
          <h1 className="text-xl font-bold mb-1">Welcome back</h1>
          <p className="text-sm text-fog-400 mb-6">Sign in to continue protecting yourself.</p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="text-xs font-medium text-fog-300">Email</label>
              <input
                type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full rounded-lg border border-void-600 bg-void-900 px-3 py-2.5 text-sm focus:border-beacon-500 focus:outline-none"
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-fog-300">Password</label>
              <input
                type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                className="mt-1 w-full rounded-lg border border-void-600 bg-void-900 px-3 py-2.5 text-sm focus:border-beacon-500 focus:outline-none"
                placeholder="••••••••"
              />
            </div>
            {error && <p className="text-xs text-alert-500">{error}</p>}
            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading && <Loader2 className="animate-spin" size={16} />}
              Sign In
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-fog-400">
            No account? <Link href="/register" className="text-beacon-500 font-medium">Create one</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
