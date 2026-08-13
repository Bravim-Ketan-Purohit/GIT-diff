import { Reveal } from "@/components/ui/reveal";
import { SectionHeading } from "@/components/ui/section-heading";
import MagicBento from "@/components/reactbits/MagicBento";

export function Features() {
  return (
    <section id="features" className="relative py-24 sm:py-28">
      <div className="mx-auto max-w-6xl px-5">
        <SectionHeading
          eyebrow="What you get"
          title="More than a diff viewer"
          sub="It builds a persistent model of your codebase and uses it to make every change a learning moment."
        />

        <Reveal delay={0.1} className="mt-16">
          <MagicBento
            textAutoHide={false}
            enableStars
            enableSpotlight
            enableBorderGlow
            enableTilt
            enableMagnetism
            clickEffect
            spotlightRadius={320}
            particleCount={8}
            glowColor="167, 139, 250"
          />
        </Reveal>
      </div>
    </section>
  );
}
