"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

type Theme = "light" | "dark";
type ThemeMode = "light" | "dark" | "auto";

interface ThemeContextType {
  theme: Theme;
  mode: ThemeMode;
  toggle: () => void;
  setMode: (mode: ThemeMode) => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: "dark",
  mode: "auto",
  toggle: () => {},
  setMode: () => {},
});

function getAutoTheme(): Theme {
  const hour = new Date().getHours();
  return hour >= 6 && hour < 18 ? "light" : "dark";
}

export function ThemeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [theme, setTheme] = useState<Theme>("dark");
  const [mode, setModeState] = useState<ThemeMode>("auto");

  useEffect(() => {
    const savedMode =
      (localStorage.getItem("themeMode") as ThemeMode) ??
      "auto";

    setModeState(savedMode);

    const currentTheme =
      savedMode === "auto"
        ? getAutoTheme()
        : savedMode;

    setTheme(currentTheme);

    document.documentElement.classList.toggle(
      "dark",
      currentTheme === "dark"
    );
  }, []);

  useEffect(() => {
    if (mode !== "auto") return;

    const updateTheme = () => {
      const next = getAutoTheme();

      setTheme(next);

      document.documentElement.classList.toggle(
        "dark",
        next === "dark"
      );
    };

    updateTheme();

    const interval = setInterval(
      updateTheme,
      60000
    );

    return () => clearInterval(interval);
  }, [mode]);

  const setMode = (newMode: ThemeMode) => {
    setModeState(newMode);

    localStorage.setItem(
      "themeMode",
      newMode
    );

    const nextTheme =
      newMode === "auto"
        ? getAutoTheme()
        : newMode;

    setTheme(nextTheme);

    document.documentElement.classList.toggle(
      "dark",
      nextTheme === "dark"
    );
  };

  const toggle = () => {
    if (theme === "dark") {
      setMode("light");
    } else {
      setMode("dark");
    }
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        mode,
        toggle,
        setMode,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () =>
  useContext(ThemeContext);