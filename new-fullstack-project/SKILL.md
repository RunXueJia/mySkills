---
name: new-fullstack-project
description: Initialize a new full-stack project workspace by creating standard backend, frontend, and docs directories plus a project-level AGENTS.md from the bundled common full-stack project standard. Use when the user says "新建全栈项目", asks to initialize a full-stack project workspace, asks to create a backend/frontend/docs skeleton, asks to create AGENTS.md from the bundled standard, or wants a reusable full-stack project collaboration guide written into the current working directory.
---

# New Fullstack Project

## Purpose

Create a basic full-stack workspace skeleton and write `AGENTS.md` in the current conversation workspace using this skill's bundled full-stack project collaboration standard.

## Workflow

1. Confirm the current workspace path from the active shell working directory or thread context.
2. Use `scripts/create_agents.py` to create the standard directory skeleton and copy `references/fullstack-project-agents-template.md` into `<workspace>/AGENTS.md`.
3. Do not overwrite an existing `AGENTS.md` unless the user explicitly asks to replace or overwrite it.
4. Directory creation is idempotent: create missing directories and leave existing directories untouched.
5. Report the created or skipped `AGENTS.md` path and summarize created/skipped directories.

## Command

Use this pattern from any workspace:

```powershell
python "$env:USERPROFILE\.agents\skills\new-fullstack-project\scripts\create_agents.py" --workspace "<current workspace path>"
```

If the user explicitly asks to replace an existing file:

```powershell
python "$env:USERPROFILE\.agents\skills\new-fullstack-project\scripts\create_agents.py" --workspace "<current workspace path>" --force
```

## Directory Skeleton

The script creates these directories when missing:

```text
backend/
backend/app/
backend/app/api/
backend/app/api/v1/
backend/app/api/v1/endpoints/
backend/app/services/
backend/app/repositories/
backend/app/models/
backend/app/schemas/
backend/app/tasks/
backend/app/libs/
backend/sql/
backend/docs/
backend/docs/iterations/
frontend/
frontend/src/
frontend/src/api/
frontend/src/components/
frontend/src/components/common/
frontend/src/views/
frontend/src/stores/
frontend/src/router/
docs/
docs/iterations/
docs/deployment/
docs/api/
```

## Reference

The AGENTS.md content lives in:

```text
references/fullstack-project-agents-template.md
```
