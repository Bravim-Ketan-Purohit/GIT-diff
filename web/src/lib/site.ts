/** Single source of truth for external links + install commands. */
export const SITE_NAME = "diffquiz";
export const TAGLINE = "predict the diff before you read what your AI just wrote";

export const GITHUB_URL = "https://github.com/Bravim-Ketan-Purohit/GIT-diff";
export const GITHUB_ISSUES = `${GITHUB_URL}/issues`;
export const CONTRIBUTING_URL = `${GITHUB_URL}/blob/main/CONTRIBUTING.md`;
export const DESIGN_URL = `${GITHUB_URL}/blob/main/DESIGN.md`;

export const INSTALL_CMD = 'pip install "diffquiz[ai]"';
export const QUICKSTART = [
  { cmd: "diffquiz index", note: "one-time: build the codebase graph (shows cost first)" },
  { cmd: "diffquiz watch", note: "get quizzed on every change your agent makes" },
];
