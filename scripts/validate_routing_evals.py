#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = (
    "id",
    "kind",
    "prompt",
    "expected_skill",
    "forbidden_skills",
    "expected_output_sections",
    "source_plan",
)
ALLOWED_KINDS = {"positive", "boundary"}
FOLDER_KIND_MAP = {
    "positive": "positive",
    "boundaries": "boundary",
}


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def format_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_catalog(path: Path) -> dict[str, dict[str, object]]:
    raw = load_json(path)
    if not isinstance(raw, dict) or not isinstance(raw.get("skills"), list):
        raise ValueError("invalid catalog structure")

    catalog: dict[str, dict[str, object]] = {}
    for entry in raw["skills"]:
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            catalog[entry["id"]] = entry
    return catalog


def validate_case(
    case: object,
    *,
    case_path: Path,
    repo_root: Path,
    catalog_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    relative_path = format_path(case_path, repo_root)

    if not isinstance(case, dict):
        return [f"{relative_path}: case root must be an object"]

    for field in REQUIRED_FIELDS:
        if field not in case:
            errors.append(f"{relative_path}: missing `{field}`")

    for field in sorted(set(case) - set(REQUIRED_FIELDS)):
        errors.append(f"{relative_path}: unexpected field `{field}`")

    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id:
        errors.append(f"{relative_path}: `id` must be a non-empty string")
    elif case_path.stem != case_id:
        errors.append(f"{relative_path}: file name must match `id` `{case_id}`")

    kind = case.get("kind")
    if kind not in ALLOWED_KINDS:
        errors.append(f"{relative_path}: `kind` must be one of {sorted(ALLOWED_KINDS)}")
    else:
        expected_kind = FOLDER_KIND_MAP.get(case_path.parent.name)
        if expected_kind is None:
            errors.append(
                f"{relative_path}: parent folder must be one of {sorted(FOLDER_KIND_MAP)}"
            )
        elif expected_kind != kind:
            errors.append(
                f"{relative_path}: folder `{case_path.parent.name}` does not match `kind` `{kind}`"
            )

    prompt = case.get("prompt")
    if not isinstance(prompt, str) or len(prompt.strip()) < 20:
        errors.append(f"{relative_path}: `prompt` must be a meaningful string")

    expected_skill = case.get("expected_skill")
    if not isinstance(expected_skill, str) or expected_skill not in catalog_ids:
        errors.append(f"{relative_path}: `expected_skill` must reference a known catalog skill")

    forbidden_skills = case.get("forbidden_skills")
    if not isinstance(forbidden_skills, list):
        errors.append(f"{relative_path}: `forbidden_skills` must be a list")
    else:
        seen_forbidden: set[str] = set()
        for skill_id in forbidden_skills:
            if not isinstance(skill_id, str) or not skill_id:
                errors.append(f"{relative_path}: `forbidden_skills` entries must be non-empty strings")
                continue
            if skill_id not in catalog_ids:
                errors.append(f"{relative_path}: unknown forbidden skill `{skill_id}`")
            if skill_id == expected_skill:
                errors.append(f"{relative_path}: `forbidden_skills` cannot contain `expected_skill`")
            if skill_id in seen_forbidden:
                errors.append(f"{relative_path}: duplicate forbidden skill `{skill_id}`")
            seen_forbidden.add(skill_id)
        if kind == "boundary" and not forbidden_skills:
            errors.append(f"{relative_path}: boundary cases must declare at least one forbidden skill")

    output_sections = case.get("expected_output_sections")
    if not isinstance(output_sections, list) or not output_sections:
        errors.append(f"{relative_path}: `expected_output_sections` must be a non-empty list")
    else:
        seen_sections: set[str] = set()
        for section in output_sections:
            if not isinstance(section, str) or not section.strip():
                errors.append(
                    f"{relative_path}: `expected_output_sections` entries must be non-empty strings"
                )
                continue
            if section in seen_sections:
                errors.append(f"{relative_path}: duplicate expected output section `{section}`")
            seen_sections.add(section)

    source_plan = case.get("source_plan")
    if not isinstance(source_plan, str) or not source_plan:
        errors.append(f"{relative_path}: `source_plan` must be a non-empty string")
    else:
        source_plan_path = repo_root / source_plan
        if not source_plan_path.exists():
            errors.append(f"{relative_path}: `source_plan` target `{source_plan}` does not exist")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate replayable routing-eval prompt fixtures.")
    parser.add_argument(
        "evals_root",
        nargs="?",
        default="evals/routing",
        help="Path to the routing eval fixtures root.",
    )
    parser.add_argument(
        "catalog",
        nargs="?",
        default="manifests/skill-catalog.json",
        help="Path to the skill catalog JSON file.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    evals_root = Path(args.evals_root)
    catalog_path = Path(args.catalog)

    if not evals_root.exists():
        print(f"routing eval root not found: {evals_root}", file=sys.stderr)
        return 1

    if not catalog_path.exists():
        print(f"skill catalog not found: {catalog_path}", file=sys.stderr)
        return 1

    try:
        catalog = load_catalog(catalog_path)
    except Exception as error:  # noqa: BLE001
        print(f"failed to read skill catalog: {error}", file=sys.stderr)
        return 1

    catalog_ids = set(catalog)
    case_paths = sorted(path for path in evals_root.rglob("*.json") if path.is_file())

    if not case_paths:
        print(f"no routing eval cases found under: {evals_root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_case_ids: set[str] = set()
    positive_coverage: set[str] = set()
    boundary_pairs: set[tuple[str, str]] = set()

    for case_path in case_paths:
        try:
            case = load_json(case_path)
        except Exception as error:  # noqa: BLE001
            errors.append(f"{format_path(case_path, repo_root)}: failed to parse JSON: {error}")
            continue

        case_errors = validate_case(
            case,
            case_path=case_path,
            repo_root=repo_root,
            catalog_ids=catalog_ids,
        )
        errors.extend(case_errors)

        if not isinstance(case, dict):
            continue

        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in seen_case_ids:
                errors.append(f"duplicate routing eval case id `{case_id}`")
            seen_case_ids.add(case_id)

        expected_skill = case.get("expected_skill")
        if not isinstance(expected_skill, str) or expected_skill not in catalog_ids:
            continue

        if case.get("kind") == "positive":
            positive_coverage.add(expected_skill)

        if case.get("kind") == "boundary" and isinstance(case.get("forbidden_skills"), list):
            for forbidden in case["forbidden_skills"]:
                if isinstance(forbidden, str) and forbidden in catalog_ids:
                    boundary_pairs.add((expected_skill, forbidden))

    for skill_id in sorted(catalog_ids):
        if skill_id not in positive_coverage:
            errors.append(f"missing positive routing case for `{skill_id}`")

    for skill_id, entry in sorted(catalog.items()):
        neighbors = entry.get("routing_priority_over", [])
        if not isinstance(neighbors, list):
            errors.append(f"catalog entry `{skill_id}` has invalid `routing_priority_over` data")
            continue
        for neighbor in neighbors:
            if (skill_id, neighbor) not in boundary_pairs:
                errors.append(
                    "missing boundary routing case where "
                    f"`{skill_id}` wins over `{neighbor}`"
                )

    if errors:
        print("routing eval validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    positive_count = len(positive_coverage)
    boundary_count = sum(1 for path in case_paths if path.parent.name == "boundaries")
    print(
        "validated "
        f"{len(case_paths)} routing eval cases "
        f"({positive_count} positive coverage entries, {boundary_count} boundary prompts)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
