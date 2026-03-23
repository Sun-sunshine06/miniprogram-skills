#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter start")

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("frontmatter must start with ---")

    try:
        end_index = lines[1:].index("---") + 1
    except ValueError as error:
        raise ValueError("frontmatter must end with ---") from error

    data: dict[str, str] = {}
    for line in lines[1:end_index]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.exists():
        errors.append("missing SKILL.md")
        return errors

    try:
        frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except Exception as error:  # noqa: BLE001
        errors.append(f"invalid SKILL.md frontmatter: {error}")
        return errors

    expected_name = skill_dir.name
    actual_name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if actual_name != expected_name:
        errors.append(f"frontmatter name '{actual_name}' does not match directory '{expected_name}'")

    if not description:
        errors.append("missing frontmatter description")

    if not openai_yaml.exists():
        errors.append("missing agents/openai.yaml")
    else:
        content = openai_yaml.read_text(encoding="utf-8")
        if "interface:" not in content:
            errors.append("agents/openai.yaml is missing interface block")

    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills")
    if not root.exists():
        print(f"skills root not found: {root}", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in root.iterdir() if path.is_dir())
    all_errors: list[str] = []

    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir)
        for error in errors:
            all_errors.append(f"{skill_dir.name}: {error}")

    if all_errors:
        print("skill validation failed:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"validated {len(skill_dirs)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
