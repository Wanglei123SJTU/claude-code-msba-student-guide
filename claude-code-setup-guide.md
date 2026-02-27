# Claude Code Setup and Configuration Guide

![Claude Code Hero](images/hero-claude-code.png)

This document focuses on Claude Code setup and configuration: prerequisites, Desktop first-run workflow, and alternative setup paths (Terminal/IDE/Web).

## 1. Preflight checklist

### Account and plan
- You need a Claude account.
- To use the Desktop `Code` tab, you need an eligible **paid** plan: Pro, Max, Teams, or Enterprise.
- Pricing:
  - Pro: `$20/month` (or `$17/month` billed annually).
  - Max: starts at `$100/month` (higher tier available at `$200/month`).
- Official pricing page: https://claude.com/pricing

#### Free fallback option
- If you prefer not to pay for a Claude Code subscription, Gemini can serve as a practical free alternative, although it has a slightly steeper learning curve, as Gemini does **not** have a standalone Windows/macOS Desktop app installer like Claude Desktop.
- Recommended free-start options:
  - **Gemini Code Assist (Individual)**: free tier for eligible individual accounts in VS Code / JetBrains.
  - **Gemini CLI**: free tier for personal Google accounts (with quota limits).
- Google Cloud trial note: eligible **new Google Cloud customers** can usually get up to **$300 trial credit** (about 90 days), which can be used for Google Cloud services such as **Gemini API usage via GCP projects**.
- Links:
  - Gemini Code Assist (individual setup): https://developers.google.com/gemini-code-assist/docs/set-up-gemini
  - Gemini CLI quotas and pricing: https://google-gemini.github.io/gemini-cli/docs/quota-and-pricing.html
  - Google Cloud Free Program ($300 trial): https://cloud.google.com/free/docs/gcp-free-tier

This document will focus on the Claude Code desktop application, as it is the most accessible option for the majority of students.

### OS and support
- macOS: Desktop app supported.
- Windows: x64 supported.
- Linux: Desktop app not currently supported.

### Local prerequisites
- On Windows, Git is required for local Desktop coding sessions ([desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart)).



---

## 2. Desktop app setup and configuration

### Step 1: Download the desktop app

`Goal`: Install Claude Desktop for your operating system.
`Action`: Open `https://claude.ai/download`, choose the correct installer, and complete installation.
`What success looks like`: Claude launches from Applications (macOS) or Start menu (Windows).

![Desktop app download flow (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/12.png)

### Step 2: Sign in and enter Code mode

`Goal`: Activate coding workflow in Desktop.
`Action`: Sign in, then switch to the `Code` tab.
`What success looks like`: You can start a local coding session.

![Desktop code tab and initial setup (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/13.png)

### Step 3: Connect local project and set safe defaults

`Goal`: Configure a safe first session.
`Action`:
1. Choose a local project folder.
2. Keep permission mode on `Ask permissions`.
3. Select model and start with a read-only analysis prompt.

`What success looks like`: Claude can inspect project structure and propose changes without auto-editing.

![Desktop project configuration and review flow (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/14.png)

Suggested first prompt:
```text
Read this repository and summarize:
1) objective,
2) key data/code entry points,
3) top implementation risks,
4) one high-impact improvement.
```

### Step 4: Review diffs and approve intentionally

`Goal`: Maintain human control and code quality.
`Action`: Review each proposed diff before accepting.
`What success looks like`: You can explain every accepted change and why it was approved.

<font color="red">
Be careful! Always review every agent action before approval, and be extremely careful with destructive actions (especially deleting files) and paid actions (for example, API calls that can incur charges).
</font>

---

## Appendix: Alternative Claude Code setup paths (Terminal / IDE / Web)

This appendix contains the other three setup paths. 
### A. Terminal CLI path

`Goal`: Install and run Claude Code in terminal.

`Command` (Windows PowerShell):
```powershell
irm https://claude.ai/install.ps1 | iex
```

`Command` (macOS/Linux):
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

`Command` (Windows WinGet optional):
```powershell
winget install Anthropic.ClaudeCode
```

`Command` (verify):
```bash
claude --version
claude --help
```

`What success looks like`: `claude` starts and accepts prompts in your project directory.

![Terminal setup step 1 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/0.png)
![Terminal setup step 2 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/1.png)
![Terminal setup step 3 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/2.png)

### B. IDE path (VS Code)

`Goal`: Use Claude Code within editor workflow.

Steps:
1. Ensure CLI is installed first.
2. Install/open the Claude-related extension/workflow in VS Code.
3. Sign in and run Claude from editor context.

`What success looks like`: You can invoke Claude from VS Code and operate on the current workspace.

![VS Code setup step 1 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/3.png)
![VS Code setup step 2 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/4.png)
![VS Code setup step 3 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/5.png)

### C. Web path

`Goal`: Use Claude coding workflows through web interface flow.

Steps:
1. Sign in on web interface.
2. Open the coding workspace flow.
3. Configure project/context and run your first task.

`What success looks like`: You can issue coding prompts in web context and review outputs.

![Web setup step 1 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/6.png)
![Web setup step 2 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/7.png)
![Web setup step 3 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/8.png)
![Web setup step 4 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/9.png)
![Web setup step 5 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/10.png)
![Web setup step 6 (Bannerbear)](https://www.bannerbear.com/images/ghost/2026-01-21-how-to-install-claude-code-terminal-ide-web-desktop-setup/11.png)

---

## References

- Claude Code desktop quickstart: https://code.claude.com/docs/en/desktop-quickstart
- Claude pricing: https://claude.com/pricing
- Claude Code desktop docs: https://code.claude.com/docs/en/desktop
- Claude Code overview: https://code.claude.com/docs/en/overview
- Bannerbear tutorial: https://www.bannerbear.com/blog/how-to-install-claude-code-terminal-ide-web-desktop-setup/





