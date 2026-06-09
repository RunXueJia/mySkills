---
name: workspace-task-checklist
description: This is the user's standing request to evaluate at the start of every task whether a workspace task checklist document is needed. Use when a task is multi-step, long-running, cross-file, implementation-heavy, verification-heavy, uses sub-agents, needs progress tracking, or when the user asks for a task list/checklist/计划/任务清单. When needed, directly create and keep updating a Chinese Markdown checklist under the current workspace docs/task/ directory, including a record of files modified during the task.
---

# Workspace Task Checklist

## Purpose

At the start of each task, decide whether a persistent task checklist document is useful. If it is useful, create one under `docs/task/` in the current workspace and update it as the task progresses. The generated task document content must be Chinese.

This skill is a documentation companion to planning and sub-agent orchestration. It does not replace normal conversation updates or `update_plan`; it creates a durable project-local record when the work is large enough to justify it.

## When To Create A Checklist

Create `docs/task/YYYY-MM-DD-HH-MM-SS-任务名.md` when one or more conditions is true:

- The task has three or more meaningful steps.
- The task touches multiple files, modules, services, pages, or repositories.
- The task involves implementation plus verification.
- The task may take long enough that progress needs to be recoverable after interruption.
- The task uses sub-agents or parallel work.
- The task has explicit phases such as discovery, implementation, validation, cleanup, and delivery.
- The user asks for a task list, checklist, plan document, or `任务清单`.

Do not create a checklist for trivial work:

- Simple Q&A.
- Reading or summarizing one short file.
- Running one simple command.
- Tiny single-file edits with obvious verification.
- Cases where the user explicitly says not to create extra files.

## Workflow

1. Classify the task as trivial, simple, or checklist-worthy.
2. If checklist-worthy, immediately create a checklist before substantial work starts.
3. Put the checklist at `<workspace>/docs/task/`.
4. Name the checklist as `YYYY-MM-DD-HH-MM-SS-任务名.md`; derive `任务名` from the task title and only remove characters that are unsafe for filenames.
5. Keep the checklist concise and Chinese: title, status, checklist items, progress log, modified files, validation, and final result.
6. Update the document after each meaningful transition:
   - Mark an item `in_progress` when starting it.
   - Mark it `completed` after it is actually done.
   - Mark it `blocked` with a short reason when progress stops on that item.
   - Append Chinese log entries for important discoveries, user decisions, validation results, and final outcome.
7. Use these Chinese section headings in task documents: `## 任务清单`, `## 进展日志`, `## 修改文件`, `## 验证`, and `## 最终结果`.
8. Whenever files are created, modified, moved, copied, or deleted for the task, record those paths in the `## 修改文件` section. Use paths relative to the workspace or absolute paths; the script stores resolved absolute paths.
9. Before the final response, confirm the `## 修改文件` section reflects the actual files changed during the task. If no files were changed, leave `- 待记录。` or replace it with a clear Chinese no-file-changes note.
10. Do not update on every tiny command. Update after real task-state changes or after a meaningful group of file changes.
11. Mention the checklist path in the final answer when one was created.

## Script

Use `scripts/task_checklist.py` for deterministic creation and updates.

Create a checklist:

```powershell
python "$env:USERPROFILE\.agents\skills\workspace-task-checklist\scripts\task_checklist.py" init --workspace "<workspace>" --title "<task title>" --item "<step 1>" --item "<step 2>"
```

Update an item by 1-based index:

```powershell
python "$env:USERPROFILE\.agents\skills\workspace-task-checklist\scripts\task_checklist.py" update --workspace "<workspace>" --index 1 --status in_progress --note "开始调研。"
python "$env:USERPROFILE\.agents\skills\workspace-task-checklist\scripts\task_checklist.py" update --workspace "<workspace>" --index 1 --status completed --note "调研完成。"
```

Add a new item:

```powershell
python "$env:USERPROFILE\.agents\skills\workspace-task-checklist\scripts\task_checklist.py" add --workspace "<workspace>" --item "运行针对性验证"
```

Append a progress note:

```powershell
python "$env:USERPROFILE\.agents\skills\workspace-task-checklist\scripts\task_checklist.py" log --workspace "<workspace>" --note "重要发现或验证结果。"
```

Record files modified during the task:

```powershell
python "$env:USERPROFILE\.agents\skills\workspace-task-checklist\scripts\task_checklist.py" files --workspace "<workspace>" --path "<changed file>" --path "<another changed file>" --note "简短修改说明。"
```

Mark the task complete:

```powershell
python "$env:USERPROFILE\.agents\skills\workspace-task-checklist\scripts\task_checklist.py" complete --workspace "<workspace>" --note "已交付最终结果。"
```

The script stores the current checklist pointer in `docs/task/.current-task-checklist`, so later updates can omit `--file` during the same workspace task.
