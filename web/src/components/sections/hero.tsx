"use client";

import { motion } from "motion/react";
import { ArrowRight } from "lucide-react";
import { Typewriter } from "@/components/ui/typewriter";
import Prism from "@/components/reactbits/Prism";
import { GitHubIcon } from "@/components/ui/github-icon";
import { TerminalDemo } from "@/components/sections/terminal-demo";
import { CompatibilityBar } from "@/components/sections/compatibility-bar";
import { GITHUB_URL } from "@/lib/site";

export function Hero() {
  return (
    <section id="top" className="relative overflow-hidden pb-24 pt-32 sm:pt-40">
      {/* Prism (React Bits) WebGL background — spans the full hero, down past the
          terminal + compatibility card. DPR-capped, fewer steps, and paused while
          scrolling (see Prism.jsx) so the larger canvas still stays smooth. */}
      <div className="pointer-events-none absolute inset-0 -z-20">
        <Prism
          animationType="rotate"
          timeScale={0.5}
          height={3.5}
          baseWidth={5.5}
          scale={3.6}
          hueShift={0}
          colorFrequency={1}
          noise={0.4}
          glow={1}
          suspendWhenOffscreen
        />
      </div>
      {/* legibility scrims: dim the prism, fade into the nav above and page below */}
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[rgba(5,7,10,0.42)]" />
      <div className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-28 bg-gradient-to-b from-bg to-transparent" />
      <div className="pointer-events-none absolute inset-x-0 bottom-0 -z-10 h-72 bg-gradient-to-b from-transparent to-bg" />
      <div className="bg-grid mask-radial pointer-events-none absolute inset-0 -z-10 opacity-20" />

      <div className="mx-auto max-w-6xl px-5">
        <div className="mx-auto max-w-3xl text-center">
          <motion.a
            href={GITHUB_URL}
            target="_blank"
            rel="noreferrer"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 rounded-full border border-line bg-panel/60 px-4 py-1.5 font-mono text-xs text-muted backdrop-blur-sm transition-colors hover:border-brand/40 hover:text-ink"
          >
            <span className="size-1.5 animate-pulse rounded-full bg-acid" />
            Works with any coding agent — no API key needed
          </motion.a>

          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.05 }}
            className="mt-6 text-balance text-4xl font-bold leading-[1.05] tracking-tight sm:text-6xl"
          >
            Predict the diff before you read{" "}
            <span className="gradient-text">what your AI just wrote.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.12 }}
            className="mx-auto mt-6 max-w-2xl text-pretty text-lg text-muted"
          >
            A terminal companion that quizzes you on every change your coding agent
            makes — so you stop{" "}
            <Typewriter
              className="font-mono text-ink"
              words={[
                "rubber-stamping AI code.",
                "merging code you never read.",
                "losing track of your own repo.",
              ]}
            />
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.18 }}
            className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row"
          >
            <a
              href="#install"
              className="group inline-flex items-center gap-2 rounded-lg spectrum-bg px-5 py-3 text-sm font-semibold text-black transition-all hover:scale-[1.03] hover:shadow-[0_0_36px_-6px_rgba(129,140,248,0.5)]"
            >
              Get started
              <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" />
            </a>
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-lg border border-line bg-panel/60 px-5 py-3 text-sm font-semibold text-ink backdrop-blur-sm transition-colors hover:border-brand/40 hover:text-brand"
            >
              <GitHubIcon className="size-4" />
              View source
            </a>
          </motion.div>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.28 }}
            className="mt-5 font-mono text-xs text-muted"
          >
            MIT licensed · Python 3.9+ · works offline
          </motion.p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
          className="mx-auto mt-16 max-w-3xl"
        >
          <TerminalDemo />
        </motion.div>

        <CompatibilityBar />
      </div>
    </section>
  );
}
