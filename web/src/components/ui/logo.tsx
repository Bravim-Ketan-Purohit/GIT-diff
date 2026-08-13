import { cn } from "@/lib/utils";

/**
 * diffquiz brand mark — the bullseye + arrow from the favicon, sans tile.
 * Replaces the 🎯 emoji so the logo is a real SVG icon (UI/UX best practice).
 */
export function LogoMark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden
      className={cn("size-5 shrink-0", className)}
    >
      <circle cx="27" cy="37" r="19" stroke="#22d3ee" strokeWidth="4" />
      <circle cx="27" cy="37" r="11" stroke="#22d3ee" strokeWidth="4" strokeOpacity="0.55" />
      <circle cx="27" cy="37" r="4.5" fill="#67e8f9" />
      <g stroke="#4ade80" strokeWidth="4" strokeLinecap="round">
        <line x1="53" y1="11" x2="34.1" y2="29.9" />
        <line x1="50" y1="8" x2="55" y2="13" strokeWidth="3" />
        <line x1="47" y1="11" x2="52" y2="16" strokeWidth="3" />
      </g>
      <polygon points="27,37 37.96,33.82 30.18,26.04" fill="#4ade80" />
    </svg>
  );
}
