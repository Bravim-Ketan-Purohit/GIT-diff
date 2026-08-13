import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/reveal";
import { SectionHeading } from "@/components/ui/section-heading";
import { GitHubIcon } from "@/components/ui/github-icon";
import { SetupPicker } from "@/components/sections/setup-picker";
import { getSetupPrompts } from "@/lib/setup-prompts";
import { GITHUB_URL, DESIGN_URL } from "@/lib/site";

export function InstallCta() {
  // Read + parse the prompts from docs/setup-prompts.md at build time.
  const prompts = getSetupPrompts();

  return (
    <section id="install" className="relative py-24 sm:py-28">
      <div className="mx-auto max-w-3xl px-5">
        <SectionHeading
          eyebrow="Get started"
          title="Set it up in one paste"
          sub="Pick the coding agent you use, copy the prompt, and paste it in — it installs diffquiz, pins the backend, and indexes your repo. Rather do it yourself? Grab the pip commands."
        />

        <Reveal delay={0.1} className="mt-12">
          <SetupPicker prompts={prompts} />
        </Reveal>

        <Reveal delay={0.18}>
          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              className="group inline-flex items-center gap-2 rounded-lg spectrum-bg px-5 py-3 text-sm font-semibold text-black transition-all hover:scale-[1.03] hover:shadow-[0_0_36px_-6px_rgba(129,140,248,0.5)]"
            >
              <GitHubIcon className="size-4" />
              Star it on GitHub
              <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" />
            </a>
            <a
              href={DESIGN_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-lg border border-line bg-panel/60 px-5 py-3 text-sm font-semibold text-ink transition-colors hover:border-brand/40 hover:text-brand"
            >
              Read the design doc
            </a>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
