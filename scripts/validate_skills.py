#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SKILL_SECTIONS = (
    "Overview",
    "Quick Start",
    "Core Rules",
    "Output Format",
)

REQUIRED_INTERFACE_FIELDS = (
    "display_name",
    "short_description",
    "default_prompt",
)

PLACEHOLDER_DESCRIPTIONS = {
    "todo",
    "tbd",
    "coming soon",
    "description",
    "placeholder",
}


def split_frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter start")

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("frontmatter must start with ---")

    try:
        end_index = lines[1:].index("---") + 1
    except ValueError as error:
        raise ValueError("frontmatter must end with ---") from error

    return lines[1:end_index], "\n".join(lines[end_index + 1 :])


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    frontmatter_lines, body = split_frontmatter(text)

    data: dict[str, str] = {}
    for line in frontmatter_lines:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body


def parse_markdown_sections(body: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE)}


def has_meaningful_description(description: str) -> bool:
    normalized = description.strip().strip("\"'")
    if len(normalized) < 20:
        return False
    return normalized.lower() not in PLACEHOLDER_DESCRIPTIONS


def parse_interface_block(text: str) -> dict[str, str]:
    lines = text.splitlines()
    interface_index: int | None = None

    for index, line in enumerate(lines):
        if line.strip() == "interface:":
            interface_index = index
            break

    if interface_index is None:
        raise ValueError("missing top-level `interface:` block")

    fields: dict[str, str] = {}
    for line in lines[interface_index + 1 :]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith("  "):
            break
        match = re.match(r"^\s{2,}([A-Za-z0-9_]+):\s*(.*)\s*$", line)
        if not match:
            raise ValueError(f"invalid `interface` line: {line}")
        key = match.group(1)
        value = match.group(2).strip().strip("\"'")
        fields[key] = value

    return fields


def format_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def validate_skill(skill_dir: Path, *, require_example_prompts: bool = False) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    references_dir = skill_dir / "references"
    example_prompts = references_dir / "example-prompts.md"

    if not skill_md.exists():
        errors.append("missing SKILL.md")
        return errors

    skill_text = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter, body = parse_frontmatter(skill_text)
    except Exception as error:  # noqa: BLE001
        errors.append(f"invalid SKILL.md frontmatter: {error}")
        return errors

    expected_name = skill_dir.name
    actual_name = frontmatter.get("name", "").strip().strip("\"'")
    description = frontmatter.get("description", "")

    if actual_name != expected_name:
        errors.append(
            f"{format_path(skill_md, skill_dir)}: frontmatter `name` is '{actual_name}' but directory name is '{expected_name}'"
        )

    if not description.strip():
        errors.append(f"{format_path(skill_md, skill_dir)}: missing frontmatter `description`")
    elif not has_meaningful_description(description):
        errors.append(
            f"{format_path(skill_md, skill_dir)}: frontmatter `description` must be specific enough for reviewers to understand the skill"
        )

    sections = parse_markdown_sections(body)
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in sections:
            errors.append(f"{format_path(skill_md, skill_dir)}: missing required section `## {section}`")

    if not references_dir.exists():
        errors.append(f"{format_path(references_dir, skill_dir)}: missing references directory")
    elif not any(references_dir.iterdir()):
        errors.append(f"{format_path(references_dir, skill_dir)}: references directory is empty")

    if require_example_prompts and not example_prompts.exists():
        errors.append(
            f"{format_path(example_prompts, skill_dir)}: missing required example prompts file (enable once M1 is adopted)"
        )

    if not openai_yaml.exists():
        errors.append(f"{format_path(openai_yaml, skill_dir)}: missing agents/openai.yaml")
    else:
        content = openai_yaml.read_text(encoding="utf-8")
        try:
            interface_fields = parse_interface_block(content)
        except Exception as error:  # noqa: BLE001
            errors.append(f"{format_path(openai_yaml, skill_dir)}: {error}")
        else:
            for field in REQUIRED_INTERFACE_FIELDS:
                if not interface_fields.get(field):
                    errors.append(
                        f"{format_path(openai_yaml, skill_dir)}: missing required `interface.{field}` value"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate public skill structure and metadata.")
    parser.add_argument("root", nargs="?", default="skills", help="Path to the skills root directory.")
    parser.add_argument(
        "--require-example-prompts",
        action="store_true",
        help="Fail if references/example-prompts.md is missing for any skill.",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"skills root not found: {root}", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in root.iterdir() if path.is_dir())
    all_errors: list[str] = []

    for skill_dir in skill_dirs:
        errors = validate_skill(skill_dir, require_example_prompts=args.require_example_prompts)
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
