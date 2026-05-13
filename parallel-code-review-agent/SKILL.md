---
name: parallel-code-review-agent
description: Use this skill when the user wants a single orchestrator agent to run multiple parallel code review agents, review a repository diff, PR, branch, or changed files from several dimensions, and produce a merged final review.
---

# Parallel Code Review Agent

## Purpose

Act as the main code review orchestrator. The main agent owns scope, delegation, result merging, final judgment, and final output. Sub-agents are temporary reviewers created only when parallel review is useful and allowed.

## Trigger

Use this workflow when the user asks for any of the following:

- Parallel code review
- Multiple agents reviewing code
- Review current diff, PR, branch, or changed files
- Code review from correctness, security, tests, maintainability, performance, or architecture angles
- "Use the parallel code review agent"

## Inputs

Accept one or more of:

- Repository path
- Review scope: current uncommitted diff, staged diff, branch comparison, PR, commit range, or specific files
- User focus areas, such as security, tests, performance, API compatibility, frontend UX, or migration risk

If no scope is provided, default to the current repository's uncommitted changes.

## Main Workflow

1. Inspect the review scope:
   - `git status --short`
   - `git diff --stat`
   - `git diff`
   - `git diff --cached` when staged changes matter
   - relevant project scripts, tests, and changed file context

2. Decide whether parallel review is useful:
   - Use sub-agents when the diff is non-trivial, touches multiple areas, or the user explicitly asks for multiple agents.
   - Keep the review local when the change is tiny or the remaining work is sequential.

3. Start the minimum useful reviewer set:
   - Correctness Reviewer
   - Security Reviewer
   - Test Coverage Reviewer
   - Maintainability Reviewer

   Add specialized reviewers only when relevant:
   - Performance Reviewer
   - API Compatibility Reviewer
   - Frontend UX Reviewer
   - Migration/Rollout Reviewer

4. Reviewer rules:
   - Review only. Do not edit files.
   - Focus on real bugs, regressions, security issues, missing tests, and maintainability risks.
   - Avoid style-only comments unless they create a concrete risk.
   - Each finding must include severity, file, line, problem, impact, and suggested fix.
   - Say clearly when no issue is found for that review dimension.

5. Merge reviewer outputs:
   - Remove duplicates.
   - Discard weak, speculative, or out-of-scope findings.
   - Verify file and line references where practical.
   - Sort by severity: P0, P1, P2, P3.

6. Final output must use a code-review stance:
   - Findings first.
   - Then open questions or assumptions.
   - Then a short summary.
   - Include validation or test gaps when relevant.

## Reviewer Prompt Template

Use concise prompts like this when creating reviewer sub-agents:

```text
You are not alone in this codebase. Do not edit files or revert changes. You are reviewing only the assigned dimension: [DIMENSION].

Review scope:
[SCOPE]

Your task:
- Find concrete bugs, regressions, security issues, missing tests, or maintainability risks in your dimension.
- Ignore style-only preferences unless they create real risk.
- Return findings only when they are supported by the changed code.

Each finding must include:
- Severity: P0/P1/P2/P3
- File and line
- Problem
- Impact
- Suggested fix

If you find no issues, say: "No findings for [DIMENSION]."
```

## Severity Guide

- P0: Critical production breakage, data loss, credential exposure, or severe security issue.
- P1: Likely user-facing regression, authorization bypass, corrupt data, or broken core workflow.
- P2: Real bug, missing important test, edge-case regression, or maintainability issue with clear future cost.
- P3: Minor risk, low-impact issue, or cleanup worth considering.

## Final Output Format

```text
Findings
- [P1] file:line - Problem
  Impact: ...
  Suggested fix: ...

Open Questions
- ...

Summary
- ...

Validation Gaps
- ...
```

If there are no findings, say so directly and mention any residual test or validation risk.
