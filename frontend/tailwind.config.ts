import type { Config } from "tailwindcss";

// Design system: "Sentinel" — a night-watch/beacon visual language.
// Deep navy (vigilance, night) + amber beacon accent (warning light) +
// signal teal (all-clear) rather than generic purple-gradient AI cliches
// or stock red/green traffic-light security kitsch.
const config: Config = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        void: {
          950: "#080D16",
          900: "#0B1220",
          800: "#101828",
          700: "#141B2D",
          600: "#1C2438",
        },
        fog: {
          400: "#8894AA",
          300: "#A7B1C4",
          200: "#CBD3E1",
        },
        paper: "#EDF1F7",
        beacon: {
          500: "#FFB020",
          400: "#FFC24D",
          600: "#E8990A",
        },
        signal: {
          500: "#2DD4BF",
          600: "#14B8A6",
        },
        alert: {
          500: "#FF5470",
          600: "#E5395A",
        },
        amberrisk: "#FF8C42",
      },
      fontFamily: {
        display: ["var(--font-space-grotesk)", "sans-serif"],
        body: ["var(--font-inter)", "sans-serif"],
        mono: ["var(--font-jetbrains-mono)", "monospace"],
      },
      boxShadow: {
        beacon: "0 0 40px -8px rgba(255,176,32,0.35)",
        signal: "0 0 40px -8px rgba(45,212,191,0.3)",
      },
      backgroundImage: {
        radar: "radial-gradient(circle at center, transparent 0%, transparent 60%, rgba(255,176,32,0.06) 61%, transparent 62%)",
      },
      animation: {
        sweep: "sweep 4s linear infinite",
        "pulse-slow": "pulse 3s cubic-bezier(0.4,0,0.6,1) infinite",
      },
      keyframes: {
        sweep: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
