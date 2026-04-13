#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def expect_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing expected file: {path}")


def expect_absent(path: Path, errors: list[str]) -> None:
    if path.exists():
        errors.append(f"expected path to be absent: {path}")


def validate_scaffold_fixture(root: Path) -> list[str]:
    errors: list[str] = []
    project_config_path = root / "project.config.json"
    app_json_path = root / "app.json"

    expect_file(project_config_path, errors)
    expect_file(app_json_path, errors)
    if errors:
        return errors

    project_config = load_json(project_config_path)
    app_json = load_json(app_json_path)

    if not isinstance(project_config, dict) or project_config.get("miniprogramRoot") != ".":
        errors.append("scaffold fixture: expected `project.config.json.miniprogramRoot` to be `.`")

    pages = app_json.get("pages") if isinstance(app_json, dict) else None
    if not isinstance(pages, list) or "pages/missing/index" not in pages:
        errors.append("scaffold fixture: expected `app.json.pages` to include `pages/missing/index`")

    for suffix in (".js", ".json", ".wxml", ".wxss"):
        expect_file(root / "pages" / "home" / f"index{suffix}", errors)

    for suffix in (".js", ".json", ".wxml"):
        expect_file(root / "pages" / "missing" / f"index{suffix}", errors)
    expect_absent(root / "pages" / "missing" / "index.wxss", errors)

    return errors


def validate_recovery_fixture(root: Path) -> list[str]:
    errors: list[str] = []
    project_config_path = root / "project.config.json"
    private_config_path = root / "project.private.config.json"
    app_json_path = root / "miniprogram" / "app.json"

    expect_file(project_config_path, errors)
    expect_file(private_config_path, errors)
    expect_file(app_json_path, errors)
    if errors:
        return errors

    project_config = load_json(project_config_path)
    private_config = load_json(private_config_path)
    app_json = load_json(app_json_path)

    if not isinstance(project_config, dict) or project_config.get("miniprogramRoot") != "miniprogram":
        errors.append(
            "recovery fixture: expected `project.config.json.miniprogramRoot` to be `miniprogram`"
        )

    pages = app_json.get("pages") if isinstance(app_json, dict) else None
    if not isinstance(pages, list) or "pages/home/index" not in pages:
        errors.append("recovery fixture: expected `miniprogram/app.json.pages` to include `pages/home/index`")

    for suffix in (".js", ".json", ".wxml", ".wxss"):
        expect_file(root / "miniprogram" / "pages" / "home" / f"index{suffix}", errors)
        expect_file(root / "pages" / "index" / f"index{suffix}", errors)

    path_name = None
    if isinstance(private_config, dict):
        condition = private_config.get("condition")
        if isinstance(condition, dict):
            mini = condition.get("miniprogram")
            if isinstance(mini, dict):
                entries = mini.get("list")
                if isinstance(entries, list) and entries:
                    first = entries[0]
                    if isinstance(first, dict):
                        path_name = first.get("pathName")
    if path_name != "pages/index/index":
        errors.append(
            "recovery fixture: expected `project.private.config.json` to carry a stale compile condition for `pages/index/index`"
        )

    return errors


def validate_gui_session_sample(sample_path: Path) -> list[str]:
    errors: list[str] = []
    expect_file(sample_path, errors)
    if errors:
        return errors

    sample = load_json(sample_path)
    if not isinstance(sample, dict):
        return ["gui session sample: root must be an object"]

    if sample.get("ok") is not False:
        errors.append("gui session sample: expected `ok` to be `false`")
    if sample.get("classification") != "devtools_session_error":
        errors.append("gui session sample: expected `classification` to be `devtools_session_error`")
    error_message = sample.get("error")
    if not isinstance(error_message, str) or "did not become ready" not in error_message:
        errors.append(
            "gui session sample: expected `error` to mention a DevTools readiness/session failure"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate committed negative-path skill fixtures.")
    parser.add_argument(
        "fixtures_root",
        nargs="?",
        default="evals/negative-fixtures",
        help="Path to the negative fixture root.",
    )
    parser.add_argument(
        "gui_session_sample",
        nargs="?",
        default="tools/wechat-gui-check/examples/sample.session-error.json",
        help="Path to the GUI session failure sample JSON file.",
    )
    args = parser.parse_args()

    fixtures_root = Path(args.fixtures_root)
    gui_session_sample = Path(args.gui_session_sample)

    if not fixtures_root.exists():
        print(f"negative fixture root not found: {fixtures_root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors.extend(validate_scaffold_fixture(fixtures_root / "scaffold-missing-page-style"))
    errors.extend(validate_recovery_fixture(fixtures_root / "recovery-wrong-root-residue"))
    errors.extend(validate_gui_session_sample(gui_session_sample))

    if errors:
        print("negative fixture validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("validated 3 negative-path fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
