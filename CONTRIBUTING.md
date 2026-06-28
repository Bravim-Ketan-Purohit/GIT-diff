# Contributing to diffquiz

Thanks for being here. diffquiz is small on purpose — that makes it a great repo
to make your first contribution to.

## Good first issues
- Add untracked-file support
- Persist a streak/score in `~/.diffquiz/`
- Add a new question style (see `ai.generate_question`)
- Improve the tmux/zellij/wezterm split recipes in the README

## Dev setup
```bash
git clone https://github.com/Bravim-Ketan-Purohit/GIT-diff
cd GIT-diff
pip install -e ".[ai]"
```

## Ground rules
- Keep it dependency-light (rich).
- Everything must still work within the cli of coding agent (no API key - except for the BYOK).
- One focused PR per change; describe the "why", and a usecase that you think most devs are using.
