import type { Metadata } from "next";
import {
  Inter,
  Space_Grotesk,
  JetBrains_Mono,
} from "next/font/google";

import "@/styles/globals.css";

import { ThemeProvider } from "@/components/layout/ThemeProvider";
import { QueryProvider } from "@/components/layout/QueryProvider";

import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
});

export const metadata: Metadata = {
  title: "Spam Shield AI — Multi-Agent Scam Detection",
  description:
    "Detect scams across URLs, emails, messages, calls, screenshots and more with AI.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className="dark"
      suppressHydrationWarning
    >
      <body
        className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}
      >
        <QueryProvider>
          <ThemeProvider>

            {children}

            <Toaster
              position="top-right"
              richColors
              closeButton
              duration={3000}
              theme="dark"
              expand={true}
            />

          </ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  );
}