from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys


STATUS_CHOICES = ("pending", "in_progress", "completed", "blocked", "skipped")
STATUS_LABELS = {
    "pending": "待处理",
    "in_progress": "进行中",
    "completed": "已完成",
    "blocked": "已阻塞",
    "skipped": "已跳过",
}
DEFAULT_ITEMS = [
    "确认范围和约束",
    "执行主要工作",
    "验证结果",
    "汇报结果和后续事项",
]
HEADING_CHECKLIST = "## 任务清单"
HEADING_PROGRESS = "## 进展日志"
HEADING_MODIFIED_FILES = "## 修改文件"
HEADING_VALIDATION = "## 验证"
HEADING_FINAL = "## 最终结果"
SECTION_ALIASES = {
    HEADING_CHECKLIST: ("## Checklist",),
    HEADING_PROGRESS: ("## Progress Log",),
    HEADING_MODIFIED_FILES: ("## Modified Files",),
    HEADING_VALIDATION: ("## Validation",),
    HEADING_FINAL: ("## Final Result",),
}
PENDING_LINES = {"- Pending.", "- 待记录。", "- 待验证。", "- 待完成。"}


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_task_name(value: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", value.strip())
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-. ")
    return name[:80] or "task"


def workspace_path(value: str) -> Path:
    return Path(value).resolve()


def task_dir(workspace: Path) -> Path:
    return workspace / "docs" / "task"


def current_pointer(workspace: Path) -> Path:
    return task_dir(workspace) / ".current-task-checklist"


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def format_item(text: str, status: str = "pending") -> str:
    clean = re.sub(r"\s+", " ", text.strip())
    if status == "completed":
        return f"- [x] {clean}"
    if status == "pending":
        return f"- [ ] {clean}"
    return f"- [ ] [{STATUS_LABELS.get(status, status)}] {clean}"


def strip_status(text: str) -> str:
    cleaned = re.sub(r"^\s*\[[^\]]+\]\s+", "", text.strip())
    return cleaned


def checklist_path_from_args(workspace: Path, file_arg: str | None) -> Path:
    if file_arg:
        candidate = Path(file_arg)
        if not candidate.is_absolute():
            candidate = workspace / candidate
        return candidate.resolve()

    pointer = current_pointer(workspace)
    if pointer.is_file():
        pointer_text = read_text(pointer).strip()
        if pointer_text:
            candidate = Path(pointer_text)
            if not candidate.is_absolute():
                candidate = workspace / candidate
            if candidate.is_file():
                return candidate.resolve()

    directory = task_dir(workspace)
    files = sorted(directory.glob("*.md"), key=lambda path: path.stat().st_mtime, reverse=True)
    if files:
        return files[0].resolve()

    raise FileNotFoundError("No task checklist found. Run the init command first.")


def remember_current(workspace: Path, path: Path) -> None:
    directory = task_dir(workspace)
    directory.mkdir(parents=True, exist_ok=True)
    write_text(current_pointer(workspace), str(path.resolve()))


def update_header(lines: list[str], status: str | None = None) -> list[str]:
    updated = False
    status_updated = status is None
    for index, line in enumerate(lines):
        if line.startswith("- Workspace:"):
            lines[index] = line.replace("- Workspace:", "- 工作区:", 1)
        elif line.startswith("- Created:"):
            lines[index] = line.replace("- Created:", "- 创建时间:", 1)
        elif line.startswith("- Updated:") or line.startswith("- 更新时间:"):
            lines[index] = f"- 更新时间: {now_text()}"
            updated = True
        elif line.startswith("- Status:") or line.startswith("- 状态:"):
            if status is not None:
                lines[index] = f"- 状态: {STATUS_LABELS.get(status, status)}"
                status_updated = True
            elif line.startswith("- Status:"):
                current_status = line.split(":", 1)[1].strip()
                lines[index] = f"- 状态: {STATUS_LABELS.get(current_status, current_status)}"

    if not updated:
        lines.insert(1, f"- 更新时间: {now_text()}")
    if not status_updated:
        lines.insert(1, f"- 状态: {STATUS_LABELS.get(status or '', status or '')}")
    return lines


def ensure_section(lines: list[str], heading: str) -> int:
    aliases = (heading, *SECTION_ALIASES.get(heading, ()))
    for index, line in enumerate(lines):
        if line.strip() in aliases:
            lines[index] = heading
            return index
    if lines and lines[-1].strip():
        lines.append("")
    lines.append(heading)
    return len(lines) - 1


def append_log(lines: list[str], note: str | None) -> list[str]:
    if not note:
        return lines
    log_index = ensure_section(lines, HEADING_PROGRESS)
    insert_index = len(lines)
    for index in range(log_index + 1, len(lines)):
        if lines[index].startswith("## "):
            insert_index = index
            break
    if insert_index > log_index + 1 and not lines[insert_index - 1].strip():
        insert_index -= 1
    lines.insert(insert_index, f"- {now_text()} - {note}")
    return lines


def section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    start = ensure_section(lines, heading)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return start, end


def normalize_modified_file(workspace: Path, value: str) -> str:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = workspace / candidate
    return str(candidate.resolve())


def modified_file_line(path: str, note: str | None = None) -> str:
    if note:
        return f"- `{path}` - {note}"
    return f"- `{path}`"


def extract_modified_path(line: str) -> str | None:
    match = re.match(r"^- `([^`]+)`(?:\s+-\s+.*)?$", line.strip())
    if not match:
        return None
    return match.group(1)


def update_modified_files(lines: list[str], paths: list[str], note: str | None) -> list[str]:
    start, end = section_bounds(lines, HEADING_MODIFIED_FILES)
    existing_lines = [
        line
        for line in lines[start + 1 : end]
        if line.strip() and line.strip() not in PENDING_LINES
    ]
    positions = {
        extracted: index
        for index, line in enumerate(existing_lines)
        if (extracted := extract_modified_path(line)) is not None
    }

    for path in paths:
        line = modified_file_line(path, note)
        if path in positions:
            existing_lines[positions[path]] = line
        else:
            positions[path] = len(existing_lines)
            existing_lines.append(line)

    if not existing_lines:
        existing_lines = ["- 待记录。"]

    replacement = [lines[start]] + existing_lines
    if end < len(lines) and lines[end].strip():
        replacement.append("")
    return lines[:start] + replacement + lines[end:]


def checklist_line_indices(lines: list[str]) -> list[int]:
    start = ensure_section(lines, HEADING_CHECKLIST)

    indices: list[int] = []
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("## "):
            break
        if re.match(r"^- \[[ xX]\] ", line):
            indices.append(index)
    return indices


def extract_item_text(line: str) -> str:
    match = re.match(r"^- \[[ xX]\]\s+(.*)$", line)
    if not match:
        return line
    return strip_status(match.group(1))


def build_initial_content(workspace: Path, title: str, items: list[str], note: str | None) -> str:
    timestamp = now_text()
    checklist_items = items or DEFAULT_ITEMS
    lines = [
        f"# {title}",
        "",
        f"- 工作区: `{workspace}`",
        f"- 创建时间: {timestamp}",
        f"- 更新时间: {timestamp}",
        f"- 状态: {STATUS_LABELS['in_progress']}",
        "",
        HEADING_CHECKLIST,
    ]
    lines.extend(format_item(item) for item in checklist_items)
    lines.extend(
        [
            "",
            HEADING_PROGRESS,
            f"- {timestamp} - {note or '已创建任务清单。'}",
            "",
            HEADING_MODIFIED_FILES,
            "- 待记录。",
            "",
            HEADING_VALIDATION,
            "- 待验证。",
            "",
            HEADING_FINAL,
            "- 待完成。",
        ]
    )
    return "\n".join(lines) + "\n"


def init_checklist(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    if not workspace.is_dir():
        print(f"ERROR workspace directory not found: {workspace}", file=sys.stderr)
        return 1

    directory = task_dir(workspace)
    directory.mkdir(parents=True, exist_ok=True)
    filename = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{safe_task_name(args.title)}.md"
    path = directory / filename
    content = build_initial_content(workspace, args.title, args.items or [], args.note)
    write_text(path, content)
    remember_current(workspace, path)
    print(f"CHECKLIST_CREATED {path}")
    return 0


def update_item(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    path = checklist_path_from_args(workspace, args.file)
    lines = read_text(path).splitlines()
    indices = checklist_line_indices(lines)
    if args.index < 1 or args.index > len(indices):
        print(f"ERROR checklist item index out of range: {args.index}", file=sys.stderr)
        return 1

    line_index = indices[args.index - 1]
    item_text = extract_item_text(lines[line_index])
    lines[line_index] = format_item(item_text, args.status)
    lines = update_header(lines, "in_progress")
    lines = append_log(lines, args.note)
    write_text(path, "\n".join(lines) + "\n")
    remember_current(workspace, path)
    print(f"CHECKLIST_UPDATED {path}")
    return 0


def add_item(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    path = checklist_path_from_args(workspace, args.file)
    lines = read_text(path).splitlines()
    checklist_index = ensure_section(lines, HEADING_CHECKLIST)
    insert_index = len(lines)
    for index in range(checklist_index + 1, len(lines)):
        if lines[index].startswith("## "):
            insert_index = index
            break
    if insert_index > 0 and lines[insert_index - 1].strip():
        lines.insert(insert_index, "")
        insert_index += 1
    lines.insert(insert_index, format_item(args.item, args.status))
    lines = update_header(lines, "in_progress")
    lines = append_log(lines, args.note)
    write_text(path, "\n".join(lines) + "\n")
    remember_current(workspace, path)
    print(f"CHECKLIST_ITEM_ADDED {path}")
    return 0


def append_note(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    path = checklist_path_from_args(workspace, args.file)
    lines = read_text(path).splitlines()
    lines = update_header(lines, None)
    lines = append_log(lines, args.note)
    write_text(path, "\n".join(lines) + "\n")
    remember_current(workspace, path)
    print(f"CHECKLIST_LOGGED {path}")
    return 0


def record_modified_files(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    path = checklist_path_from_args(workspace, args.file)
    modified_paths = [normalize_modified_file(workspace, value) for value in args.paths]
    lines = read_text(path).splitlines()
    lines = update_header(lines, None)
    lines = update_modified_files(lines, modified_paths, args.note)
    lines = append_log(lines, args.log_note)
    write_text(path, "\n".join(lines) + "\n")
    remember_current(workspace, path)
    print(f"CHECKLIST_FILES_UPDATED {path}")
    return 0


def complete_task(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    path = checklist_path_from_args(workspace, args.file)
    lines = read_text(path).splitlines()
    lines = update_header(lines, "completed")
    lines = update_modified_files(lines, [], None)
    lines = append_log(lines, args.note or "任务已完成。")
    final_index, final_end = section_bounds(lines, HEADING_FINAL)
    final_lines = [
        line
        for line in lines[final_index + 1 : final_end]
        if line.strip() and line.strip() not in PENDING_LINES
    ]
    final_lines.append(f"- {args.note or '已完成。'}")
    replacement = [lines[final_index]] + final_lines
    if final_end < len(lines) and lines[final_end].strip():
        replacement.append("")
    lines = lines[:final_index] + replacement + lines[final_end:]
    write_text(path, "\n".join(lines) + "\n")
    remember_current(workspace, path)
    print(f"CHECKLIST_COMPLETED {path}")
    return 0


def show_current(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    path = checklist_path_from_args(workspace, args.file)
    print(path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and update workspace task checklist documents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--workspace", default=".", help="Workspace root. Defaults to the current directory.")
    common.add_argument("--file", help="Checklist file path. Defaults to the current checklist in docs/task/.")

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--workspace", default=".", help="Workspace root. Defaults to the current directory.")
    init_parser.add_argument("--title", required=True, help="Task title.")
    init_parser.add_argument("--item", action="append", dest="items", help="Checklist item. Repeat for multiple items.")
    init_parser.add_argument("--note", help="Initial progress note.")
    init_parser.set_defaults(func=init_checklist)

    update_parser = subparsers.add_parser("update", parents=[common])
    update_parser.add_argument("--index", required=True, type=int, help="1-based checklist item index.")
    update_parser.add_argument("--status", required=True, choices=STATUS_CHOICES, help="New item status.")
    update_parser.add_argument("--note", help="Progress note to append.")
    update_parser.set_defaults(func=update_item)

    add_parser = subparsers.add_parser("add", parents=[common])
    add_parser.add_argument("--item", required=True, help="Checklist item text.")
    add_parser.add_argument("--status", default="pending", choices=STATUS_CHOICES, help="Initial item status.")
    add_parser.add_argument("--note", help="Progress note to append.")
    add_parser.set_defaults(func=add_item)

    log_parser = subparsers.add_parser("log", parents=[common])
    log_parser.add_argument("--note", required=True, help="Progress note to append.")
    log_parser.set_defaults(func=append_note)

    files_parser = subparsers.add_parser("files", parents=[common])
    files_parser.add_argument("--path", action="append", dest="paths", required=True, help="Modified file path. Repeat for multiple files.")
    files_parser.add_argument("--note", help="Optional note stored next to each path.")
    files_parser.add_argument("--log-note", help="Optional progress note to append.")
    files_parser.set_defaults(func=record_modified_files)

    complete_parser = subparsers.add_parser("complete", parents=[common])
    complete_parser.add_argument("--note", help="Final result note.")
    complete_parser.set_defaults(func=complete_task)

    show_parser = subparsers.add_parser("show", parents=[common])
    show_parser.set_defaults(func=show_current)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
