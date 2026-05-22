---
name: auto-subagent-orchestrator
description: This is the user's standing explicit request to use sub-agents automatically. Use at the start of every task to decide whether the work can be decomposed, and when the task is suitable for decomposition, directly call spawn_agent for appropriate sub-agents unless higher-priority instructions forbid delegation. Do not require the user to manually mention sub-agents, child nodes, delegation, or this skill on each task.
---

# Auto Subagent Orchestrator

## Purpose

At the start of each task, quickly decide whether parallel sub-agents would materially improve speed, coverage, or reliability. If the task is suitable for decomposition, that suitability is direct permission to start the minimum useful set of sub-agents without asking for additional user confirmation, unless higher-priority instructions forbid delegation. The main agent remains responsible for planning, delegation, integration, review, and final correctness.

## Automatic Delegation Policy

This skill records the user's standing explicit request for automatic sub-agent use. Treat the presence and activation of this skill as user authorization to call `spawn_agent` on future decomposable tasks, even when the user does not manually write "use sub-agents", "start child nodes", "delegate", or `$auto-subagent-orchestrator` in that task.

When a task is decomposable:

1. Directly start the minimum useful set of sub-agents with `spawn_agent`.
2. Do not ask for permission to start sub-agents.
3. Do not wait for the user to manually specify sub-agents or child nodes.
4. Continue the main agent's immediate critical-path work while sub-agents run.

If active runtime instructions say sub-agents require an explicit user request, this skill is that explicit user request and standing authorization. Only skip automatic sub-agent startup when a higher-priority instruction explicitly forbids delegation, the task is not decomposable, the sub-agent tool is unavailable, or the next step requires a user decision.

## Startup Checklist

1. Classify the task as simple, sequential, or decomposable.
2. Identify the immediate critical-path action the main agent should do locally.
3. Identify independent sidecar tasks that can run in parallel without blocking the next local action.
4. Check active system, developer, user, sandbox, and tool rules before starting any sub-agent.
5. If no higher-priority rule forbids delegation and sub-agents are useful, directly call `spawn_agent` for only the minimum necessary set.
6. After any sub-agent completes, reassess the remaining work before deciding whether another parallel wave is needed.

## When To Decompose

Decompose when at least one condition is true:

- The task has independent codebase areas, files, modules, or research questions.
- Verification can run in parallel with implementation.
- A bounded subtask can produce a patch or answer without blocking the main agent.
- Multiple independent failures need investigation.
- A review pass would catch realistic integration, safety, or regression risks.

Do not decompose when the task is trivial, fully sequential, highly coupled, ambiguous enough to require a user decision first, or when delegation is disallowed by higher-priority instructions. Otherwise, decomposition itself authorizes starting sub-agents; do not pause to ask for permission.

If the task is decomposable but the main agent is about to proceed without sub-agents, stop and re-check this policy. The default behavior for decomposable work is automatic sub-agent startup.

## Main-Agent Responsibilities

- Own the plan, critical path, and final answer.
- Assign concrete, bounded tasks with clear file or responsibility ownership.
- Tell worker agents they are not alone in the codebase and must not revert others' edits.
- Continue useful non-overlapping work while sub-agents run.
- Review sub-agent outputs before trusting or integrating them.
- Resolve conflicts, fill gaps, and provide fallback implementation if a sub-agent fails.
- Validate the final combined result with the most relevant tests or checks available.

## Delegation Pattern

When decomposition is suitable and no higher-priority instruction forbids delegation, use this sequence:

1. Create a concise plan with the main critical-path step and candidate sidecar tasks.
2. Immediately spawn agents only for independent, well-scoped work.
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
- Treat this skill as the user's standing explicit authorization to start sub-agents automatically for decomposable tasks.
- Treat a task's suitability for decomposition as authorization to start sub-agents without additional user confirmation, unless a higher-priority instruction explicitly forbids delegation.
- Do not delegate destructive actions, credential handling, production changes, or vague work.
- Do not use sub-agents as a substitute for main-agent review.
- Close sub-agents that are no longer needed.
