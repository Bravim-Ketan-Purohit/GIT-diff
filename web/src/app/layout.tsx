import type { Metadata, Viewport } from "next";
import { Geist, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const sans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const mono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

const SITE = "https://diffquiz.dev";
const TITLE = "diffquiz — predict the diff before you read what your AI just wrote";
const DESCRIPTION =
  "A terminal companion that quizzes you on every change your coding agent makes — Claude Code, OpenAI Codex, Gemini CLI or opencode — so you actually understand your own codebase instead of rubber-stamping it. Zero-config, grounded in a graph of your code.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: TITLE,
  description: DESCRIPTION,
  keywords: [
    "diffquiz",
    "ai code review",
    "git diff",
    "coding agent",
    "claude code",
    "openai codex",
    "gemini cli",
    "opencode",
    "developer tools",
    "cli",
    "codebase knowledge graph",
  ],
  authors: [{ name: "Bravim Purohit" }],
  openGraph: {
    type: "website",
    url: SITE,
    title: TITLE,
    description: DESCRIPTION,
    siteName: "diffquiz",
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE,
    description: DESCRIPTION,
  },
};

export const viewport: Viewport = {
  themeColor: "#05070a",
  colorScheme: "dark",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable} h-full antialiased`}>
      <body className="min-h-full">{children}</body>
    </html>
  );
}
