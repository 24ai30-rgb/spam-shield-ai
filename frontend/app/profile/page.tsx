"use client";

import { useQuery } from "@tanstack/react-query";

import {
  User,
  Shield,
  Activity,
  FileText,
  Crown,
  Mail,
  Calendar,
} from "lucide-react";

import { AppShell } from "@/components/layout/AppShell";

import { authApi, dashboardApi } from "@/lib/api";

export default function ProfilePage() {
  const { data: me } = useQuery({
    queryKey: ["me"],
    queryFn: () => authApi.me().then((r) => r.data),
  });

  const { data: stats } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: () => dashboardApi.stats().then((r) => r.data),
  });

  return (
    <AppShell title="My Profile" subtitle="Manage your Spam Shield AI account">
      <div className="grid lg:grid-cols-3 gap-6">
        {/* PROFILE CARD */}
        <div className="lg:col-span-1">
          <div className="card p-8">
            <div className="flex flex-col items-center">
              <div className="h-28 w-28 rounded-full bg-cyan-500/10 flex items-center justify-center">
                <User className="text-cyan-400" size={56} />
              </div>

              <h2 className="text-2xl font-bold mt-5">
                {me?.full_name ?? "User"}
              </h2>

              <div className="flex items-center gap-2 text-fog-400 mt-2">
                <Mail size={16} />
                {me?.email}
              </div>

              <div className="mt-5 flex items-center gap-2 rounded-full bg-yellow-500/10 border border-yellow-500/20 px-4 py-2">
                <Crown className="text-yellow-400" size={18} />
                <span className="text-yellow-400 text-sm font-semibold">
                  Free Plan
                </span>
              </div>
            </div>

            <div className="border-t border-white/10 my-6" />

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Calendar size={18} />
                  <span>Member Since</span>
                </div>
                <span className="text-fog-400">2026</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Shield size={18} />
                  <span>Safety Score</span>
                </div>
                <span className="text-cyan-400 font-bold">
                  {stats?.cyber_safety_score ?? 70}/100
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* ACCOUNT OVERVIEW */}
        <div className="lg:col-span-2">
          <div className="grid md:grid-cols-2 gap-5">
            <div className="card p-6">
              <Activity className="text-green-400 mb-3" size={24} />
              <h2 className="text-4xl font-bold">{stats?.total_scans ?? 0}</h2>
              <p className="text-fog-400 mt-2">Total Scans</p>
            </div>

            <div className="card p-6">
              <Shield className="text-red-400 mb-3" size={24} />
              <h2 className="text-4xl font-bold">{stats?.scams_blocked ?? 0}</h2>
              <p className="text-fog-400 mt-2">Threats Blocked</p>
            </div>

            <div className="card p-6">
              <FileText className="text-cyan-400 mb-3" size={24} />
              <h2 className="text-4xl font-bold">{stats?.total_scans ?? 0}</h2>
              <p className="text-fog-400 mt-2">Reports Generated</p>
            </div>

            <div className="card p-6">
              <User className="text-yellow-400 mb-3" size={24} />
              <h2 className="text-4xl font-bold">
                {stats?.community_reports ?? 0}
              </h2>
              <p className="text-fog-400 mt-2">Community Reports</p>
            </div>
          </div>

          <div className="card p-6 mt-6">
            <h3 className="text-xl font-bold mb-4">Account Actions</h3>
            <div className="flex flex-wrap gap-4">
              <button className="btn-primary">Edit Profile</button>

              <button
                onClick={() => {
                  localStorage.removeItem("access_token");
                  localStorage.removeItem("refresh_token");
                  window.location.href = "/login";
                }}
                className="rounded-xl border border-red-500/30 bg-red-500/10 px-5 py-3 text-red-400 hover:bg-red-500/20 transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}

