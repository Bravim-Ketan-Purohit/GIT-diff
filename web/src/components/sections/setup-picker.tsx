"use client";

import { useState } from "react";
import { Terminal } from "lucide-react";
import {
  ClaudeLogo,
  OpenAILogo,
  GeminiLogo,
  OpenCodeLogo,
} from "@/components/ui/agent-logos";
import { CopyButton } from "@/components/ui/copy-button";
import { cn } from "@/lib/utils";

export type SetupKey = "claude" | "codex" | "gemini" | "opencode" | "manual";

const AGENTS = [
  { key: "claude", label: "Claude Code", Logo: ClaudeLogo, iconClass: "text-[#D97757]" },
  { key: "codex", label: "Codex", Logo: OpenAILogo, iconClass: "text-white" },
  { key: "gemini", label: "Gemini CLI", Logo: GeminiLogo, iconClass: "" },
  { key: "opencode", label: "OpenCode", Logo: OpenCodeLogo, iconClass: "text-[#03B000]" },
] as const;

const LABELS: Record<SetupKey, string> = {
  claude: "Claude Code",
  codex: "OpenAI Codex",
  gemini: "Gemini CLI",
  opencode: "OpenCode",
  manual: "your terminal",
};

export function SetupPicker({ prompts }: { prompts: Record<SetupKey, string> }) {
  const [active, setActive] = useState<SetupKey>("claude");
  const text = prompts[active];
  const isManual = active === "manual";

  return (
    <div className="terminal-shadow scanlines relative overflow-hidden rounded-xl border border-line bg-[#070a10]">
      {/* picker row — grouped: agent | manual */}
      <div className="flex flex-wrap items-center gap-x-2 gap-y-2 border-b border-line bg-[#0b0f17] px-3 py-2.5">
        <Terminal className="mr-0.5 size-4 shrink-0 text-muted" aria-hidden />

        {/* agent group */}
        <GroupLabel>agent</GroupLabel>
        {AGENTS.map((a) => (
          <Pill key={a.key} active={active === a.key} onClick={() => setActive(a.key)}>
            <a.Logo className={cn("size-3.5", a.iconClass)} />
            {a.label}
          </Pill>
        ))}

        <span className="mx-1 hidden h-5 w-px bg-line sm:block" aria-hidden />

        {/* manual group */}
        <GroupLabel>manual</GroupLabel>
        <Pill active={isManual} onClick={() => setActive("manual")}>
          <Terminal className="size-3.5 text-acid" />
          pip
        </Pill>

        <CopyButton text={text} className="ml-auto shrink-0 border-line/0 hover:border-brand/40" />
      </div>

      {/* body */}
      <div className="px-4 py-3.5 sm:px-5">
        {isManual ? (
          <ManualBlock text={text} />
        ) : (
          <>
            <p className="font-mono text-xs text-muted"># paste this into {LABELS[active]}</p>
            <pre className="mt-2.5 max-h-[22rem] overflow-auto whitespace-pre-wrap break-words font-mono text-[13px] leading-relaxed text-ink/90">
              {text}
            </pre>
          </>
        )}
      </div>
    </div>
  );
}

/* ---- manual / pip: a real command list, copy line-by-line --------------- */

function ManualBlock({ text }: { text: string }) {
  const lines = text.split("\n");
  return (
    <div>
      <p className="mb-3 text-xs text-muted">Run these in your project, top to bottom:</p>
      <div className="font-mono text-[13px] leading-relaxed">
        {lines.map((line, i) => {
          if (line.trim() === "") return <div key={i} className="h-3" aria-hidden />;

          const isComment = line.trimStart().startsWith("#");
          if (isComment) {
            return (
              <div key={i} className="flex gap-2.5">
                <span className="w-2 shrink-0" aria-hidden />
                <span className="text-muted/70">{line}</span>
              </div>
            );
          }

          const command = stripTrailingComment(line);
          return (
            <div key={i} className="group/cmd flex items-start gap-2.5 rounded-md px-1 -mx-1 hover:bg-white/[0.03]">
              <span className="w-2 shrink-0 select-none text-acid">$</span>
              <code className="flex-1 whitespace-pre-wrap break-words text-ink">{line}</code>
              <CopyButton
                text={command}
                className="shrink-0 border-0 p-1 opacity-0 transition-opacity group-hover/cmd:opacity-100 focus-visible:opacity-100"
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}

/** Drop a trailing " # …" inline comment so a copied command is runnable as-is. */
function stripTrailingComment(line: string): string {
  const m = line.match(/\s+#\s.*$/);
  return (m ? line.slice(0, m.index) : line).trimEnd();
}

/* ---- bits ---------------------------------------------------------------- */

function GroupLabel({ children }: { children: React.ReactNode }) {
  return (
    <span className="font-mono text-[10px] uppercase tracking-[0.15em] text-muted/60">
      {children}
    </span>
  );
}

function Pill({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "flex items-center gap-1.5 rounded-md border px-2.5 py-1 font-mono text-xs transition-colors",
        active
          ? "border-line bg-black/50 text-ink"
          : "border-transparent text-muted hover:text-ink",
      )}
    >
      {children}
    </button>
  );
}
