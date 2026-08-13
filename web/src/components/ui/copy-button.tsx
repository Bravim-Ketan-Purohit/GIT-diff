"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { cn } from "@/lib/utils";

export function CopyButton({ text, className }: { text: string; className?: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard blocked — no-op */
    }
  }

  return (
    <button
      type="button"
      onClick={handleCopy}
      aria-label={copied ? "Copied" : "Copy to clipboard"}
      className={cn(
        "rounded-md border border-line p-2 text-muted transition-colors hover:border-brand/40 hover:text-brand",
        className,
      )}
    >
      {copied ? (
        <Check className="size-4 text-acid" />
      ) : (
        <Copy className="size-4" />
      )}
    </button>
  );
}
