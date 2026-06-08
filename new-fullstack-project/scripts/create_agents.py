from __future__ import annotations

import argparse
from pathlib import Path
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a full-stack project skeleton and AGENTS.md from the bundled standard."
    )
    parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace directory to initialize. Defaults to the current directory.",
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
    skeleton_dirs = [
        "backend",
        "backend/app",
        "backend/app/api",
        "backend/app/api/v1",
        "backend/app/api/v1/endpoints",
        "backend/app/services",
        "backend/app/repositories",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/tasks",
        "backend/app/libs",
        "backend/sql",
        "backend/docs",
        "backend/docs/iterations",
        "frontend",
        "frontend/src",
        "frontend/src/api",
        "frontend/src/components",
        "frontend/src/components/common",
        "frontend/src/views",
        "frontend/src/stores",
        "frontend/src/router",
        "docs",
        "docs/iterations",
        "docs/deployment",
        "docs/api",
    ]

    if not template_path.is_file():
        print(f"ERROR template not found: {template_path}", file=sys.stderr)
        return 1

    if not workspace.is_dir():
        print(f"ERROR workspace directory not found: {workspace}", file=sys.stderr)
        return 1

    created_dirs: list[Path] = []
    existing_dirs: list[Path] = []
    for relative_dir in skeleton_dirs:
        directory = workspace / relative_dir
        if directory.exists():
            if not directory.is_dir():
                print(f"ERROR path exists but is not a directory: {directory}", file=sys.stderr)
                return 1
            existing_dirs.append(directory)
            continue
        directory.mkdir(parents=True, exist_ok=True)
        created_dirs.append(directory)

    agents_exists = target_path.exists()
    if agents_exists and not args.force:
        print(f"SKIPPED_AGENTS existing {target_path}")
        print("Use --force only when the user explicitly asks to overwrite it.")
    else:
        content = template_path.read_text(encoding="utf-8")
        target_path.write_text(content, encoding="utf-8", newline="\n")
        action = "UPDATED_AGENTS" if agents_exists else "CREATED_AGENTS"
        print(f"{action} {target_path}")

    for directory in created_dirs:
        print(f"CREATED_DIR {directory}")
    print(f"SUMMARY created_dirs={len(created_dirs)} existing_dirs={len(existing_dirs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
