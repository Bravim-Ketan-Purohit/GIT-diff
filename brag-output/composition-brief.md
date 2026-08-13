# Hyperframes Composition Brief: diffquiz

## Objective
A ~19s landscape brag video that re-enacts one real diffquiz quiz round and lands on the tagline + logo.

## Output
- Composition: `brag-output/composition/`  · Rendered: `brag-output/brag.mp4`
- Format: landscape 1920x1080 · Duration: ~19s

## Source material
- Product: **diffquiz** — quizzes you on your AI agent's diffs before you read them.
- Tagline (verbatim): "Predict the diff before you read what your AI just wrote."
- UI recreated: the terminal quiz round (watch → 🧠 your move → 🔍 reveal → 📊 scorecard) and the gradient logo.
- The diff payoff: pinning the JWT algorithm; scorecard catches that RS256 callers break.

## Creative direction
- Tone: default — terminal-native dev-tool teaser, dry and confident.
- Hook: typed `❯ diffquiz watch` → `● change detected — auth.py`.
- Outro: VIBGYOR gradient tagline + 🎯 logo + agent row + repo URL.
- Avoid: generic SaaS language, abstract filler, redesigning the brand.

## Visual identity (from the project)
- bg #05070a · panel #070a10 · ink #e6edf3 · muted #8a96a8
- cyan #22d3ee · acid green #4ade80 · warn #fbbf24 · magenta #e879f9 · rose #fb7185
- spectrum: #a78bfa→#818cf8→#60a5fa→#22d3ee→#34d399→#fcd34d→#fb923c→#fb7185
- mono: JetBrains Mono · sans: Inter (Geist stand-in)

## Storyboard (see brag-plan.md)
1. Hook — 0–3s — typed `diffquiz watch`, watching, `● change detected — auth.py`.
2. 🧠 your move — 3–7s — "validate_token is called by 3 routes — what did the agent harden?" + typed prediction.
3. 🔍 what actually changed — 7–11s — diff; the green `+ algorithms=["HS256"]` slams in (beat moment).
4. 📊 scorecard — 11–15s — SCORE / MISSED / WATCH rows one by one.
5. Tagline + logo — 15–19s — gradient headline, 🎯 diffquiz, agent row, repo URL.

## Audio
- Render is currently blocked on FFmpeg (see doctor); audio layering deferred. Visual composition first; music/SFX can be added once render is unblocked. No music asset bundled with /brag, so a track would come from the Hyperframes registry at that point.

## Hyperframes notes
- Single index.html, GSAP timeline registered as `window.__timelines["main"]`, deterministic.
- Each scene is a centered terminal-window clip with identical chrome (reads as one window updating); clean cuts between scenes; outro clip on top.
