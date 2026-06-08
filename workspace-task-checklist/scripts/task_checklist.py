from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys


STATUS_CHOICES = ("pending", "in_progress", "completed", "blocked", "skipped")
DEFAULT_ITEMS = [
    "Confirm scope and constraints",
    "Perform the main work",
    "Validate the result",
    "Report outcome and follow-ups",
]


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
    return f"- [ ] [{status}] {clean}"


def strip_status(text: str) -> str:
    cleaned = re.sub(r"^\s*\[[A-Za-z_-]+\]\s+", "", text.strip())
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
        if line.startswith("- Updated:"):
            lines[index] = f"- Updated: {now_text()}"
            updated = True
        elif status is not None and line.startswith("- Status:"):
            lines[index] = f"- Status: {status}"
            status_updated = True

    if not updated:
        lines.insert(1, f"- Updated: {now_text()}")
    if not status_updated:
        lines.insert(1, f"- Status: {status}")
    return lines


def ensure_section(lines: list[str], heading: str) -> int:
    for index, line in enumerate(lines):
        if line.strip() == heading:
            return index
    if lines and lines[-1].strip():
        lines.append("")
    lines.append(heading)
    return len(lines) - 1


def append_log(lines: list[str], note: str | None) -> list[str]:
    if not note:
        return lines
    log_index = ensure_section(lines, "## Progress Log")
    insert_index = len(lines)
    for index in range(log_index + 1, len(lines)):
        if lines[index].startswith("## "):
            insert_index = index
            break
    lines.insert(insert_index, f"- {now_text()} - {note}")
    return lines


def checklist_line_indices(lines: list[str]) -> list[int]:
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == "## Checklist")
    except StopIteration:
        return []

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
        f"- Workspace: `{workspace}`",
        f"- Created: {timestamp}",
        f"- Updated: {timestamp}",
        "- Status: in_progress",
        "",
        "## Checklist",
    ]
    lines.extend(format_item(item) for item in checklist_items)
    lines.extend(
        [
            "",
            "## Progress Log",
            f"- {timestamp} - {note or 'Checklist created.'}",
            "",
            "## Validation",
            "- Pending.",
            "",
            "## Final Result",
            "- Pending.",
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
    checklist_index = ensure_section(lines, "## Checklist")
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


def complete_task(args: argparse.Namespace) -> int:
    workspace = workspace_path(args.workspace)
    path = checklist_path_from_args(workspace, args.file)
    lines = read_text(path).splitlines()
    lines = update_header(lines, "completed")
    lines = append_log(lines, args.note or "Task completed.")
    final_index = ensure_section(lines, "## Final Result")
    insert_index = len(lines)
    for index in range(final_index + 1, len(lines)):
        if lines[index].startswith("## "):
            insert_index = index
            break
    lines.insert(insert_index, f"- {args.note or 'Completed.'}")
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
