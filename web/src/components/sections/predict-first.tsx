import { Spotlight } from "@/components/ui/spotlight";
import { Reveal } from "@/components/ui/reveal";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect";
import { cn } from "@/lib/utils";

const STATS = [
  { value: "30s", color: "text-violet-400", label: "of dead time per change, turned into retention" },
  { value: "1", color: "text-cyan-400", label: "guess is all it takes to make the correction stick" },
  { value: "0", color: "text-amber-400", label: "API keys required to get scored" },
];

export function PredictFirst() {
  return (
    <section id="why" className="relative overflow-hidden py-28 sm:py-36">
      <Spotlight className="-top-20 right-0 rotate-180 opacity-60" fill="#a78bfa" />
      <div className="bg-grid mask-radial-center pointer-events-none absolute inset-0 -z-10 opacity-50" />

      <div className="mx-auto max-w-3xl px-5 text-center">
        <Reveal>
          <p className="font-mono text-xs uppercase tracking-[0.25em] spectrum-text">
            Why predict-first works
          </p>
        </Reveal>

        <blockquote className="mt-8 text-balance text-2xl font-medium leading-snug tracking-tight sm:text-4xl">
          <TextGenerateEffect words="The moment of being slightly wrong is what makes the correction stick." />
        </blockquote>

        <Reveal delay={0.1}>
          <p className="mx-auto mt-8 max-w-xl text-pretty text-muted">
            Prediction before feedback is one of the most reliable learning mechanics
            there is. diffquiz weaponizes the half-minute you'd otherwise spend waiting
            for your agent.
          </p>
        </Reveal>

        <div className="mt-16 grid gap-6 sm:grid-cols-3">
          {STATS.map((s, i) => (
            <Reveal key={s.label} delay={i * 0.1}>
              <div className="rounded-2xl border border-line bg-panel/40 px-4 py-7">
                <div className={cn("font-mono text-4xl font-bold text-glow", s.color)}>
                  {s.value}
                </div>
                <p className="mt-3 text-sm text-muted">{s.label}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
