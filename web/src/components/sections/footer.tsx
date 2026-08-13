import { GitHubIcon } from "@/components/ui/github-icon";
import { LogoMark } from "@/components/ui/logo";
import { GITHUB_URL, GITHUB_ISSUES, DESIGN_URL, CONTRIBUTING_URL } from "@/lib/site";

const LINKS = [
  { href: GITHUB_URL, label: "GitHub" },
  { href: DESIGN_URL, label: "Design doc" },
  { href: CONTRIBUTING_URL, label: "Contributing" },
  { href: GITHUB_ISSUES, label: "Issues" },
];

export function Footer() {
  return (
    <footer className="relative border-t border-line">
      <div className="bg-grid mask-radial pointer-events-none absolute inset-0 -z-10 opacity-30" />
      <div className="mx-auto max-w-6xl px-5 py-14">
        <div className="flex flex-col items-center justify-between gap-8 sm:flex-row sm:items-start">
          <div className="text-center sm:text-left">
            <a href="#top" className="flex items-center justify-center gap-2 font-mono text-sm font-semibold sm:justify-start">
              <LogoMark className="size-5" />
              <span>
                diff<span className="spectrum-text">quiz</span>
              </span>
            </a>
            <p className="mt-3 max-w-xs text-sm text-muted">
              Predict the diff before you read what your AI just wrote.
            </p>
          </div>

          <nav className="flex flex-wrap items-center justify-center gap-x-6 gap-y-3">
            {LINKS.map((l) => (
              <a
                key={l.label}
                href={l.href}
                target="_blank"
                rel="noreferrer"
                className="text-sm text-muted transition-colors hover:text-ink"
              >
                {l.label}
              </a>
            ))}
          </nav>
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-4 border-t border-line pt-6 text-xs text-muted sm:flex-row">
          <p>MIT © {new Date().getFullYear()} Bravim Purohit</p>
          <p className="flex items-center gap-1.5">
            Built in the terminal, for the terminal.
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noreferrer"
              className="ml-1 inline-flex items-center gap-1 transition-colors hover:text-brand"
            >
              <GitHubIcon className="size-3.5" />
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
