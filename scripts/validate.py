#!/usr/bin/env python3
"""Validate PP Skills against the portable Agent Skills spec."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
CATALOG_PATH = SKILLS_DIR / "CATALOG.md"
AUDIENCES = ("product", "engineering", "shared")

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPAT = 500
MAX_SKILL_LINES = 500
SKIP_DIRS = {"scripts", "references", "assets", "templates", "examples"}


class SkillError(Exception):
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        raise SkillError("SKILL.md must start with YAML frontmatter (---)")
    rest = text[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    else:
        raise SkillError("frontmatter opening --- must be followed by a newline")

    match = re.search(r"\n---\s*\n", rest)
    if not match:
        raise SkillError("frontmatter is not closed with a --- line")
    raw = rest[: match.start()]
    body = rest[match.end() :]
    if not body.strip():
        raise SkillError("SKILL.md body is empty")
    return parse_simple_yaml(raw), body


def parse_simple_yaml(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith(" ") or line.startswith("\t"):
            raise SkillError(f"unexpected indented line: {line!r}")
        if ":" not in line:
            raise SkillError(f"expected key: value, got {line!r}")
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if key in {"metadata"} and value == "":
            meta, i = parse_string_map(lines, i + 1)
            data[key] = meta
            continue
        if value in {">", ">-", "|", "|-"}:
            folded, i = read_block(lines, i + 1)
            data[key] = folded
            continue
        data[key] = unquote(value)
        i += 1
    return data


def parse_string_map(lines: list[str], start: int) -> tuple[dict[str, str], int]:
    mapping: dict[str, str] = {}
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            break
        if indent != 2:
            raise SkillError(
                "metadata must be a flat map of string keys to string values "
                f"(2-space indent). Offending line: {line!r}"
            )
        stripped = line.strip()
        if ":" not in stripped:
            raise SkillError(f"metadata entry must be key: value, got {stripped!r}")
        key, _, value = stripped.partition(":")
        value = value.strip()
        if value in {"", ">", ">-", "|", "|-"} or value.startswith("{") or value.startswith("["):
            raise SkillError(
                f"metadata.{key.strip()} must be a quoted or plain string, not nested YAML"
            )
        mapping[key.strip()] = unquote(value)
        i += 1
    return mapping, i


def read_block(lines: list[str], start: int) -> tuple[str, int]:
    chunks: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if line and not line.startswith((" ", "\t")):
            break
        chunks.append(line[2:] if line.startswith("  ") else line)
        i += 1
    text = "\n".join(chunks).strip()
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
    return text, i


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def discover_skills() -> list[Path]:
    found: list[Path] = []
    for audience_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        if audience_dir.name.startswith("."):
            continue
        for skill_dir in sorted(p for p in audience_dir.iterdir() if p.is_dir()):
            if skill_dir.name in SKIP_DIRS or skill_dir.name.startswith("."):
                continue
            found.append(skill_dir)
    return found


def validate_skill(skill_dir: Path) -> dict[str, str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise SkillError(f"missing SKILL.md in {skill_dir.relative_to(ROOT)}")

    audience = skill_dir.parent.name
    if audience not in AUDIENCES:
        raise SkillError(f"unknown audience directory {audience!r}; expected one of {AUDIENCES}")

    text = skill_md.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise SkillError("SKILL.md has a UTF-8 BOM; save without BOM")

    data, body = parse_frontmatter(text)
    name = data.get("name")
    description = data.get("description")
    if not isinstance(name, str) or not name:
        raise SkillError("frontmatter.name is required")
    if not isinstance(description, str) or not description:
        raise SkillError("frontmatter.description is required")
    if not NAME_RE.match(name) or len(name) > MAX_NAME:
        raise SkillError(
            f"name {name!r} must be 1-{MAX_NAME} chars, lowercase alphanumerics and single hyphens"
        )
    if name != skill_dir.name:
        raise SkillError(f"name {name!r} must match directory name {skill_dir.name!r}")
    if len(description) > MAX_DESCRIPTION:
        raise SkillError(f"description is {len(description)} chars; max is {MAX_DESCRIPTION}")
    if "use when" not in description.lower():
        raise SkillError("description must include 'Use when' plus trigger terms")

    compatibility = data.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not (1 <= len(compatibility) <= MAX_COMPAT):
            raise SkillError(f"compatibility must be a string of 1-{MAX_COMPAT} chars")

    metadata = data.get("metadata", {})
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise SkillError("metadata must be a string-to-string map")
    for key, value in metadata.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise SkillError("metadata keys and values must be strings")

    meta_audience = metadata.get("audience")
    if meta_audience and meta_audience != audience:
        raise SkillError(
            f"metadata.audience {meta_audience!r} does not match path audience {audience!r}"
        )

    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    if line_count > MAX_SKILL_LINES:
        raise SkillError(f"SKILL.md is {line_count} lines; keep it under {MAX_SKILL_LINES}")

    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", body):
        href = match.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = (skill_dir / href).resolve()
        try:
            target.relative_to(skill_dir.resolve())
        except ValueError as exc:
            raise SkillError(f"link escapes skill directory: {href}") from exc
        if not target.exists():
            raise SkillError(f"broken relative link: {href}")
        rel = target.relative_to(skill_dir.resolve())
        if len(rel.parts) > 2:
            raise SkillError(f"link is nested more than one level: {href}")

    return {
        "name": name,
        "audience": audience,
        "description": description,
        "path": str(skill_dir.relative_to(ROOT)),
    }


def write_catalog(skills: list[dict[str, str]]) -> None:
    lines = [
        "# Catalog",
        "",
        "Generated by `python3 scripts/validate.py --write-catalog`. Do not edit by hand.",
        "",
        "| Skill | Audience | Description |",
        "| --- | --- | --- |",
    ]
    for skill in sorted(skills, key=lambda s: (s["audience"], s["name"])):
        desc = skill["description"].replace("|", "\\|")
        link = f"[{skill['name']}]({skill['audience']}/{skill['name']}/SKILL.md)"
        lines.append(f"| {link} | {skill['audience']} | {desc} |")
    lines.append("")
    CATALOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-catalog",
        action="store_true",
        help=f"rewrite {CATALOG_PATH.relative_to(ROOT)} from valid skills",
    )
    args = parser.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"missing {SKILLS_DIR}", file=sys.stderr)
        return 1

    errors = 0
    records: list[dict[str, str]] = []
    for skill_dir in discover_skills():
        rel = skill_dir.relative_to(ROOT)
        try:
            records.append(validate_skill(skill_dir))
            print(f"ok  {rel}")
        except SkillError as exc:
            errors += 1
            print(f"err {rel}: {exc}", file=sys.stderr)

    if errors:
        print(f"{errors} skill(s) failed", file=sys.stderr)
        return 1

    if args.write_catalog:
        write_catalog(records)
        print(f"wrote {CATALOG_PATH.relative_to(ROOT)}")

    print(f"{len(records)} skill(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
