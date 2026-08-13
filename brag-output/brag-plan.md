# Brag Plan: diffquiz

## Inspection rubric (Step 1)
1. **What is the app?** A terminal tool that quizzes you on your AI coding agent's diffs *before* you read them — you predict the change, then it reveals the real diff and scores your guess (flagging bugs).
2. **Funniest / most impressive claim?** "Predict the diff before you read what your AI just wrote." + "The danger isn't that the AI is wrong. It's that you stopped paying attention."
3. **Visual hook?** The auto-playing terminal "quiz round" (watch → 🧠 your move → 🔍 reveal → 📊 scorecard) on a near-black canvas, plus the VIBGYOR gradient headline over the animated Prism background.
4. **What to show from the UI?** The live terminal demo — the actual predict→reveal→score loop with the JWT-algorithm-pinning diff.
5. **Shortest satisfying video?** ~19s — enough to land one full quiz round + the tagline/logo.
6. **Tone?** Preset `default`; direction: "terminal-native dev-tool teaser — dry, confident, a little cheeky."
7. **Audio?** Restrained electronic/tech bed; keyboard ticks on typed text; a soft click on the diff reveal; a chime on the scorecard; one logo hit.
8. **Share caption?** Drafted below.
9. **User flow worth showing?** YES — the core loop is the centerpiece: `diffquiz watch` → "change detected" → predict → reveal diff → scorecard.

---

## What is this app?
diffquiz quizzes a developer on their coding agent's diffs before they read them — predict the change, then see the real diff and a score with risk flags — so you actually understand the code your AI writes instead of rubber-stamping it.

## The angle
Re-enact one real quiz round in a terminal, end to end, and let the punchline be the score: the developer guesses "token-expiry check," the agent actually pinned the JWT algorithm, and diffquiz catches that callers sending RS256 tokens will now break. The product *catching a real ripple effect* is the brag — not a feature list.

## Hook (first 2-3 seconds)
Black screen, a blinking cursor. A command types itself: `❯ diffquiz watch`. Then a cyan line snaps in: `● change detected — auth.py`. One overlay line: **"Your agent changed auth.py. Did you read it?"**

## Key moments (the middle)
- The **🧠 your move** panel: "validate_token is called by **3 routes** — what did the agent harden?" (graph blast-radius, in-product).
- A typed prediction appears character-by-character: `added a token-expiry check?`
- The **🔍 what actually changed** diff reveal — the red `-` line, then the green `+ algorithms=["HS256"]` line slams in.
- The **📊 scorecard** rows arrive one by one: `SCORE 60/100` · `MISSED: it pins the JWT algorithm` · `WATCH: RS256 callers now fail — check the 3 routes.`

## Outro / punchline
Cut to the VIBGYOR gradient headline: **"Predict the diff before you read what your AI just wrote."** Logo (🎯 target mark + diffquiz), the agent row (Claude Code · Codex · Gemini CLI · opencode), and the repo URL.

## User flow worth showing
The working loop, not landing-page sections: **`diffquiz watch` → change detected → 🧠 predict → 🔍 reveal → 📊 score.** This is the strongest material; Scenes 1–4 are the flow.

## Tone
- Preset: default
- Creative direction: terminal-native dev-tool teaser — dry, confident, a little cheeky
- Interpretation: 4–5 scenes, comfortable pace, snappy entrances that then hold so each terminal line is readable; restraint over flash. The product's wit carries it; motion serves legibility.

## Format: landscape — 1920x1080
## Duration: ~19s

## Visual identity (from the project)
- Background: `#05070a` (`--color-bg`); panels `#0a0e15`
- Accent (brand cyan): `#22d3ee`; acid green `#4ade80`
- Spectrum (headline/logo): `#a78bfa → #818cf8 → #60a5fa → #22d3ee → #34d399 → #fcd34d → #fb923c → #fb7185`
- CLI panel borders: yellow `#fbbf24` (your move) · green `#4ade80` (reveal) · magenta `#e879f9` (scorecard) · cyan `#22d3ee` (banner)
- Text: `#e6edf3` (ink); muted `#8a96a8`
- Display/mono font: **JetBrains Mono**; Body font: **Geist** (Geist Sans)
- Strongest visual element: the terminal quiz-round window with traffic-light chrome + a "● live" dot, on a near-black canvas

## Share copy (draft)
Stop rubber-stamping your AI's code. diffquiz quizzes you on every diff before you read it — predict it, then see what actually changed (and what's about to break). 🎯

## Audio direction
- Role: warm, low tech bed — present but never loud under the terminal
- Music: an upbeat/tech electronic track (select at composition time from bundled tracks)
- Music treatment: start low under the hook, gentle lift into the reveal, settle for the scorecard, soft fade on the outro
- Music cue guidance: track + tempo to be detected at composition time; target a strong cue on the diff `+` reveal (~Scene 3) and on the logo hit (~Scene 5); use a beat-grid window for the 3 scorecard rows but hold each row to the reading floor
- Audio-reactive treatment: subtle — let the prism/headline presence breathe with music energy on the outro only; no waveform bars
- SFX posture: moderate, motion-matched — keyboard ticks on typed text, a soft click/whoosh on the diff reveal, a light chime per scorecard row, one clean logo hit
- Audio-coupled moments: the typed command (Scene 1), the typed prediction (Scene 2), the `+` line reveal (Scene 3), the 3 scorecard rows (Scene 4), the logo (Scene 5)
- Restraint rule: audio must not bury the terminal text or rush a line off before it's readable

## Storyboard

### Scene 1 — Hook: "did you read it?" — 3s
Black canvas, blinking cyan cursor. `❯ diffquiz watch` types out, then `diffquiz · watching for changes every 3s` (dim), then a cyan `● change detected — auth.py`. Overlay line holds: "Your agent changed auth.py. Did you read it?"
Sequential/interaction: yes — command types character by character, then the change-detected line snaps in.
Audio intent: quiet tension; the room leans in.
Audio-coupled idea: keyboard ticks on the typed command; a soft low hit on "change detected".
Music: low tech bed entering.
Transition mood: clean → Scene 2

### Scene 2 — 🧠 your move — 4s
The yellow-bordered "🧠 your move" panel slides in: "auth.py changed. validate_token is called by **3 routes** — what did the agent harden?" Then a prediction types in below: `❯ added a token-expiry check?`
Sequential/interaction: yes — panel in, then the prediction types out (held ~1.2s after).
Audio intent: curiosity; a beat of commitment.
Audio-coupled idea: key ticks on the typed prediction.
Music: bed continues, slight lift.
Transition mood: clean → Scene 3

### Scene 3 — 🔍 what actually changed — 4s
Green-bordered "🔍 what actually changed" panel. Diff lines: dim `@@ def validate_token(token): @@`, red `- return jwt.decode(token, SECRET)`, then the green `+ return jwt.decode(token, SECRET, algorithms=["HS256"])` SLAMS in and holds.
Sequential/interaction: yes — the `+` line lands last on a strong cue.
Audio intent: the satisfying "reveal."
Audio-coupled idea: soft click/whoosh synced to the `+` line.
Music: strong cue on the reveal.
Transition mood: hard → Scene 4

### Scene 4 — 📊 scorecard — 4s
Magenta-bordered "📊 scorecard". Three rows arrive one by one (each held to the reading floor): `SCORE: 60/100 — right that it's a security fix, wrong mechanism.` · `MISSED: it pins the JWT algorithm.` · `WATCH: RS256 callers now fail — check the 3 routes.`
Sequential/interaction: yes — 3 rows, beat-grid windows but each held long enough to read.
Audio intent: the payoff — the tool *caught* something.
Audio-coupled idea: a light chime per row; a slightly heavier accent on WATCH.
Music: settle, let the rows breathe.
Transition mood: soft → Scene 5

### Scene 5 — Tagline + logo — 4s
Cut to near-black. The VIBGYOR gradient headline writes in: "Predict the diff before you read what your AI just wrote." Then the logo (🎯 target mark + `diffquiz`) with the agent row underneath (Claude Code · Codex · Gemini CLI · opencode) and `github.com/Bravim-Ketan-Purohit/GIT-diff`.
Sequential/interaction: headline reveal, then logo + agent row settle.
Audio intent: confident landing.
Audio-coupled idea: one clean logo hit; gentle fade.
Music: soft fade out after the hit.
Transition mood: soft fade → end

**Music mood for this video:** upbeat / tech (restrained)
**Audio summary:** A low tech bed carries a single quiz round — keyboard ticks on the typed command and guess, a satisfying click on the diff reveal, three light chimes on the scorecard, and a clean logo hit that fades out under the tagline.
