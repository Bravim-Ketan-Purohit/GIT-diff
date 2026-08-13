"use client";

import { Reveal } from "@/components/ui/reveal";
import {
  ClaudeLogo,
  OpenAILogo,
  GeminiLogo,
  OpenCodeLogo,
} from "@/components/ui/agent-logos";
import { cn } from "@/lib/utils";

const AGENTS = [
  // `color` is a Tailwind text-* class (drives the SVG via currentColor).
  // Gemini bakes its own gradient fill, so its color class is a no-op.
  { name: "Claude Code", Logo: ClaudeLogo, color: "text-[#D97757]" },
  { name: "OpenAI Codex", Logo: OpenAILogo, color: "text-white" },
  { name: "Gemini CLI", Logo: GeminiLogo, color: "" },
  { name: "opencode", Logo: OpenCodeLogo, color: "text-[#03B000]" },
];

export function CompatibilityBar() {
  return (
    <Reveal delay={0.15} className="mx-auto mt-8 max-w-3xl">
      <div className="rounded-2xl border border-line bg-panel/40 px-6 py-6 backdrop-blur-sm">
        <p className="text-center font-mono text-[11px] uppercase tracking-[0.2em] text-muted">
          Pairs with your coding agent
          <span className="mx-2 text-line">·</span>
          it quizzes the diff, whoever wrote it
        </p>

        <div className="mt-6 flex flex-wrap items-center justify-center gap-x-10 gap-y-5">
          {AGENTS.map(({ name, Logo, color }) => (
            <div
              key={name}
              className="group flex items-center gap-2.5 opacity-90 transition-all duration-300 hover:-translate-y-0.5 hover:opacity-100"
            >
              <Logo className={cn("size-6", color)} />
              <span className="text-sm font-medium text-muted transition-colors group-hover:text-ink">
                {name}
              </span>
            </div>
          ))}
        </div>
      </div>
    </Reveal>
  );
}
