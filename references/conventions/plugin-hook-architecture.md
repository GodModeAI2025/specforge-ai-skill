# SpecForge: Plugin & Hook Architecture (Conceptual Framework)

## 1. Introduction

As SpecForge evolves from a "soft" prompt-based skill into a deterministic Agentic Application, the limits of in-context learning become apparent. LLMs suffer from "Context Overflow" and "Eager Execution", often ignoring strict governance rules (like phase orchestration or formatting constraints) when executing complex tasks.

To achieve **Global Consistency**—ensuring that every new feature strictly adheres to project-wide design principles, architecture rules, and folder routing conventions without relying on the LLM's memory—SpecForge must transition its critical governance checks from Markdown instructions to **hardcoded platform plugins (hooks)**.

This document outlines the architecture for these hooks, combining the "Anti-Vibe-Coding" (Research-Plan-Implement) methodology with the deterministic gating principles of advanced AI harnesses.

## 2. Core Hook Concepts

These hooks are intended to be implemented within the AI execution environment (e.g., as MCP servers, IDE extensions, or agent execution intercepts).

### 2.1. Global Consistency & Harness Concepts

These hooks ensure that local changes do not violate global architectural integrity.

*   **The AI Validator Hook (Principle Gate)**
    *   **Problem:** System prompts cannot reliably evaluate complex architectural changes against global design principles.
    *   **Solution:** A secondary, fast LLM validation step (e.g., using `call_llm`) triggered at Phase Gate G3 (Plan → Implement).
    *   **Mechanism:** The hook reads the proposed `plan.md` and the central `constitution.md` (Single Source of Truth). It prompts the secondary model: *"Identify any architectural or structural violations in this plan against the constitution."* If a violation is found, the hook blocks the gate and forces the primary agent to revise the plan.

*   **Pre-Write Policy Enforcer (Path & Routing Linter)**
    *   **Problem:** The LLM might write sensitive files to public folders, violating information architecture rules.
    *   **Solution:** A hard intercept on the `Write`, `Edit`, or `Bash` tools.
    *   **Mechanism:** Before a file is written, a deterministic script evaluates the target path against the routing rules defined in `constitution.md` (or `specforge.json`). For instance, if a rule states that HR files must go to a specific internal directory, any attempt to write them to a shared/collaboration directory will throw a `Permission Denied` error, demanding user intervention.

*   **Context-Graph Traceability (Soft Recommendation)**
    *   **Problem:** Newly generated specifications often become isolated files, disconnected from the broader knowledge base.
    *   **Solution:** A post-creation validation hook.
    *   **Mechanism:** After creating a `spec.md` or `plan.md`, the system checks if these files contain valid backlinks to the central `constitution.md` and whether they have been registered in a central index (like a Zettelkasten or Knowledge Graph repository). If not, the agent is prompted to add these connections, ensuring a tightly woven information architecture without hardcoding specific local folder structures.

### 2.2. RPI (Anti-Vibe-Coding) Concepts

These hooks enforce the Research → Plan → Implement workflow to prevent hallucinations and undocumented drift.

*   **Context Masking Hook (Isolated Research via Sub-Agent Spawning)**
    *   **Problem:** Passing a "Feature Ticket" alongside the codebase context creates a cognitive bias; the LLM sees what it wants to see rather than what actually exists.
    *   **Solution:** The execution engine spawns an isolated sub-agent (`spawn_session`) during the Discover (Modus 9) phase.
    *   **Mechanism:** This sub-agent receives *only* the instruction to document the current state of specific files or systems, intentionally omitting the feature ticket. Once the objective `research.md` is returned, it is merged back into the main thread.

*   **Hard Gate-Checks (Spec-Linter via MCP Tool)**
    *   **Problem:** LLMs are terrible at self-evaluating against strict syntactic rules (e.g., "Did I avoid vague words like 'fast' or 'scalable'?").
    *   **Solution:** A deterministic Python/AST linter.
    *   **Mechanism:** Before passing Phase Gate G1 or G4, a local linter parses the markdown artifact. It checks for EARS syntax compliance, counts Gherkin scenarios, and flags SOPHIST violations (passive voice, generic actors). The gate remains locked until the linter returns an exit code of 0.

*   **State Machine Enforcer (Prompt Diet)**
    *   **Problem:** Asking an LLM to "stop and wait for user approval" often results in the LLM generating the research, the outline, and the entire plan in a single, massive response.
    *   **Solution:** Platform-level dynamic tool gating.
    *   **Mechanism:** The agent is given *only* the tools and prompts necessary for the current state (e.g., "Outline"). Write permissions for code or detailed plans are physically revoked. The state transitions strictly sequentially (or loops back on failure) via user UI interaction.

*   **Plan Fidelity Diff-Checker (Pre-Commit Interceptor)**
    *   **Problem:** "Vibe-Coding" during implementation leads to scope creep and undocumented changes.
    *   **Solution:** A hook that runs during the Review Phase (Gate G5) or pre-commit.
    *   **Mechanism:** The hook compares the git diff (`git diff HEAD --name-only`) against the list of files explicitly approved in `plan.md`. Any drift triggers an automatic F3 CONDITIONAL failure, requiring explicit human risk acceptance before proceeding.

## 3. Implementation Strategy

To ensure these rules remain CI/CD-friendly and independent of individual developer machine setups:

1.  **Repository-Relative Paths:** All hooks and linters operate on paths relative to the repository root (e.g., `references/conventions/`, `scripts/`).
2.  **Stateless Validation:** Validations rely on configuration files checked into the repository (e.g., `specforge.json`, `constitution.md`) rather than local environment variables.
3.  **Extensibility:** By standardizing the exit codes and JSON output of the CLI scripts (in the `scripts/` directory), these checks can be executed equally well by a local AI agent, a GitHub Action, or an MCP server.