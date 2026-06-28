<div align="center">

<!-- ░░░ ANIMATED WAVING HEADER (renders automatically via capsule-render) ░░░ -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3670A0,50:5B4FC4,100:8E2DE2&height=220&section=header&text=diffquiz&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Predict%20the%20diff%20before%20you%20read%20what%20your%20AI%20just%20wrote&descAlignY=58&descSize=16" width="100%" alt="diffquiz" />

<!-- ░░░ LIVE TYPING EFFECT (cycles through your taglines, animates automatically) ░░░ -->
<a href="https://github.com/Bravim-Ketan-Purohit/GIT-diff">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3200&pause=900&color=5B4FC4&center=true&vCenter=true&width=620&height=45&lines=Stop+rubber-stamping+your+AI's+code.;Commit+to+a+guess+before+you+see+the+diff.;Turn+dead+time+into+retention.;Actually+understand+your+own+codebase." alt="Typing SVG" />
</a>

<br/>

<!-- ░░░ BADGES ░░░ -->
<p>
  <a href="https://github.com/Bravim-Ketan-Purohit/GIT-diff">
    <img src="https://img.shields.io/badge/pip%20install-diffquiz-3670A0?style=for-the-badge&logo=python&logoColor=white" alt="pip install diffquiz" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge" alt="License: MIT" />
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-4B8BBE?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+" />
  <a href="CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/PRs-welcome-8E2DE2?style=for-the-badge" alt="PRs Welcome" />
  </a>
</p>

<!-- ░░░ DEMO SLOT — the one thing you still record yourself ░░░ -->
<!-- Drop a terminal recording here (asciinema or a GIF). This is the #1 thing that earns stars. -->
<!-- <img src="docs/demo.gif" alt="diffquiz demo" width="80%" /> -->

</div>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" alt="" />

## 🧠 The problem

AI agents write code faster than you can read it. So you don't read it. You skim the green squares, hit accept, and three weeks later you can't answer basic questions about your own project — *what does this function return, where is this used, why is it built this way.*

> [!WARNING]
> **The danger isn't that the AI is wrong. It's that you stopped paying attention.**

`diffquiz` fixes that with one mechanic backed by learning science: **commit to a guess before you see the answer.** Before it reveals what your agent changed, it asks you to predict it. That single act of prediction is what turns passive skimming into actual understanding — and it catches bugs you'd otherwise wave through.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" alt="" />

## ⚡ How it works

```mermaid
flowchart LR
    A([🤖 Agent edits<br/>the repo]) --> B{👀 diffquiz<br/>detects change}
    B --> C[❓ &quot;auth.py changed —<br/>what & why?&quot;]
    C --> D[⌨️ You type a<br/>one-line guess]
    D --> E[📜 Reveals the<br/>real diff]
    E --> F([🎯 AI scores you<br/>+ flags bugs & risks])

    classDef predict fill:#5B4FC4,stroke:#8E2DE2,stroke-width:2px,color:#fff;
    classDef reveal fill:#3670A0,stroke:#4B8BBE,stroke-width:2px,color:#fff;
    class C,D predict;
    class E,F reveal;
```

1. Run `diffquiz watch` in a split terminal pane next to your coding agent.
2. Your agent edits the repo. `diffquiz` notices the new changes.
3. **Before showing you the diff,** it asks: *"`auth.py` changed — what do you think changed, and why?"*
4. You type a one-line prediction.
5. It reveals the real diff, then (with an API key) scores your guess and **flags any bugs or risks it spots.**

You learn the codebase as it's being built, and you stop merging code you never read.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" alt="" />

## 📦 Install

```bash
pip install diffquiz            # core
pip install "diffquiz[ai]"      # + AI scoring & risk flags (recommended)
```

## 🚀 Quickstart

```bash
# In your project, after your agent has made some changes:
diffquiz once

# Or run it live in a pane and get quizzed on every change:
diffquiz watch
```

<details>
<summary><b>🪟 Side-by-side with your agent (tmux)</b></summary>

<br/>

```bash
# main pane = your agent, right third = diffquiz
tmux new-session \; split-window -h -p 33 'diffquiz watch'
```

</details>

<details>
<summary><b>🤖 AI scoring (optional but worth it)</b></summary>

<br/>

```bash
export ANTHROPIC_API_KEY=sk-...          # unlocks grading + risk flags
export DIFFQUIZ_MODEL=claude-sonnet-4-6  # optional: sharper, slower than the default
```

> [!NOTE]
> Without a key, `diffquiz` still works — it shows the diff after your guess, just without the AI scorecard.

</details>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" alt="" />

## 🔬 Why predict-first works

> [!TIP]
> Prediction before feedback is one of the most reliable learning mechanics there is: the moment of *being slightly wrong* is what makes the correction stick.

`diffquiz` weaponizes the 30 seconds you'd otherwise spend waiting for your agent — turning dead time into retention.

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" alt="" />

## 🗺️ Roadmap

- [ ] `docs/demo.gif` — record the first real session
- [ ] Untracked-file support (currently quizzes on tracked changes vs `HEAD`)
- [ ] Streak + score history (`~/.diffquiz/`)
- [ ] Spaced-repetition deck from past diffs
- [ ] Pluggable agents beyond git (watch a log, a webhook, etc.)
- [ ] A proper Textual TUI for the watch pane

Got an idea? [**Open an issue**](https://github.com/Bravim-Ketan-Purohit/GIT-diff/issues) — see [**CONTRIBUTING**](CONTRIBUTING.md).

## 🤝 Contributing

PRs are welcome. Whether it's a roadmap item, a bug fix, or just better docs — pick something up and open a pull request.

<details>
<summary><b>⭐ Star history</b></summary>

<br/>

<a href="https://star-history.com/#Bravim-Ketan-Purohit/GIT-diff&Date">
  <img src="https://api.star-history.com/svg?repos=Bravim-Ketan-Purohit/GIT-diff&type=Date" alt="Star History Chart" width="70%" />
</a>

</details>

## 📄 License

MIT © [**Bravim Purohit**](https://github.com/Bravim-Ketan-Purohit)

<!-- ░░░ ANIMATED WAVING FOOTER ░░░ -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:8E2DE2,50:5B4FC4,100:3670A0&height=120&section=footer" width="100%" alt="" />
