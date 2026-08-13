"use client";

import { useEffect, useState } from "react";
import { Star } from "lucide-react";
import { GitHubIcon } from "@/components/ui/github-icon";
import { LogoMark } from "@/components/ui/logo";
import { GITHUB_URL } from "@/lib/site";
import { cn } from "@/lib/utils";

const LINKS = [
  { href: "#how", label: "How it works" },
  { href: "#features", label: "Features" },
  { href: "#why", label: "Why it works" },
  { href: "#install", label: "Install" },
];

export function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 16);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={cn(
        "fixed inset-x-0 top-0 z-50 transition-all duration-300",
        scrolled
          ? "border-b border-line bg-bg/80 backdrop-blur-md"
          : "border-b border-transparent",
      )}
    >
      <nav className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        <a href="#top" className="flex items-center gap-2 font-mono text-sm font-semibold">
          <LogoMark className="size-5" />
          <span className="text-ink">
            diff<span className="spectrum-text">quiz</span>
          </span>
        </a>

        <div className="hidden items-center gap-8 md:flex">
          {LINKS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-sm text-muted transition-colors hover:text-ink"
            >
              {l.label}
            </a>
          ))}
        </div>

        <a
          href={GITHUB_URL}
          target="_blank"
          rel="noreferrer"
          className="group flex items-center gap-2 rounded-lg border border-line bg-panel/60 px-3.5 py-2 text-sm text-ink transition-colors hover:border-brand/40 hover:text-brand"
        >
          <GitHubIcon className="size-4" />
          <span className="hidden sm:inline">Star on GitHub</span>
          <Star className="size-3.5 text-muted transition-colors group-hover:text-warn" />
        </a>
      </nav>
    </header>
  );
}
