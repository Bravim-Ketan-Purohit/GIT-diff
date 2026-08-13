/**
 * Single source of truth for the setup section: the prompts live in
 * `docs/setup-prompts.md` (one level above this Next app) and are read +
 * parsed at build time, so the site always matches the doc character-for-character
 * and the upcoming PyPI swap is a one-file edit in `docs/` — nothing here.
 *
 * Server-only (uses node:fs). Never import this from a client component.
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";

export interface SetupPrompts {
  claude: string;
  codex: string;
  gemini: string;
  opencode: string;
  manual: string;
}

const SOURCE = join(process.cwd(), "..", "docs", "setup-prompts.md");

/** Return the first fenced ```<lang> block that appears after `heading`, verbatim. */
function blockAfter(md: string, heading: string, lang: string): string {
  const hIdx = md.indexOf(heading);
  if (hIdx === -1) throw new Error(`setup-prompts.md: heading not found: "${heading}"`);
  const fence = "```" + lang;
  const fIdx = md.indexOf(fence, hIdx);
  if (fIdx === -1) throw new Error(`setup-prompts.md: no ${lang} block after "${heading}"`);
  const bodyStart = fIdx + fence.length + 1; // skip the newline right after ```<lang>
  const closeIdx = md.indexOf("\n```", bodyStart);
  if (closeIdx === -1) throw new Error(`setup-prompts.md: unterminated block after "${heading}"`);
  return md.slice(bodyStart, closeIdx);
}

export function getSetupPrompts(): SetupPrompts {
  const md = readFileSync(SOURCE, "utf8");
  return {
    claude: blockAfter(md, "### Claude Code", "text"),
    codex: blockAfter(md, "### OpenAI Codex", "text"),
    gemini: blockAfter(md, "### Gemini CLI", "text"),
    opencode: blockAfter(md, "### OpenCode", "text"),
    manual: blockAfter(md, "## Manual setup", "bash"),
  };
}
