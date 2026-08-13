import { Eye, Brain, ScanSearch } from "lucide-react";
import { Reveal } from "@/components/ui/reveal";
import { SectionHeading } from "@/components/ui/section-heading";
import { cn } from "@/lib/utils";

const STEPS = [
  {
    icon: Eye,
    color: "text-violet-400",
    num: "group-hover:text-violet-400/25",
    title: "Your agent edits the repo",
    body: "Run diffquiz watch in a split pane next to your coding agent. It notices the moment new changes land.",
  },
  {
    icon: Brain,
    color: "text-cyan-400",
    num: "group-hover:text-cyan-400/25",
    title: "It asks before it reveals",
    body: "Before showing you a single line, it asks one pointed question: what changed here, and why? You commit to a guess.",
  },
  {
    icon: ScanSearch,
    color: "text-amber-400",
    num: "group-hover:text-amber-400/25",
    title: "Reveal, score, flag risks",
    body: "Then it shows the real diff, scores how close you were, and flags any bug or security risk it spots — citing the line.",
  },
];

export function HowItWorks() {
  return (
    <section id="how" className="relative py-24 sm:py-28">
      <div className="bg-dots mask-radial-center pointer-events-none absolute inset-0 -z-10 opacity-40" />
      <div className="mx-auto max-w-6xl px-5">
        <SectionHeading
          eyebrow="How it works"
          title="One mechanic, backed by learning science"
          sub="Commit to a guess before you see the answer. That single act turns passive skimming into real understanding."
        />

        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {STEPS.map((step, i) => (
            <Reveal key={step.title} delay={i * 0.1}>
              <div className="card-glow group h-full rounded-2xl border border-line bg-panel/50 p-6 transition-all duration-300">
                <div className="flex items-center justify-between">
                  <div
                    className={cn(
                      "flex size-11 items-center justify-center rounded-xl border border-line bg-black/40 transition-colors group-hover:border-white/20",
                      step.color,
                    )}
                  >
                    <step.icon className="size-5" />
                  </div>
                  <span
                    className={cn(
                      "font-mono text-5xl font-bold text-line transition-colors",
                      step.num,
                    )}
                  >
                    {String(i + 1).padStart(2, "0")}
                  </span>
                </div>
                <h3 className="mt-5 text-lg font-semibold text-ink">{step.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">{step.body}</p>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.2}>
          <p className="mx-auto mt-12 max-w-xl text-center text-sm text-muted">
            <span className="font-mono text-ink">tmux tip:</span>{" "}
            <code className="rounded bg-panel px-1.5 py-0.5 font-mono text-xs text-brand">
              tmux new-session \; split-window -h -p 33 &apos;diffquiz watch&apos;
            </code>
          </p>
        </Reveal>
      </div>
    </section>
  );
}
