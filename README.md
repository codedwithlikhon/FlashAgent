# FlashAgent

FlashAgent is a lightweight staging area for research on modern agentic AI frameworks and UI systems. The repository currently contains documentation summarizing the most relevant patterns from:

- **AI Manus** – secure sandboxed conversations, Docker-based orchestration, and multilingual tooling.
- **Browser Use** – Playwright-powered browser automation with persistent CDP sessions and sharable tooling.
- **Lemon AI** – privacy-focused, VM-isolated execution with self-learning repositories and local/offline LLM options.
- **OpenHands** – an IDE-centric agent experience featuring chat, terminals, file explorers, and MCP-compatible toolchains.
- **Vercel Geist & Ant Design** – accessible component libraries, design tokens, grid layouts, and navigation patterns for cohesive dashboards.

## Design Guidelines

The UI workstream draws heavily from Vercel's Geist system and Ant Design 5/6 principles:

- Adopt Geist typography tokens (e.g., `text-heading-32`, `text-button-14`) to ensure consistent hierarchy and readability.
- Use Ant Design's 24-column grid with responsive gutters (`{ xs: 8, sm: 16, md: 24, lg: 32 }`) to accommodate dense enterprise layouts.
- Follow navigation rules where the first-level menu aligns with the logo, the current item receives the strongest emphasis, and collapsed states inherit parent highlights.
- Prefer CSS variables and scoped overrides (as in Ant Design v6) to manage variants, hover states, and theme extensions without specificity wars.

## Platform Roadmap

FlashAgent aims to evolve from documentation into a full-featured agent platform by:

1. **Sandboxing & Deployment** – launching per-task Docker or microVM sandboxes, supporting pooled vs. siloed execution, and hardening profiles with dropped capabilities, seccomp, and cgroup quotas.
2. **Browser Automation** – orchestrating stepwise Playwright actions, enabling self-healing selectors, and sharing CDP sessions between Browser-Use agents and custom actions.
3. **Tool Extensibility** – exposing a registry/MCP-based plug-in layer for terminals, editors, search, Slack, and API integrations with per-tool policies and audit trails.
4. **Session Memory** – persisting scratchpads, summaries, and vector-backed knowledge to resume tasks and provide human-in-the-loop checkpoints.
5. **Multilingual UX** – instrumenting i18n across the dashboard, routing LLMs per language, and inviting community translation packs.
6. **Design System Migration** – replacing ad-hoc Ant Design Vue elements with Geist-inspired components, high-contrast theming, and accessible navigation/terminal/file panels.
7. **Security Posture** – enforcing least privilege, prompt/input filtering, human approvals for sensitive actions, continuous container scanning, and alerting pipelines.

## Deployment Notes

Although the working tree is intentionally minimal, past experiments covered:

- Node.js/Playwright Docker images with layered base builds for <30s incremental rebuilds.
- Python + Browser-Use demos showcasing shared Chrome sessions, CDP connectivity, and multi-agent orchestration.
- Vue 3 dashboards integrating MCP server management, terminal streaming, and VS Code-style explorers using Ant Design Vue components.

These assets will return in future commits as the roadmap items stabilize. For now, the repository remains documentation-first while new architecture and design specifications solidify.

## Contributing

1. Fork the repository and create a feature branch.
2. Align UI contributions with the Geist/Ant Design guidelines above (navigation sizing, grid spacing, typography, CSS-variable overrides).
3. For automation tooling, ensure code executes inside sandbox containers and includes error handling, audit logging, and resource limits.
4. Submit a pull request with summaries, tests (or rationale when tests are not applicable), and references to relevant roadmap items.

Please open issues if you have suggestions for sandbox orchestration, design tokens, multi-LLM support, or documentation gaps.
