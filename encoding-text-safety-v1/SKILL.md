---
name: encoding-text-safety-v1
description: Enforce UTF-8 text safety for source code and configuration changes. Use when Codex creates or edits code, config, docs, prompts, comments, logs, or user-visible text and must keep files in UTF-8 without BOM, detect mojibake, repair readable text before functional edits, verify BOM status, and report whether any encoding-only fixes were made.
---

# Encoding Text Safety V1

## Overview

Apply these rules before and after editing any source file, configuration file, comment, prompt, or user-visible text.
Default to UTF-8 without BOM unless the repository explicitly requires another encoding.

## Default Encoding

- Use UTF-8 for all source and configuration files.
- Save files as UTF-8 without BOM by default.
- Do not use GBK, ANSI, UTF-16, or other encodings unless the repository has an explicit rule that requires them.

## Check Before Editing

1. Read the target file and inspect for content-level mojibake before making functional changes.
2. Check for obvious corruption such as known mojibake fragments or the Unicode replacement character (`U+FFFD`).
3. Check whether the file starts with a UTF-8 BOM: `EF BB BF`.
4. If text is corrupted, repair the readable text first, then continue with the intended task.
5. Avoid carrying broken text forward into a functional change.

## Write Safely

- Do not use write paths that may silently change encoding.
- On Windows and PowerShell, avoid `Out-File` for source or config writes unless the encoding behavior is fully controlled and verified.
- Use only write methods that explicitly guarantee UTF-8 without BOM.
- Do not skip encoding confirmation just because the file looks normal in the terminal or editor.

## Validate After Editing

Run both checks after every text change and before build or test steps:

1. Verify that the file has no UTF-8 BOM.
2. Verify that the file contains no `U+FFFD` replacement character and no common mojibake fragments.

If either check fails, fix the file before proceeding.

## Repair Strategy

- If the damaged text is reversibly recoverable, restore the original meaning.
- If the text is not reversibly recoverable, rewrite it into clear Chinese or English.
- Limit the repair to comments, prompts, labels, messages, and other text content.
- Do not change business logic during a text-repair pass.
- Prioritize readability and accuracy for user-visible error messages.

## Scope Expansion

- If one file in a directory has mojibake, spot-check related files in the same directory.
- If similar issues are found, repair them in the same pass when practical.
- Keep encoding repair separate from logic changes whenever possible.

## Exceptions

- Follow a repository-specific non-UTF-8 rule only when the repository explicitly requires it.
- State the reason for that exception in the change summary.

## Reporting Requirements

Include these points in the final change summary:

- Whether a BOM was found and fixed.
- Whether content-level mojibake was found and fixed.
- Whether business logic changed. This should usually be `no` for encoding-only repairs.
- If the work was only an encoding repair, report the result of a minimal build or validation step as well.

## Practical Notes

- Prefer deterministic write methods and then verify the actual bytes on disk.
- Treat encoding repair as a prerequisite cleanup step, not an optional polish step.
- When both encoding repair and logic changes are required, finish the text cleanup first and keep the two concerns clearly separated in the summary.
