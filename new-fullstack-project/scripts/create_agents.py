from __future__ import annotations

import argparse
from pathlib import Path
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create AGENTS.md in a workspace from the bundled full-stack project standard."
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace directory where AGENTS.md should be created. Defaults to the current directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing AGENTS.md. Use only when explicitly requested.",
    )
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    template_path = skill_dir / "references" / "fullstack-project-agents-template.md"
    workspace = Path(args.workspace).resolve()
    target_path = workspace / "AGENTS.md"

    if not template_path.is_file():
        print(f"ERROR template not found: {template_path}", file=sys.stderr)
        return 1

    if not workspace.is_dir():
        print(f"ERROR workspace directory not found: {workspace}", file=sys.stderr)
        return 1

    if target_path.exists() and not args.force:
        print(f"EXISTS {target_path}")
        print("Use --force only when the user explicitly asks to overwrite it.")
        return 2

    content = template_path.read_text(encoding="utf-8")
    target_path.write_text(content, encoding="utf-8", newline="\n")
    print(f"CREATED {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
