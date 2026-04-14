#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED_STATUS = {"public-draft", "public-beta-tool"}
ALLOWED_READINESS = {"low", "medium", "high"}
ALLOWED_SURFACES = {"scaffold", "recovery", "cli", "gui", "architecture", "workflow", "copy"}
ALLOWED_REPO_ACTIONS = {
    "review-only",
    "restore-and-clean",
    "safe-repo-fix",
    "runtime-smoke-check",
    "navigation-restructure",
    "interaction-flow-refine",
    "ui-copy-simplify",
}
REQUIRED_REQUIRES_FIELDS = (
    "wechat_devtools_installation",
    "official_cli",
    "gui_automation",
    "user_supplied_miniprogram_automator",
)
REQUIRED_EVIDENCE_FIELDS = (
    "validation_log",
    "routing_fixture",
    "external_forward_test",
    "collaborator_host_test",
)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def format_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def validate_bool_block(
    block: object,
    *,
    required_fields: tuple[str, ...],
    context: str,
) -> list[str]:
    errors: list[str] = []

    if not isinstance(block, dict):
        return [f"{context}: expected an object"]

    extra_keys = sorted(set(block) - set(required_fields))
    missing_keys = [field for field in required_fields if field not in block]

    for field in missing_keys:
        errors.append(f"{context}: missing `{field}`")

    for field in extra_keys:
        errors.append(f"{context}: unexpected field `{field}`")

    for field in required_fields:
        if field not in block:
            continue
        if not isinstance(block[field], bool):
            errors.append(f"{context}: `{field}` must be a boolean")

    return errors


def validate_entry(entry: object, known_skill_ids: set[str], index: int) -> list[str]:
    context = f"skills[{index}]"
    errors: list[str] = []

    if not isinstance(entry, dict):
        return [f"{context}: expected an object"]

    required_fields = {
        "id",
        "status",
        "public_readiness",
        "surface",
        "repo_action",
        "requires",
        "evidence",
        "routing_priority_over",
    }

    for field in sorted(required_fields - set(entry)):
        errors.append(f"{context}: missing `{field}`")

    for field in sorted(set(entry) - required_fields):
        errors.append(f"{context}: unexpected field `{field}`")

    skill_id = entry.get("id")
    if not isinstance(skill_id, str) or not skill_id:
        errors.append(f"{context}: `id` must be a non-empty string")
    elif skill_id not in known_skill_ids:
        errors.append(f"{context}: `id` `{skill_id}` does not match a directory under skills/")

    status = entry.get("status")
    if status not in ALLOWED_STATUS:
        errors.append(f"{context}: `status` must be one of {sorted(ALLOWED_STATUS)}")

    readiness = entry.get("public_readiness")
    if readiness not in ALLOWED_READINESS:
        errors.append(f"{context}: `public_readiness` must be one of {sorted(ALLOWED_READINESS)}")

    surface = entry.get("surface")
    if surface not in ALLOWED_SURFACES:
        errors.append(f"{context}: `surface` must be one of {sorted(ALLOWED_SURFACES)}")

    repo_action = entry.get("repo_action")
    if repo_action not in ALLOWED_REPO_ACTIONS:
        errors.append(f"{context}: `repo_action` must be one of {sorted(ALLOWED_REPO_ACTIONS)}")

    requires = entry.get("requires")
    errors.extend(
        validate_bool_block(
            requires,
            required_fields=REQUIRED_REQUIRES_FIELDS,
            context=f"{context}.requires",
        )
    )

    evidence = entry.get("evidence")
    errors.extend(
        validate_bool_block(
            evidence,
            required_fields=REQUIRED_EVIDENCE_FIELDS,
            context=f"{context}.evidence",
        )
    )

    routing_priority_over = entry.get("routing_priority_over")
    if not isinstance(routing_priority_over, list):
        errors.append(f"{context}: `routing_priority_over` must be a list")
    else:
        seen_neighbors: set[str] = set()
        for neighbor in routing_priority_over:
            if not isinstance(neighbor, str) or not neighbor:
                errors.append(f"{context}: `routing_priority_over` entries must be non-empty strings")
                continue
            if neighbor == skill_id:
                errors.append(f"{context}: `routing_priority_over` cannot reference its own skill id")
            if neighbor not in known_skill_ids:
                errors.append(f"{context}: unknown `routing_priority_over` skill `{neighbor}`")
            if neighbor in seen_neighbors:
                errors.append(f"{context}: duplicate `routing_priority_over` skill `{neighbor}`")
            seen_neighbors.add(neighbor)

    if isinstance(requires, dict):
        if requires.get("official_cli") and not requires.get("wechat_devtools_installation"):
            errors.append(
                f"{context}: `requires.official_cli` implies `requires.wechat_devtools_installation`"
            )
        if requires.get("gui_automation") and not requires.get("wechat_devtools_installation"):
            errors.append(
                f"{context}: `requires.gui_automation` implies `requires.wechat_devtools_installation`"
            )
        if requires.get("user_supplied_miniprogram_automator") and not requires.get("gui_automation"):
            errors.append(
                f"{context}: `requires.user_supplied_miniprogram_automator` implies `requires.gui_automation`"
            )

        if surface == "cli" and not requires.get("official_cli"):
            errors.append(f"{context}: `surface` `cli` requires `requires.official_cli = true`")
        if surface == "gui" and not requires.get("gui_automation"):
            errors.append(f"{context}: `surface` `gui` requires `requires.gui_automation = true`")

    if surface == "gui" and repo_action != "runtime-smoke-check":
        errors.append(f"{context}: `surface` `gui` must use `repo_action` `runtime-smoke-check`")
    if surface == "scaffold" and repo_action != "review-only":
        errors.append(f"{context}: `surface` `scaffold` must use `repo_action` `review-only`")
    if surface == "recovery" and repo_action != "restore-and-clean":
        errors.append(f"{context}: `surface` `recovery` must use `repo_action` `restore-and-clean`")
    if surface == "cli" and repo_action != "safe-repo-fix":
        errors.append(f"{context}: `surface` `cli` must use `repo_action` `safe-repo-fix`")
    if surface == "architecture" and repo_action != "navigation-restructure":
        errors.append(f"{context}: `surface` `architecture` must use `repo_action` `navigation-restructure`")
    if surface == "workflow" and repo_action != "interaction-flow-refine":
        errors.append(f"{context}: `surface` `workflow` must use `repo_action` `interaction-flow-refine`")
    if surface == "copy" and repo_action != "ui-copy-simplify":
        errors.append(f"{context}: `surface` `copy` must use `repo_action` `ui-copy-simplify`")

    if status == "public-beta-tool" and surface != "gui":
        errors.append(f"{context}: `public-beta-tool` status is only expected on the GUI tool surface")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the machine-readable public skill catalog.")
    parser.add_argument(
        "catalog",
        nargs="?",
        default="manifests/skill-catalog.json",
        help="Path to the skill catalog JSON file.",
    )
    parser.add_argument(
        "skills_root",
        nargs="?",
        default="skills",
        help="Path to the skills root directory.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    catalog_path = Path(args.catalog)
    skills_root = Path(args.skills_root)

    if not catalog_path.exists():
        print(f"skill catalog not found: {catalog_path}", file=sys.stderr)
        return 1

    if not skills_root.exists():
        print(f"skills root not found: {skills_root}", file=sys.stderr)
        return 1

    known_skill_ids = {path.name for path in skills_root.iterdir() if path.is_dir()}

    try:
        raw_catalog = load_json(catalog_path)
    except Exception as error:  # noqa: BLE001
        print(f"failed to read skill catalog: {error}", file=sys.stderr)
        return 1

    errors: list[str] = []

    if not isinstance(raw_catalog, dict):
        errors.append("catalog root must be an object")
    else:
        version = raw_catalog.get("version")
        if version != 1:
            errors.append("catalog `version` must be `1`")

        skills = raw_catalog.get("skills")
        if not isinstance(skills, list) or not skills:
            errors.append("catalog `skills` must be a non-empty list")
            skills = []

        seen_skill_ids: set[str] = set()
        for index, entry in enumerate(skills):
            entry_errors = validate_entry(entry, known_skill_ids, index)
            errors.extend(entry_errors)

            if isinstance(entry, dict):
                skill_id = entry.get("id")
                if isinstance(skill_id, str) and skill_id:
                    if skill_id in seen_skill_ids:
                        errors.append(f"duplicate skill id in catalog: `{skill_id}`")
                    seen_skill_ids.add(skill_id)

        missing_from_catalog = sorted(known_skill_ids - seen_skill_ids)
        extra_in_catalog = sorted(seen_skill_ids - known_skill_ids)

        for skill_id in missing_from_catalog:
            errors.append(f"skill directory `{skill_id}` is missing from the catalog")
        for skill_id in extra_in_catalog:
            errors.append(f"catalog entry `{skill_id}` does not have a matching skill directory")

    if errors:
        print("skill catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "validated "
        f"{len(known_skill_ids)} cataloged skills from {format_path(catalog_path, repo_root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
