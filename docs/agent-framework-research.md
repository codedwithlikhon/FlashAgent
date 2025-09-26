# Agent Framework and Design System Research

## Overview
This document summarizes findings about prominent agent frameworks and Vercel's Geist design system, then distils opportunities for improving FlashAgent based on those observations.

## Framework Snapshots

### AI Manus (Simpleyyt/ai-manus)
- **Sandboxed execution.** Every conversation launches an isolated Docker sandbox that runs Chrome, tool APIs, and a Plan-Act agent, providing security and enabling real-time task takeover.
- **Rich toolset.** Built-in tools (terminal, browser, filesystem, web search, messaging) operate inside the sandbox, can be extended via the MCP interface, and are observable for manual intervention.
- **Session persistence.** Task history lives in MongoDB or Redis, supports background jobs, interruptions, uploads/downloads, and multi-language UI with authentication.
- **Deployment.** Docker Compose bundles backend, frontend, and sandbox services; roadmap includes mobile/Windows sandboxes and multi-cluster support.

**Key takeaways for FlashAgent:** adopt per-session sandboxing, persistent session storage, and extensible tool APIs for safer, resumable workflows.

### Browser Use (browser-use/browser-use)
- **Goal.** Provide “no-code” browser automation for repetitive web tasks via a persistent Playwright-powered browser instance.
- **Strengths.** Handles dynamic sites, logins, cookies, multi-step workflows, and session reuse. Widely integrated (70k+ stars) and offers hosted/cloud variations plus macOS native automation.
- **Limitations.** Focuses exclusively on browser control—no bundled sandboxing, LLM orchestration, or multi-tool governance.

**Key takeaways for FlashAgent:** leverage Browser Use as a reliable browser executor while layering missing orchestration, memory, and safety features.

### Lemon AI (hexdocom/lemonai)
- **Local-first.** Runs entirely on the user’s machine with Ollama-provided local LLMs (DeepSeek, Qwen, Llama, Gemma) and optional cloud providers.
- **VM sandbox.** Executes tasks inside a full virtual machine for stronger isolation than containers, protecting host OS during code execution.
- **Capabilities.** Supports deep research, web browsing, code generation, data analysis, and maintains a knowledge base for self-learning.
- **Deployment.** Offers one-click desktop, Docker, or subscription packages and emphasizes 10x cost reduction compared to SaaS agents.

**Key takeaways for FlashAgent:** consider optional VM-level sandboxes, local LLM support, and reusable “experience” storage to reduce dependence on external APIs.

### OpenHands (All-Hands-AI/OpenHands)
- **Developer-centric UI.** Combines chat, change tracking, embedded VS Code, terminal, browser, and notebook panels so users can monitor and intervene in agent actions.
- **Tool parity with developers.** Agents can modify code, run shells, browse the web, call APIs, and copy snippets—mirroring a human engineer’s environment.
- **Deployment.** Runs in managed cloud or locally with user-provided API keys; features micro-agents and repository customisation.

**Key takeaways for FlashAgent:** build a unified control plane with transparent tooling, expose diffs, and make it easy for humans to collaborate with agents mid-task.

### Vercel Geist Design System
- **Colors.** Uses dual background tokens and ten-step color scales (default, hover, active, borders, strong backgrounds, high-contrast text) to guarantee accessibility.
- **Typography.** Supplies semantic text classes (heading, button, label, copy) with presets for size, line height, letter spacing, and weight; encourages `<strong>` modifiers for emphasis.
- **Components & foundations.** Provides consistent UI components, iconography, spacing, and brand guidelines for cohesive experiences.

**Key takeaways for FlashAgent:** adopt Geist tokens (colors, typography, spacing) or map them to existing Ant Design primitives to improve visual consistency and accessibility.

## Improvement Opportunities for FlashAgent

1. **Design System Modernisation**
   - Integrate Geist color and typography tokens into the Vue dashboard via CSS variables or a theme adapter.
   - Replace ad-hoc styling with Geist-inspired component patterns to improve contrast and accessibility.

2. **Sandboxed Execution Model**
   - Launch per-conversation containers (inspired by AI Manus) with browser, terminal, and tool APIs to safeguard the host and enable task resumption.
   - Explore VM-based isolation (à la Lemon AI) for users needing stronger guarantees.

3. **Tooling and Plugin Architecture**
   - Provide built-in terminal, filesystem, browser, and search tools that run inside the sandbox.
   - Expose a plugin API so teams can register custom tools (e.g., Slack, database connectors) via MCP or lightweight adapters.

4. **Session Memory and Persistence**
   - Record task history, events, and artefacts in a database for later retrieval, audit, or continuation.
   - Support background tasks, manual stop/resume, and cross-session knowledge accumulation.

5. **Unified Developer Experience**
   - Extend the dashboard to surface chat reasoning, action history, diffs, terminal output, and browser previews in a single view similar to OpenHands.
   - Provide controls for human-in-the-loop approval, replay, or manual override.

6. **LLM Flexibility and Local Mode**
   - Support multiple LLM back-ends and configurable parameters, plus local inference via Ollama or other runtimes.
   - Add cost controls and caching to avoid redundant model calls.

7. **Deployment & Operations**
   - Publish Docker Compose stacks for orchestrating frontend, backend, sandboxes, and databases.
   - Plan for multi-tenant scaling, monitoring, authentication, and access control.

8. **Documentation & Community**
   - Expand docs with architecture diagrams, extension guides, and advanced tutorials.
   - Foster community channels for feedback, templates, and shared plugins.

## Next Steps
- Prototype Geist-themed styling in the existing Vue dashboard to evaluate effort and compatibility.
- Define requirements for sandbox orchestration (container vs VM) and storage (MongoDB, Postgres, Redis).
- Draft a plugin contract that mirrors MCP capabilities while remaining simple to implement.
- Document a phased roadmap so contributors can tackle discrete enhancements without overwhelming scope.

This research should serve as a foundation for prioritising FlashAgent’s evolution from example repository to production-ready agent platform.
