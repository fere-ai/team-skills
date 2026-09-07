# Team Skills — agent instructions

This repository is **Team Skills**: a catalog of portable Agent Skills for product and engineering teams, by Pranav Prakash.

Skills are the product. Do not treat this like an application repo.

## Where skills live

Canonical path: `skills/<audience>/<skill-name>/SKILL.md`

| Audience | Path | Use for |
| --- | --- | --- |
| product | `skills/product/` | discovery, PRDs, specs, prioritization, launches, research |
| engineering | `skills/engineering/` | RFCs, reviews, incidents, testing, architecture, delivery |
| shared | `skills/shared/` | authoring and workflows both teams share |

Do **not** author skills in `.cursor/skills/`, `.claude/skills/`, or `.agents/skills/`. Those are install targets, not the source of truth.

## Before you add or edit a skill

1. Read `skills/shared/team-skill-authoring/SKILL.md`.
2. Copy `templates/skill/` to `skills/<audience>/<skill-name>/`.
3. Directory name must equal the `name` field (lowercase, digits, hyphens).
4. Run `python3 scripts/validate.py` before you finish.

## Rules

- One skill, one job. Split rather than pile on.
- Description: capability first, then `Use when` plus trigger terms. Third person.
- `SKILL.md` under 500 lines. Put detail in `references/`, `scripts/`, or `assets/`.
- Link supporting files one level deep from `SKILL.md`.
- Write for any Agent Skills client (Cursor, Claude Code, Hermes, others). Avoid harness-only commands unless the skill is explicitly about that harness.
- No secrets, no live credentials, no time-sensitive "as of <date>" claims.

## Validation

```bash
python3 scripts/validate.py
python3 scripts/validate.py --write-catalog
```
