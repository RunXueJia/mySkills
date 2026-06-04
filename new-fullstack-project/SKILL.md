---
name: new-fullstack-project
description: Create a project-level AGENTS.md for a new full-stack project in the current conversation workspace. Use when the user says "新建全栈项目", asks to initialize a full-stack project workspace, asks to create AGENTS.md from the bundled common full-stack project standard, or wants a reusable full-stack project collaboration guide written into the current working directory.
---

# New Fullstack Project

## Purpose

Create `AGENTS.md` in the current conversation workspace using this skill's bundled full-stack project collaboration standard.

## Workflow

1. Confirm the current workspace path from the active shell working directory or thread context.
2. Use `scripts/create_agents.py` to copy `references/fullstack-project-agents-template.md` into `<workspace>/AGENTS.md`.
3. Do not overwrite an existing `AGENTS.md` unless the user explicitly asks to replace or overwrite it.
4. Report the created file path and whether any overwrite was skipped.

## Command

Use this pattern from any workspace:

```powershell
python "$env:USERPROFILE\.agents\skills\new-fullstack-project\scripts\create_agents.py" --workspace "<current workspace path>"
```

If the user explicitly asks to replace an existing file:

```powershell
python "$env:USERPROFILE\.agents\skills\new-fullstack-project\scripts\create_agents.py" --workspace "<current workspace path>" --force
```

## Reference

The AGENTS.md content lives in:

```text
references/fullstack-project-agents-template.md
```
