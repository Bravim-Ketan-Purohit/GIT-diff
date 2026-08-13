"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { cn } from "@/lib/utils";

/* ---- the script for one looping round ----------------------------------- */

const DIFF_LINES: { text: string; tone: "ctx" | "add" | "del" | "hunk" }[] = [
  { text: "@@ def validate_token(token): @@", tone: "hunk" },
  { text: "-    return jwt.decode(token, SECRET)", tone: "del" },
  { text: '+    return jwt.decode(token, SECRET, algorithms=["HS256"])', tone: "add" },
];

const SCORECARD = [
  { label: "SCORE", body: "60/100 — right that it's a security fix, wrong mechanism.", tone: "score" },
  { label: "MISSED", body: 'it pins the JWT algorithm (algorithms=["HS256"]), not token expiry.', tone: "missed" },
  { label: "WATCH", body: "callers sending RS256 tokens now fail to decode — check the 3 routes.", tone: "watch" },
] as const;

/* timeline (ms) for revealing each block, then the loop restart */
const SCHEDULE = [250, 1050, 1900, 2750, 4250, 5550, 7100];
const LOOP_AT = 11800;

export function TerminalDemo({ className }: { className?: string }) {
  const [step, setStep] = useState(0);
  const [cycle, setCycle] = useState(0);

  useEffect(() => {
    const timers = SCHEDULE.map((t, i) => setTimeout(() => setStep(i + 1), t));
    const loop = setTimeout(() => {
      setStep(0);
      setCycle((c) => c + 1);
    }, LOOP_AT);
    return () => {
      timers.forEach(clearTimeout);
      clearTimeout(loop);
    };
  }, [cycle]);

  return (
    <div
      className={cn(
        "terminal-shadow scanlines relative w-full overflow-hidden rounded-xl border border-line bg-[#070a10]",
        className,
      )}
    >
      {/* window chrome */}
      <div className="flex items-center gap-2 border-b border-line bg-[#0b0f17] px-4 py-3">
        <span className="size-3 rounded-full bg-[#ff5f57]" />
        <span className="size-3 rounded-full bg-[#febc2e]" />
        <span className="size-3 rounded-full bg-[#28c840]" />
        <span className="ml-3 font-mono text-xs text-muted">diffquiz — watch — zsh</span>
        <span className="ml-auto flex items-center gap-1.5 font-mono text-[10px] text-acid">
          <span className="size-1.5 animate-pulse rounded-full bg-acid" /> live
        </span>
      </div>

      {/* body */}
      <div
        key={cycle}
        className="min-h-[420px] space-y-3 p-4 font-mono text-[13px] leading-relaxed sm:p-5 sm:text-sm"
      >
        {step >= 1 && (
          <Block>
            <span className="text-acid">❯</span>{" "}
            <TypeOnce text="diffquiz watch" className="text-ink" />
          </Block>
        )}

        {step >= 2 && (
          <Block>
            <span className="text-muted">
              diffquiz · watching for changes every 3s · Ctrl-C to quit
            </span>
          </Block>
        )}

        {step >= 3 && (
          <Block>
            <span className="text-brand">● change detected</span>{" "}
            <span className="text-muted">— src/auth.py</span>
          </Block>
        )}

        {step >= 4 && (
          <Block>
            <Panel title="🧠 your move" tone="warn">
              <p className="text-ink/90">
                auth.py changed. <span className="text-warn">validate_token</span> is
                called by <span className="text-warn">3 routes</span> — what did the
                agent harden, and why?
              </p>
            </Panel>
          </Block>
        )}

        {step >= 5 && (
          <Block>
            <span className="text-muted">Your prediction</span>{" "}
            <span className="text-acid">▸</span>{" "}
            <TypeOnce text="added a token-expiry check?" className="text-ink" speed={38} />
          </Block>
        )}

        {step >= 6 && (
          <Block>
            <Panel title="🔍 what actually changed" tone="acid">
              <pre className="overflow-x-auto whitespace-pre">
                {DIFF_LINES.map((l, i) => (
                  <div
                    key={i}
                    className={cn(
                      l.tone === "add" && "text-acid",
                      l.tone === "del" && "text-rose-400",
                      l.tone === "hunk" && "text-muted",
                      l.tone === "ctx" && "text-ink/70",
                    )}
                  >
                    {l.text}
                  </div>
                ))}
              </pre>
            </Panel>
          </Block>
        )}

        {step >= 7 && (
          <Block>
            <Panel title="📊 scorecard" tone="magenta">
              <div className="space-y-1.5">
                {SCORECARD.map((row) => (
                  <p key={row.label}>
                    <span
                      className={cn(
                        "font-semibold",
                        row.tone === "score" && "text-acid",
                        row.tone === "missed" && "text-warn",
                        row.tone === "watch" && "text-rose-400",
                      )}
                    >
                      {row.label}:
                    </span>{" "}
                    <span className="text-ink/85">{row.body}</span>
                  </p>
                ))}
              </div>
            </Panel>
          </Block>
        )}

        {step >= 1 && step < 7 && (
          <span className="inline-block h-4 w-2 animate-blink bg-brand align-middle" />
        )}
      </div>
    </div>
  );
}

/* ---- pieces -------------------------------------------------------------- */

function Block({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}

const TONES = {
  warn: "border-warn/40 shadow-[0_0_30px_-12px_rgba(251,191,36,0.45)]",
  acid: "border-acid/40 shadow-[0_0_30px_-12px_rgba(74,222,128,0.45)]",
  magenta: "border-magenta/40 shadow-[0_0_30px_-12px_rgba(232,121,249,0.45)]",
} as const;

const TITLE_TONES = {
  warn: "text-warn",
  acid: "text-acid",
  magenta: "text-magenta",
} as const;

function Panel({
  title,
  tone,
  children,
}: {
  title: string;
  tone: keyof typeof TONES;
  children: React.ReactNode;
}) {
  return (
    <div className={cn("rounded-lg border bg-black/30 px-4 py-3", TONES[tone])}>
      <div className={cn("mb-2 text-xs font-semibold", TITLE_TONES[tone])}>{title}</div>
      {children}
    </div>
  );
}

/** Types its text once when mounted (resets on cycle remount). */
function TypeOnce({
  text,
  className,
  speed = 55,
}: {
  text: string;
  className?: string;
  speed?: number;
}) {
  const [n, setN] = useState(0);
  useEffect(() => {
    if (n >= text.length) return;
    const t = setTimeout(() => setN((v) => v + 1), speed);
    return () => clearTimeout(t);
  }, [n, text, speed]);
  return <span className={className}>{text.slice(0, n)}</span>;
}
