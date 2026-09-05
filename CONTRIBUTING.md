# Contributing to PP Skills

## Add a skill

1. Pick an audience: `product`, `engineering`, or `shared`.
2. Read [`skills/shared/pp-skill-authoring/SKILL.md`](skills/shared/pp-skill-authoring/SKILL.md).
3. Copy the template:

   ```bash
   cp -R templates/skill skills/<audience>/<skill-name>
   ```

4. Set `name` in `SKILL.md` to the directory name.
5. Write a third-person description: what the skill does, then `Use when` plus triggers.
6. Keep `SKILL.md` lean. Move long reference material to `references/`.
7. Validate:

   ```bash
   python3 scripts/validate.py
   python3 scripts/validate.py --write-catalog
   ```

## Review a skill

Check the authoring skill checklist: description triggers, one job, portable instructions, one-level-deep links, no secrets, no dated claims.

## Naming

- Lowercase letters, digits, hyphens only
- No leading/trailing hyphen, no consecutive hyphens
- Max 64 characters
- Prefer a verb phrase: `writing-prd`, `incident-response`, not `helper` or `utils`
