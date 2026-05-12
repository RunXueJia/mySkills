---
name: summarize-task
description: Create a Chinese task summary when the user sends "/总结任务" or asks to summarize the current task into the Desktop task folder. Use this skill to write a dated Chinese Markdown summary under the user's Desktop\task directory, named with the current date plus a Chinese title, recording what was created, how to view it, how to cancel/remove it, and current verification results.
---

# Summarize Task

When the user sends `/总结任务`, create a Chinese Markdown summary for the current task.

## Output Location

Write the summary to:

`C:\Users\16084\Desktop\task`

Create the directory if it does not exist.

## File Naming

Use this filename pattern:

`YYYY-MM-DD_中文标题.md`

Rules:

- Use the current local date.
- Use a concise Chinese title that describes the task.
- Prefer Chinese words over English in the title.
- Keep the title filesystem-safe; avoid `\ / : * ? " < > |`.

Example:

`2026-05-06_开机自动关闭网络代理任务概要.md`

## Content Requirements

Write the summary in Chinese. Include these sections when applicable:

- `目标`: What the user wanted to accomplish.
- `已创建内容`: Files, scripts, tasks, configs, or other artifacts created or changed.
- `如何查看`: Commands or GUI steps for inspecting the result.
- `如何手动执行`: Manual run commands if relevant.
- `如何取消或卸载`: Commands or steps to remove, disable, or undo the created behavior.
- `当前验证结果`: What was verified, including command outcomes or observed state.
- `注意事项`: Important limitations, follow-up risks, or known interactions.

If a section is not relevant, omit it rather than inventing content.

## Workflow

1. Review the current conversation and local artifacts relevant to the task.
2. Confirm the Desktop `task` directory exists or create it.
3. Write a concise but useful Markdown summary in Chinese.
4. Prefer `apply_patch` for file creation when possible.
5. In the final response, provide a clickable link to the created summary file.

## Style

- Use clear Chinese headings.
- Use exact paths and commands.
- Keep the summary practical and auditable.
- Do not use English filenames unless the existing artifact name must be quoted.
