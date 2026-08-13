import { Reveal } from "@/components/ui/reveal";
import { TextGenerateEffect } from "@/components/ui/text-generate-effect";

export function Problem() {
  return (
    <section className="relative py-24 sm:py-32">
      <div className="mx-auto max-w-3xl px-5 text-center">
        <Reveal>
          <p className="font-mono text-xs uppercase tracking-[0.25em] spectrum-text">
            The problem
          </p>
        </Reveal>

        <h2 className="mt-6 text-balance text-3xl font-semibold leading-tight tracking-tight sm:text-5xl">
          <TextGenerateEffect words="AI agents write code faster than you can read it. So you don't read it." />
        </h2>

        <Reveal delay={0.1}>
          <p className="mx-auto mt-8 max-w-2xl text-pretty text-lg text-muted">
            You skim the green squares, hit accept, and three weeks later you can't
            answer basic questions about your own project — what this function returns,
            where it's used, why it's built this way.
          </p>
        </Reveal>

        <Reveal delay={0.18}>
          <p className="mx-auto mt-10 max-w-xl text-balance text-xl font-medium text-ink sm:text-2xl">
            The danger isn't that the AI is wrong. It's that{" "}
            <span className="spectrum-text">you stopped paying attention.</span>
          </p>
        </Reveal>
      </div>
    </section>
  );
}
