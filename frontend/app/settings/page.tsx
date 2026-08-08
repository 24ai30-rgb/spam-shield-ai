"use client";

import { useState } from "react";

import {
  Shield,
  Bell,
  Moon,
  Lock,
  KeyRound,
  Trash2,
  Save,
} from "lucide-react";

import { useAuthStore } from "@/lib/store";
import { AppShell } from "@/components/layout/AppShell";
import { useTheme } from "@/components/layout/ThemeProvider";

export default function SettingsPage() {

  const { user } = useAuthStore();

  const {
  theme,
  mode,
  setMode,
} = useTheme();

  const [emailAlerts, setEmailAlerts] = useState(true);

  const [weeklyDigest, setWeeklyDigest] = useState(true);

  const [communityAlerts, setCommunityAlerts] = useState(true);

  const [privacyMode, setPrivacyMode] = useState(false);

  const [password, setPassword] = useState({
    current: "",
    new: "",
    confirm: "",
  });

  return (

    <AppShell
      title="Settings"
      subtitle="Manage your account and preferences"
    >

      {/* HERO */}

      <div className="mb-6 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-white/10 p-8">

        <div className="flex items-center justify-between">

          <div>

            <div className="flex items-center gap-2 text-cyan-400">

              <Shield size={18} />

              <span className="text-sm font-semibold">

                Enterprise Security Settings

              </span>

            </div>

            <h2 className="text-3xl font-bold mt-3">

              Account Preferences

            </h2>

            <p className="text-fog-400 mt-3">

              Manage your profile, notifications,
              privacy and security settings.

            </p>

          </div>

          <Shield
            size={80}
            className="text-cyan-500 opacity-20"
          />

        </div>

      </div>

      <div className="space-y-6">

        {/* PROFILE */}

        <div className="card p-6">

          <h3 className="text-lg font-bold mb-5">

            Profile

          </h3>

          <div className="grid md:grid-cols-2 gap-5">

            <Field
              label="Full Name"
              value={user?.full_name || "—"}
            />

            <Field
              label="Email"
              value={user?.email || "—"}
            />

            <Field
              label="Plan"
              value={user?.plan_tier || "Free"}
              capitalize
            />

            <Field
              label="Role"
              value={user?.role || "User"}
              capitalize
            />

          </div>

        </div>

        {/* APPEARANCE */}

        <div className="card p-6">

          <div className="flex items-center justify-between">

            <div>

              <div className="flex items-center gap-2">

                <Moon
                  className="text-yellow-400"
                  size={20}
                />

                <h3 className="font-semibold">

                  Appearance

                </h3>

              </div>

              <p className="text-sm text-fog-400 mt-2">

                Select your preferred theme.

              </p>

            </div>

         <div className="space-y-3">

  <label className="flex items-center gap-3">
    <input
      type="radio"
      checked={mode === "light"}
      onChange={() => setMode("light")}
    />
    <span>☀️ Light</span>
  </label>

  <label className="flex items-center gap-3">
    <input
      type="radio"
      checked={mode === "dark"}
      onChange={() => setMode("dark")}
    />
    <span>🌙 Dark</span>
  </label>

  <label className="flex items-center gap-3">
    <input
      type="radio"
      checked={mode === "auto"}
      onChange={() => setMode("auto")}
    />
    <span>🕒 Auto (Time Based)</span>
  </label>

</div>
            

          </div>

        </div>
                {/* NOTIFICATIONS */}

        <div className="card p-6">

          <div className="flex items-center gap-2 mb-5">

            <Bell
              className="text-cyan-400"
              size={20}
            />

            <h3 className="text-lg font-bold">

              Notification Preferences

            </h3>

          </div>

          <div className="space-y-4">

            <ToggleRow
              title="High Risk Scan Alerts"
              description="Receive alerts whenever Spam Shield detects a dangerous threat."
              checked={emailAlerts}
              onChange={() =>
                setEmailAlerts(!emailAlerts)
              }
            />

            <ToggleRow
              title="Weekly Cyber Safety Digest"
              description="Receive a weekly report of your cyber safety activity."
              checked={weeklyDigest}
              onChange={() =>
                setWeeklyDigest(!weeklyDigest)
              }
            />

            <ToggleRow
              title="Community Threat Updates"
              description="Get notified when new scams become trending."
              checked={communityAlerts}
              onChange={() =>
                setCommunityAlerts(!communityAlerts)
              }
            />

          </div>

        </div>

        {/* PRIVACY */}

        <div className="card p-6">

          <div className="flex items-center gap-2 mb-5">

            <Lock
              className="text-green-400"
              size={20}
            />

            <h3 className="text-lg font-bold">

              Privacy Controls

            </h3>

          </div>

          <ToggleRow
            title="Private Mode"
            description="Hide your profile from community statistics and public leaderboards."
            checked={privacyMode}
            onChange={() =>
              setPrivacyMode(!privacyMode)
            }
          />

        </div>

        {/* CHANGE PASSWORD */}

        <div className="card p-6">

          <div className="flex items-center gap-2 mb-5">

            <KeyRound
              className="text-yellow-400"
              size={20}
            />

            <h3 className="text-lg font-bold">

              Change Password

            </h3>

          </div>

          <div className="space-y-4">

            <input
              type="password"
              placeholder="Current Password"
              value={password.current}
              onChange={(e) =>
                setPassword({
                  ...password,
                  current: e.target.value,
                })
              }
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3"
            />

            <input
              type="password"
              placeholder="New Password"
              value={password.new}
              onChange={(e) =>
                setPassword({
                  ...password,
                  new: e.target.value,
                })
              }
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3"
            />

            <input
              type="password"
              placeholder="Confirm New Password"
              value={password.confirm}
              onChange={(e) =>
                setPassword({
                  ...password,
                  confirm: e.target.value,
                })
              }
              className="w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3"
            />

          </div>

        </div>
                {/* SAVE SETTINGS */}

        <div className="card p-6">

          <div className="flex items-center justify-between">

            <div>

              <h3 className="text-lg font-bold">

                Save Changes

              </h3>

              <p className="text-sm text-fog-400 mt-2">

                Save your appearance, privacy and notification preferences.

              </p>

            </div>

            <button className="btn-primary flex items-center gap-2">

              <Save size={18} />

              Save Settings

            </button>

          </div>

        </div>

        {/* DANGER ZONE */}

        <div className="card border border-red-500/30 p-6">

          <div className="flex items-center gap-2 mb-4">

            <Trash2
              className="text-red-400"
              size={20}
            />

            <h3 className="text-lg font-bold text-red-400">

              Danger Zone

            </h3>

          </div>

          <p className="text-sm text-fog-400 leading-7">

            Deleting your account permanently removes:

            <br />

            • Profile

            <br />

            • Scan History

            <br />

            • Generated Reports

            <br />

            • Community Reports

            <br />

            • Saved Preferences

          </p>

          <button className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 px-5 py-3 text-red-400 hover:bg-red-500/20 transition">

            Delete Account

          </button>

        </div>

      </div>

    </AppShell>

  );

}

/* ------------------------------------ */
/* Helper Components */
/* ------------------------------------ */

function Field({
  label,
  value,
  capitalize,
}: {
  label: string;
  value: string;
  capitalize?: boolean;
}) {
  return (

    <div>

      <p className="text-xs text-fog-400 mb-1">

        {label}

      </p>

      <p
        className={`text-sm font-medium ${
          capitalize ? "capitalize" : ""
        }`}
      >

        {value}

      </p>

    </div>

  );
}

function ToggleRow({
  title,
  description,
  checked,
  onChange,
}: {
  title: string;
  description: string;
  checked: boolean;
  onChange: () => void;
}) {
  return (

    <div className="flex items-center justify-between py-3 border-b border-white/10 last:border-0">

      <div>

        <p className="font-medium">

          {title}

        </p>

        <p className="text-xs text-fog-400 mt-1">

          {description}

        </p>

      </div>

      <button
        onClick={onChange}
        className={`relative h-7 w-12 rounded-full transition ${
          checked
            ? "bg-cyan-500"
            : "bg-gray-600"
        }`}
      >

        <span
          className={`absolute top-1 h-5 w-5 rounded-full bg-white transition-all ${
            checked
              ? "left-6"
              : "left-1"
          }`}
        />

      </button>

    </div>

  );
}