# diffquiz — landing page

Marketing/launch site for [diffquiz](../README.md). Built with **Next.js 16 (App
Router)**, **Tailwind CSS v4**, **Framer Motion** (`motion`), and components in the
[Aceternity UI](https://ui.aceternity.com) / [React Bits](https://reactbits.dev)
style (Spotlight, Meteors, text-generate, typewriter, cursor-spotlight cards).

## Develop

```bash
pnpm install
pnpm dev          # http://localhost:3000
```

## Build

```bash
pnpm build        # production build (static — prerenders to HTML)
pnpm start        # serve the production build
```

## Deploy to Vercel

This site lives in the `web/` subfolder of a larger repo, so point Vercel at it:

1. Import the repo at <https://vercel.com/new>.
2. Set **Root Directory** to `web`.
3. Framework preset auto-detects **Next.js** — no other config needed.

The page is fully static, so it also exports cleanly to any static host.

## Structure

```
src/
  app/
    layout.tsx        # fonts (JetBrains Mono + Geist), metadata, theme
    page.tsx          # composes the sections
    globals.css       # design tokens + terminal aesthetic + keyframes
  components/
    sections/         # nav · hero · problem · how-it-works · features ·
                      # predict-first · install-cta · footer · terminal-demo
    ui/               # spotlight · meteors · text-generate · typewriter ·
                      # spotlight-card · reveal · section-heading · copy-button
  lib/
    site.ts           # external links + install commands (single source of truth)
    utils.ts          # cn() class merger
```

## Editing copy

All product copy is grounded in the real tool. Links and install commands live in
[`src/lib/site.ts`](src/lib/site.ts) — change them in one place.
