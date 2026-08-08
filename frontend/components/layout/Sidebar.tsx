"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import {
  LayoutDashboard,
  UploadCloud,
  History,
  Users,
  BarChart3,
  Bot,
  Settings,
  Shield,
  Moon,
  Sun,
  LogOut,
  GraduationCap,
} from "lucide-react";

import { cx } from "@/lib/utils";
import { useTheme } from "./ThemeProvider";
import { useAuthStore } from "@/lib/store";

const NAV_ITEMS = [
  {
    href: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    href: "/upload",
    label: "Upload Center",
    icon: UploadCloud,
  },
  {
    href: "/training",
    label: "AI Training",
    icon: GraduationCap,
  },
  {
    href: "/history",
    label: "Threat History",
    icon: History,
  },
  {
    href: "/community",
    label: "Community",
    icon: Users,
  },
  {
    href: "/analytics",
    label: "Analytics",
    icon: BarChart3,
  },
  {
    href: "/chatbot",
    label: "AI Assistant",
    icon: Bot,
  },
  {
    href: "/settings",
    label: "Settings",
    icon: Settings,
  },
];

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const { theme, toggle } = useTheme();
  const { logout, user } = useAuthStore();

  return (
    <aside className="flex min-h-screen w-64 flex-col bg-void-900 text-white">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-6">
        <Shield className="text-yellow-500" size={32} />

        <div>
          <span className="block text-xl font-bold">
            Spam Shield AI
          </span>

          <span className="block text-xs text-fog-400">
            Enterprise Cyber Defense
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const active =
            pathname === href ||
            pathname.startsWith(`${href}/`);

          return (
            <Link
              key={href}
              href={href}
              className={cx(
                "flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition-all",
                active
                  ? "bg-yellow-500/10 text-yellow-500"
                  : "text-fog-400 hover:bg-white/5 hover:text-white"
              )}
            >
              <Icon size={18} />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Bottom Controls */}
      <div className="space-y-2 px-3 pb-6">
        {/* Theme Toggle */}
        <button
          onClick={toggle}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-fog-400 transition hover:bg-white/5 hover:text-white"
        >
          {theme === "dark" ? (
            <Sun size={18} />
          ) : (
            <Moon size={18} />
          )}

          {theme === "dark" ? "Light Mode" : "Dark Mode"}
        </button>

        {/* Sign Out */}
        <button
          onClick={() => {
            logout();
            router.push("/login");
          }}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-red-500 transition hover:bg-red-500/10"
        >
          <LogOut size={18} />
          Sign Out
        </button>

        {/* User */}
        {user && (
          <div className="mt-3 flex items-center gap-3 rounded-xl bg-white/5 px-3 py-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-yellow-500/20 font-bold text-yellow-500">
              {user.full_name?.charAt(0).toUpperCase() || "U"}
            </div>

            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-white">
                {user.full_name}
              </p>

              <p className="truncate text-xs capitalize text-fog-400">
                {user.plan_tier} Plan
              </p>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
}