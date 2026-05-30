#!/usr/bin/env python3
"""
init_unity_project_structure.py

Create the canonical `_Project/` directory layout under an Assets folder,
without overwriting anything that already exists.

Usage:
    python3 init_unity_project_structure.py --path /absolute/path/to/Assets
    python3 init_unity_project_structure.py --path . --root MyProject
    python3 init_unity_project_structure.py --path /abs/Assets --with-resources

Notes:
    - Idempotent. Existing folders are left untouched.
    - Does NOT create scripts, scenes, or prefabs — only directories
      plus a `.gitkeep` so they survive in source control.
    - Does NOT modify ProjectSettings or Packages.
    - `Resources/` is NOT created by default — Addressables is preferred.
      Pass `--with-resources` to opt in.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


# Canonical layout. Order matters only for nice console output.
# Resources/ is intentionally omitted from the default list.
DIRS = [
    "Art/Sprites",
    "Art/Models",
    "Art/Materials",
    "Art/Animations",
    "Art/Fonts",
    "Art/VFX",
    "Audio/BGM",
    "Audio/SFX",
    "Code/Runtime/Core",
    "Code/Runtime/Gameplay",
    "Code/Runtime/UI",
    "Code/Runtime/Systems",
    "Code/Runtime/Data",
    "Code/Runtime/Input",
    "Code/Runtime/Utils",
    "Code/Editor",
    "Code/Tests/EditMode",
    "Code/Tests/PlayMode",
    "Configs/ScriptableObjects",
    "Configs/Levels",
    "Prefabs/Characters",
    "Prefabs/Gameplay",
    "Prefabs/UI",
    "Prefabs/Effects",
    "Scenes",
    "Addressables",
    "StreamingAssets",
]

OPTIONAL_RESOURCES_DIR = "Resources"


def safe_print(msg: str) -> None:
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", "ignore").decode())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the canonical _Project/ skeleton inside a Unity Assets folder."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Absolute or relative path to the Unity project's Assets folder.",
    )
    parser.add_argument(
        "--root",
        default="_Project",
        help='Root subfolder name under Assets (default: "_Project").',
    )
    parser.add_argument(
        "--no-gitkeep",
        action="store_true",
        help="Do not create .gitkeep files in empty directories.",
    )
    parser.add_argument(
        "--with-resources",
        action="store_true",
        help=(
            "Also create a Resources/ folder. Off by default to discourage abuse — "
            "prefer Addressables for non-trivial assets."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    assets_path = Path(args.path).resolve()

    if not assets_path.exists():
        safe_print(f"ERROR: path does not exist: {assets_path}")
        return 1

    if assets_path.name != "Assets":
        safe_print(
            f"WARNING: target folder is not named 'Assets' ({assets_path.name}). "
            "Continuing, but make sure this is your Unity Assets directory."
        )

    project_root = assets_path / args.root
    project_root.mkdir(exist_ok=True)
    safe_print(f"Project root: {project_root}")

    dirs = list(DIRS)
    if args.with_resources:
        dirs.append(OPTIONAL_RESOURCES_DIR)
    else:
        safe_print(
            "Note: Resources/ omitted (default). Pass --with-resources to opt in. "
            "Prefer Addressables for non-trivial assets."
        )

    created = 0
    skipped = 0
    for rel in dirs:
        target = project_root / rel
        if target.exists():
            skipped += 1
        else:
            target.mkdir(parents=True, exist_ok=False)
            created += 1
            safe_print(f"  + {rel}")

        if not args.no_gitkeep:
            keep = target / ".gitkeep"
            if not keep.exists():
                keep.write_text("")

    safe_print("")
    safe_print(f"Done. Created {created} folders, skipped {skipped} existing.")
    safe_print("Reminder: Unity will generate .meta files on its next refresh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
