---
name: auto-subagent-orchestrator
description: Use at the start of every task to decide whether the work can be decomposed, and when permitted by the active instructions, automatically start appropriate sub-agents while the main agent assigns work, tracks integration, reviews outputs, and provides fallback coverage.
---

# Auto Subagent Orchestrator

## Purpose

At the start of each task, quickly decide whether parallel sub-agents would materially improve speed, coverage, or reliability. The main agent remains responsible for planning, delegation, integration, review, and final correctness.

## Startup Checklist

1. Classify the task as simple, sequential, or decomposable.
2. Identify the immediate critical-path action the main agent should do locally.
3. Identify independent sidecar tasks that can run in parallel without blocking the next local action.
4. Check active system, developer, user, sandbox, and tool rules before starting any sub-agent.
5. If sub-agents are allowed and useful, start only the minimum necessary set.
6. After any sub-agent completes, reassess the remaining work before deciding whether another parallel wave is needed.

## When To Decompose

Decompose when at least one condition is true:

- The task has independent codebase areas, files, modules, or research questions.
- Verification can run in parallel with implementation.
- A bounded subtask can produce a patch or answer without blocking the main agent.
- Multiple independent failures need investigation.
- A review pass would catch realistic integration, safety, or regression risks.

Do not decompose when the task is trivial, fully sequential, highly coupled, ambiguous enough to require a user decision first, or when delegation is disallowed by higher-priority instructions.

## Main-Agent Responsibilities

- Own the plan, critical path, and final answer.
- Assign concrete, bounded tasks with clear file or responsibility ownership.
- Tell worker agents they are not alone in the codebase and must not revert others' edits.
- Continue useful non-overlapping work while sub-agents run.
- Review sub-agent outputs before trusting or integrating them.
- Resolve conflicts, fill gaps, and provide fallback implementation if a sub-agent fails.
- Validate the final combined result with the most relevant tests or checks available.

## Delegation Pattern

When delegation is allowed, use this sequence:

1. Create a concise plan with the main critical-path step and candidate sidecar tasks.
2. Spawn agents only for independent, well-scoped work.
3. Prefer worker agents for bounded patches and explorer agents for specific codebase questions.
4. Avoid duplicating work between the main agent and sub-agents.
5. Wait only when blocked on a sub-agent result.
6. Review changed files, integrate results, and run targeted validation.

## Iterative Re-Delegation

Sub-agent orchestration is not limited to the first wave. After one or more sub-agents complete, the main agent should re-evaluate the updated state and may start a new wave of sub-agents when the remaining work has newly independent tasks.

Use iterative re-delegation when:

- A completed investigation reveals multiple independent fixes or follow-up questions.
- A completed implementation exposes separate validation, compatibility, or regression checks.
- Integration creates distinct cleanup tasks that can be handled without blocking the main critical path.
- Several failures remain and can be assigned to separate owners.

For each new wave:

1. Summarize what changed and what remains.
2. Confirm the next tasks are independent, bounded, and useful in parallel.
3. Assign clear ownership and context from prior sub-agent results.
4. Keep the main agent on the immediate critical path while the new wave runs.
5. Stop spawning when remaining work is sequential, low value, blocked on a decision, or ready for final validation.

The main agent controls iterative re-delegation. Sub-agents should not independently spawn descendants unless the active instructions and the specific delegated prompt explicitly allow it.

## Prompt Template

Use concise prompts like:

```text
You are not alone in this codebase. Do not revert edits made by others. Own [files/modules/responsibility]. Implement or investigate [specific task]. Keep changes minimal, follow existing style, validate if practical, and report changed files plus any blockers.
```

## Safety Rules

- Higher-priority instructions always override this skill.
- Do not start sub-agents if the current environment or active instructions require explicit user authorization and it has not been given.
- Do not delegate destructive actions, credential handling, production changes, or vague work.
- Do not use sub-agents as a substitute for main-agent review.
- Close sub-agents that are no longer needed.
