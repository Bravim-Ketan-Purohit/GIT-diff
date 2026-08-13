import { Reveal } from "@/components/ui/reveal";
import { cn } from "@/lib/utils";

export function SectionHeading({
  eyebrow,
  title,
  sub,
  className,
}: {
  eyebrow: string;
  title: React.ReactNode;
  sub?: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("mx-auto max-w-2xl text-center", className)}>
      <Reveal>
        <p className="font-mono text-xs uppercase tracking-[0.25em] spectrum-text">{eyebrow}</p>
        <h2 className="mt-4 text-balance text-3xl font-bold tracking-tight sm:text-4xl">
          {title}
        </h2>
        {sub && <p className="mx-auto mt-4 max-w-xl text-pretty text-muted">{sub}</p>}
      </Reveal>
    </div>
  );
}
