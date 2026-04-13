#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = (
    "case_id",
    "transcript_kind",
    "captured_at",
    "capture_method",
    "selected_skill",
    "rejected_skills",
    "observed_output_sections",
    "notes",
)
SECTION_FIELDS = ("heading", "content")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def format_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_cases(evals_root: Path) -> dict[str, dict[str, object]]:
    cases: dict[str, dict[str, object]] = {}
    for folder in ("positive", "boundaries"):
        for path in sorted((evals_root / folder).glob("*.json")):
            raw = load_json(path)
            if isinstance(raw, dict) and isinstance(raw.get("id"), str):
                cases[raw["id"]] = raw
    return cases


def validate_replay(
    replay: object,
    *,
    replay_path: Path,
    repo_root: Path,
    cases: dict[str, dict[str, object]],
    known_skill_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    relative_path = format_path(replay_path, repo_root)

    if not isinstance(replay, dict):
        return [f"{relative_path}: replay root must be an object"]

    for field in REQUIRED_FIELDS:
        if field not in replay:
            errors.append(f"{relative_path}: missing `{field}`")

    for field in sorted(set(replay) - set(REQUIRED_FIELDS)):
        errors.append(f"{relative_path}: unexpected field `{field}`")

    case_id = replay.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        errors.append(f"{relative_path}: `case_id` must be a non-empty string")
        return errors
    if replay_path.stem != case_id:
        errors.append(f"{relative_path}: file name must match `case_id` `{case_id}`")

    case = cases.get(case_id)
    if case is None:
        errors.append(f"{relative_path}: unknown `case_id` `{case_id}`")
        return errors

    transcript_kind = replay.get("transcript_kind")
    if transcript_kind != "replay":
        errors.append(f"{relative_path}: `transcript_kind` must be `replay`")

    captured_at = replay.get("captured_at")
    if not isinstance(captured_at, str) or not DATE_PATTERN.match(captured_at):
        errors.append(f"{relative_path}: `captured_at` must use `YYYY-MM-DD` format")

    capture_method = replay.get("capture_method")
    if not isinstance(capture_method, str) or len(capture_method.strip()) < 20:
        errors.append(f"{relative_path}: `capture_method` must be a meaningful string")

    selected_skill = replay.get("selected_skill")
    expected_skill = case.get("expected_skill")
    if not isinstance(selected_skill, str) or selected_skill not in known_skill_ids:
        errors.append(f"{relative_path}: `selected_skill` must reference a known catalog skill")
    elif selected_skill != expected_skill:
        errors.append(
            f"{relative_path}: `selected_skill` `{selected_skill}` must match case "
            f"`expected_skill` `{expected_skill}`"
        )

    rejected_skills = replay.get("rejected_skills")
    if not isinstance(rejected_skills, list):
        errors.append(f"{relative_path}: `rejected_skills` must be a list")
    else:
        seen_rejected: set[str] = set()
        for skill_id in rejected_skills:
            if not isinstance(skill_id, str) or not skill_id:
                errors.append(f"{relative_path}: `rejected_skills` entries must be non-empty strings")
                continue
            if skill_id not in known_skill_ids:
                errors.append(f"{relative_path}: unknown rejected skill `{skill_id}`")
            if skill_id == selected_skill:
                errors.append(f"{relative_path}: `rejected_skills` cannot contain `selected_skill`")
            if skill_id in seen_rejected:
                errors.append(f"{relative_path}: duplicate rejected skill `{skill_id}`")
            seen_rejected.add(skill_id)

        forbidden = case.get("forbidden_skills", [])
        if isinstance(forbidden, list):
            for skill_id in forbidden:
                if isinstance(skill_id, str) and skill_id not in seen_rejected:
                    errors.append(
                        f"{relative_path}: forbidden skill `{skill_id}` must appear in `rejected_skills`"
                    )

    observed_sections = replay.get("observed_output_sections")
    expected_sections = case.get("expected_output_sections")
    if not isinstance(observed_sections, list) or not observed_sections:
        errors.append(f"{relative_path}: `observed_output_sections` must be a non-empty list")
    elif not isinstance(expected_sections, list):
        errors.append(f"{relative_path}: source case has invalid `expected_output_sections`")
    else:
        if len(observed_sections) != len(expected_sections):
            errors.append(
                f"{relative_path}: expected {len(expected_sections)} observed sections, "
                f"found {len(observed_sections)}"
            )

        for index, section in enumerate(observed_sections):
            context = f"{relative_path}: observed_output_sections[{index}]"
            if not isinstance(section, dict):
                errors.append(f"{context}: section must be an object")
                continue

            for field in SECTION_FIELDS:
                if field not in section:
                    errors.append(f"{context}: missing `{field}`")
            for field in sorted(set(section) - set(SECTION_FIELDS)):
                errors.append(f"{context}: unexpected field `{field}`")

            heading = section.get("heading")
            if not isinstance(heading, str) or not heading.strip():
                errors.append(f"{context}: `heading` must be a non-empty string")
            elif index < len(expected_sections) and heading != expected_sections[index]:
                errors.append(
                    f"{context}: `heading` `{heading}` must match "
                    f"`{expected_sections[index]}`"
                )

            content = section.get("content")
            if not isinstance(content, str) or len(content.strip()) < 20:
                errors.append(f"{context}: `content` must be a meaningful string")

    notes = replay.get("notes")
    if not isinstance(notes, str) or len(notes.strip()) < 20:
        errors.append(f"{relative_path}: `notes` must be a meaningful string")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate replayable routing transcript records.")
    parser.add_argument(
        "replays_root",
        nargs="?",
        default="evals/routing-replays",
        help="Path to the routing replay transcript root.",
    )
    parser.add_argument(
        "evals_root",
        nargs="?",
        default="evals/routing",
        help="Path to the routing eval fixtures root.",
    )
    parser.add_argument(
        "skills_root",
        nargs="?",
        default="skills",
        help="Path to the skills root directory.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    replays_root = Path(args.replays_root)
    evals_root = Path(args.evals_root)
    skills_root = Path(args.skills_root)

    if not replays_root.exists():
        print(f"routing replay root not found: {replays_root}", file=sys.stderr)
        return 1
    if not evals_root.exists():
        print(f"routing eval root not found: {evals_root}", file=sys.stderr)
        return 1
    if not skills_root.exists():
        print(f"skills root not found: {skills_root}", file=sys.stderr)
        return 1

    known_skill_ids = {path.name for path in skills_root.iterdir() if path.is_dir()}

    try:
        cases = load_cases(evals_root)
    except Exception as error:  # noqa: BLE001
        print(f"failed to read routing eval cases: {error}", file=sys.stderr)
        return 1

    replay_paths = sorted(path for path in replays_root.glob("*.json") if path.is_file())
    if not replay_paths:
        print(f"no routing replay transcripts found under: {replays_root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_case_ids: set[str] = set()

    for replay_path in replay_paths:
        try:
            replay = load_json(replay_path)
        except Exception as error:  # noqa: BLE001
            errors.append(f"{format_path(replay_path, repo_root)}: failed to parse JSON: {error}")
            continue

        replay_errors = validate_replay(
            replay,
            replay_path=replay_path,
            repo_root=repo_root,
            cases=cases,
            known_skill_ids=known_skill_ids,
        )
        errors.extend(replay_errors)

        if isinstance(replay, dict) and isinstance(replay.get("case_id"), str):
            case_id = replay["case_id"]
            if case_id in seen_case_ids:
                errors.append(f"duplicate routing replay transcript for `{case_id}`")
            seen_case_ids.add(case_id)

    missing_case_ids = sorted(set(cases) - seen_case_ids)
    extra_case_ids = sorted(seen_case_ids - set(cases))

    for case_id in missing_case_ids:
        errors.append(f"missing routing replay transcript for `{case_id}`")
    for case_id in extra_case_ids:
        errors.append(f"routing replay transcript `{case_id}` does not match a known case")

    if errors:
        print("routing replay validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"validated {len(replay_paths)} routing replay transcripts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
