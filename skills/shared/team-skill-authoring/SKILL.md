---
name: team-skill-authoring
description: >-
  Authors and reviews Team Skills to the portable Agent Skills spec. Use when
  adding, editing, or reviewing a skill in this repo, or when the user mentions
  SKILL.md, scaffolding a skill, or contributing to Team Skills.
license: MIT
metadata:
  audience: shared
  author: Pranav Prakash
  version: "0.1.0"
---

# Team Skill authoring

Team Skills is a catalog of portable Agent Skills for product and engineering teams. One folder, many agents: Cursor, Claude Code, Hermes, and anything else that reads `SKILL.md`.

## Quick start

```bash
cp -R templates/skill skills/<audience>/<skill-name>
# edit skills/<audience>/<skill-name>/SKILL.md
python3 scripts/validate.py
python3 scripts/validate.py --write-catalog
```

`<audience>` is `product`, `engineering`, or `shared`. `<skill-name>` must equal the `name` field.

## Frontmatter

Required by the [Agent Skills spec](https://agentskills.io/specification):

| Field | Rules |
| --- | --- |
| `name` | 1–64 chars. `[a-z0-9-]` only. No leading, trailing, or consecutive hyphens. Must match the directory name. |
| `description` | 1–1024 chars. Third person. Capability first, then `Use when` plus trigger terms. |

Team Skills also sets:

```yaml
license: MIT
metadata:
  audience: product | engineering | shared
  author: Pranav Prakash
  version: "0.1.0"
```

`metadata` values must be strings. Optional spec fields: `compatibility` (env requirements only), `allowed-tools` (experimental).

Omit Cursor `disable-model-invocation` unless the skill should load only when named. Add Hermes-only keys (`platforms`, nested `metadata.hermes`) only when the skill is Hermes-specific.

### Description

Write two beats in one block:

1. What the skill does (front-load this; some indexes truncate around 60 characters).
2. `Use when` plus concrete triggers (file types, verbs, role names, phrases the user would say).

```yaml
# Good
description: >-
  Turns discovery notes into a one-pager PRD with problem, bets, and
  non-goals. Use when writing a PRD, product spec, or one-pager, or when
  the user asks to spec a feature.

# Bad
description: Helps with product docs.
```

No first person. No marketing words (powerful, seamless, comprehensive).

## Body

Assume the agent is already capable. Teach only the house workflow: steps, decision gates, output shape, failure modes.

Recommended section order:

1. **When to use** — one short paragraph, plus a "Don't use for" line if the skill is easy to over-apply.
2. **Workflow** — numbered steps. Each step has a checkable done condition.
3. **Output** — a template or concrete example, not an abstract outline.
4. **Pitfalls** — known failure modes.
5. **Verification** — how to prove it worked.
6. **Resources** — links one level deep (`references/foo.md`, `scripts/bar.py`).

Keep `SKILL.md` under 500 lines (target well under 200). Move detail to:

- `references/` — docs the agent reads only when needed
- `scripts/` — tiny CLIs the agent should run, not rewrite
- `assets/` — templates and static files used in output

Do not nest references (`references/a/b.md`). Do not chain "see that file which points at another file."

## Degrees of freedom

| Freedom | When | How |
| --- | --- | --- |
| High | Judgment work (reviews, coaching) | Principles and checklists |
| Medium | Preferred shape with room to adapt | Templates and examples |
| Low | Fragile, must be consistent | Scripts the agent executes |

## Portability

- Write instructions that work without a specific IDE. Name a harness only when the task is that harness.
- Use POSIX paths (`scripts/validate.py`), never backslashes.
- Prefer tools every agent has: read files, run a shell, edit files.
- If a step needs a Cursor MCP, Claude slash command, or Hermes toolset, gate it: "If `<tool>` is available, … Otherwise …"

## Naming

- Verb or job: `writing-prd`, `incident-response`, `pr-review`
- Not: `helper`, `utils`, `notes`, `misc`
- Prefix `team-` only for repo-meta skills (`team-skill-authoring`)

## Anti-patterns

- Padding `SKILL.md` with background the agent already knows
- Several unrelated jobs in one skill
- Time-stamped process ("before August 2026, use v1")
- Secrets, tokens, or private URLs
- Windows paths, optional-tool soup, or three ways to do the same step with no default

## Checklist

- [ ] Directory name equals `name`
- [ ] Description has capability + `Use when` triggers, third person
- [ ] `metadata.audience` is `product`, `engineering`, or `shared`
- [ ] Body is a procedure, not an essay
- [ ] Supporting files are one level deep and linked from `SKILL.md`
- [ ] `python3 scripts/validate.py` passes
