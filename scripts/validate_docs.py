#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

IGNORED_PARTS = {".git", ".tmp", "node_modules"}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")
EXTERNAL_TARGET_PREFIXES = ("http://", "https://", "mailto:")


def should_skip(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if not should_skip(path))


def format_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()

    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()

    # Titles such as `(./foo.md "Title")` are not used in this repository,
    # but trimming them keeps the validator resilient if they appear later.
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]

    return target


def resolve_local_target(markdown_path: Path, target: str) -> Path | None:
    normalized = normalize_target(target)

    if not normalized or normalized.startswith("#"):
        return None

    lowered = normalized.lower()
    if lowered.startswith(EXTERNAL_TARGET_PREFIXES):
        return None

    path_only = normalized.split("#", 1)[0]
    if not path_only:
        return None

    return (markdown_path.parent / path_only).resolve(strict=False)


def extract_local_targets(markdown_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    resolved_targets: list[str] = []
    in_code_fence = False

    for line_number, line in enumerate(markdown_path.read_text(encoding="utf-8").splitlines(), start=1):
        if CODE_FENCE_RE.match(line):
            in_code_fence = not in_code_fence
            continue

        if in_code_fence:
            continue

        for raw_target in MARKDOWN_LINK_RE.findall(line):
            resolved = resolve_local_target(markdown_path, raw_target)
            if resolved is None:
                continue

            resolved_targets.append(str(resolved))
            if not resolved.exists():
                errors.append(
                    f"{line_number}: link target `{normalize_target(raw_target)}` does not exist"
                )

    return errors, resolved_targets


def find_counterpart(markdown_path: Path) -> Path | None:
    if markdown_path.name.endswith(".zh-CN.md"):
        counterpart = markdown_path.with_name(markdown_path.name.replace(".zh-CN.md", ".md"))
        return counterpart if counterpart.exists() else None

    zh_counterpart = markdown_path.with_name(markdown_path.stem + ".zh-CN.md")
    return zh_counterpart if zh_counterpart.exists() else None


def validate_markdown_file(markdown_path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    line_errors, resolved_targets = extract_local_targets(markdown_path)
    relative_path = format_path(markdown_path, root)

    for error in line_errors:
        errors.append(f"{relative_path}:{error}")

    counterpart = find_counterpart(markdown_path)
    if counterpart is not None and str(counterpart.resolve(strict=False)) not in resolved_targets:
        errors.append(
            f"{relative_path}: missing local language-switch link to `{format_path(counterpart, root)}`"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate repository markdown links and bilingual document cross-links."
    )
    parser.add_argument("root", nargs="?", default=".", help="Path to the repository root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"repository root not found: {root}", file=sys.stderr)
        return 1

    markdown_files = iter_markdown_files(root)
    all_errors: list[str] = []

    for markdown_path in markdown_files:
        all_errors.extend(validate_markdown_file(markdown_path, root))

    if all_errors:
        print("docs validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"validated {len(markdown_files)} markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
