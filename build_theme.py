#!/usr/bin/env python3
"""
build_theme.py — validate and package the Surprising Watermelon RemNote theme.

This repo uses a single variable-driven `theme.css` for both light and dark mode.
The old concatenate-light-and-dark workflow was intentionally retired because it
can create selector leakage between modes.

Usage:
  python build_theme.py             # validate only
  python build_theme.py --package   # validate, then create remnote-watermelon-theme.zip
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
THEME = ROOT / "theme.css"
MANIFEST = ROOT / "manifest.json"
PACKAGE_NAME = "remnote-watermelon-theme.zip"
TOP_LEVEL_FOLDER = "remnote-watermelon-theme"

REQUIRED_FILES = [
    "manifest.json",
    "theme.css",
    "README.md",
    "LICENSE",
    "PACKAGING.md",
    "AGENTS.md",
]

FORBIDDEN_PATTERNS = {
    r"--swl": "Old light-only --swl variables should not appear in combined theme.css.",
    r"body\s+\.dark\s+div#hierarchy-editor": "Use .dark div#hierarchy-editor, not body .dark div#hierarchy-editor.",
    r":is\([^)]*\.dark\s+(?:b|i|strong|em|\.bold|\.italic|\.underline|\.code|\.inline-code|\.rn-code|\.rn-highlight-reference)": "Do not put .dark-prefixed selectors inside :is(...). Scope the outer selector instead.",
    r"\.light\s+\.dark\\:bg-black\s*,\s*\.dark\\:bg-black": "Do not include a global .dark\\:bg-black light-mode selector.",
}

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".vscode",
    ".idea",
    "dist",
    "build",
    ".tmp",
}

EXCLUDE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".swp",
    ".swo",
}

EXCLUDE_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    PACKAGE_NAME,
    "PluginZip.zip",
}


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def brace_balance_ok(css: str) -> bool:
    stripped = strip_comments(css)
    balance = 0
    for char in stripped:
        if char == "{":
            balance += 1
        elif char == "}":
            balance -= 1
            if balance < 0:
                return False
    return balance == 0


def css_variables_defined(css: str) -> set[str]:
    return set(re.findall(r"--[A-Za-z0-9_-]+\s*:", css))


def css_variables_used(css: str) -> set[str]:
    return set(re.findall(r"var\(\s*(--[A-Za-z0-9_-]+)", css))


def normalize_defined(definitions: set[str]) -> set[str]:
    return {item[:-1].strip() for item in definitions}


def validate_manifest() -> list[str]:
    errors: list[str] = []
    if not MANIFEST.exists():
        return ["Missing manifest.json"]

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"manifest.json is invalid JSON: {exc}"]

    required_keys = [
        "manifestVersion",
        "id",
        "name",
        "author",
        "version",
        "theme",
        "description",
        "requestNative",
        "requiredScopes",
        "enableOnMobile",
    ]
    for key in required_keys:
        if key not in manifest:
            errors.append(f"manifest.json missing required key: {key}")

    if manifest.get("theme") != ["light", "dark"]:
        errors.append('manifest.json should contain "theme": ["light", "dark"]')

    if manifest.get("requestNative") is not False:
        errors.append("manifest.json should keep requestNative=false for this CSS-only theme")

    if manifest.get("requiredScopes") != []:
        errors.append("manifest.json should keep requiredScopes=[] for this CSS-only theme")

    version = manifest.get("version")
    if not isinstance(version, dict) or not all(k in version for k in ("major", "minor", "patch")):
        errors.append("manifest.json version should contain major, minor, and patch")

    return errors


def validate_theme_css() -> list[str]:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    if not THEME.exists():
        return errors

    css = THEME.read_text(encoding="utf-8")

    if not brace_balance_ok(css):
        errors.append("theme.css braces are unbalanced")

    defined = normalize_defined(css_variables_defined(css))
    used = css_variables_used(css)
    undefined = sorted(used - defined)
    if undefined:
        errors.append("Undefined CSS variables: " + ", ".join(undefined))

    for pattern, message in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, css, flags=re.S):
            errors.append(message)

    if ":root" not in css or ".dark" not in css:
        errors.append("theme.css should contain both default/light tokens and .dark token overrides")

    return errors


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = set(rel.parts)

    if parts & EXCLUDE_DIRS:
        return False
    if path.name in EXCLUDE_NAMES:
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    if path.suffix == ".zip":
        return False
    return path.is_file()


def iter_package_files() -> Iterable[Path]:
    for path in sorted(ROOT.rglob("*")):
        if should_include(path):
            yield path


def create_package() -> Path:
    out = ROOT / PACKAGE_NAME
    if out.exists():
        out.unlink()

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in iter_package_files():
            rel = path.relative_to(ROOT)
            arcname = Path(TOP_LEVEL_FOLDER) / rel
            zf.write(path, arcname.as_posix())

    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and package the RemNote theme.")
    parser.add_argument("--package", action="store_true", help="Create remnote-watermelon-theme.zip after validation.")
    args = parser.parse_args()

    errors = []
    errors.extend(validate_manifest())
    errors.extend(validate_theme_css())

    if errors:
        print("Theme validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    css = THEME.read_text(encoding="utf-8")
    defined = normalize_defined(css_variables_defined(css))
    used = css_variables_used(css)

    print(f"theme.css OK — {len(css.splitlines())} lines, {len(css.encode('utf-8'))} bytes")
    print(f"CSS variables: {len(defined)} defined, {len(used)} used, 0 undefined")
    print("manifest.json OK")

    if args.package:
        out = create_package()
        print(f"Package created: {out.name} ({out.stat().st_size} bytes)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
