# Team Skills

Portable [Agent Skills](https://agentskills.io) for product and engineering teams, by Pranav Prakash.

One `SKILL.md` folder per workflow. The same skill loads in Cursor, Claude Code, Hermes, and any other agent that follows the open Agent Skills format.

## Layout

```text
skills/
  product/        # discovery, specs, launches, prioritization
  engineering/    # design docs, reviews, incidents, delivery
  shared/         # authoring and other cross-team workflows
templates/skill/  # copy this to start a new skill
scripts/          # validate + local install
```

Each skill is a directory whose name matches the `name` field in `SKILL.md`:

```text
skills/<audience>/<skill-name>/
  SKILL.md           # required: frontmatter + instructions
  scripts/           # optional: executable helpers
  references/        # optional: loaded only when needed
  assets/            # optional: templates and static files
```

See [skills/CATALOG.md](skills/CATALOG.md) for the current inventory.

## Install

Skills are authored here. Agents discover them after you install (or point) at this repo.

### Any supported agent (`npx skills`)

From a project that should use Team Skills:

```bash
npx skills add /path/to/team-skills
```

From GitHub:

```bash
npx skills add fere-ai/team-skills
npx skills add fere-ai/team-skills --skill team-skill-authoring
npx skills add fere-ai/team-skills -g          # all your projects
```

The CLI copies or symlinks each skill into the agent-native folder (`.cursor/skills`, `.claude/skills`, `.agents/skills`, and [dozens more](https://github.com/vercel-labs/skills#supported-agents)).

### Cursor

Project: `npx skills add <source> -a cursor`

Or symlink a single skill:

```bash
ln -s /path/to/team-skills/skills/shared/team-skill-authoring ~/.cursor/skills/team-skill-authoring
```

### Claude Code

Project: `npx skills add <source> -a claude-code`

Personal: `ln -s` into `~/.claude/skills/<skill-name>`

### Hermes

Point Hermes at this catalog (single source of truth, no copies):

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - /path/to/team-skills/skills
```

Or trust this repo as project-local skills after cloning, then run `hermes skills trust` inside it.

You can also install an individual skill from its `SKILL.md` URL once the repo is published.

### Link everything locally

```bash
./scripts/link-local.sh
./scripts/link-local.sh --dry-run
```

## Author a skill

1. Read [`skills/shared/team-skill-authoring/SKILL.md`](skills/shared/team-skill-authoring/SKILL.md).
2. Copy [`templates/skill`](templates/skill) into `skills/<audience>/<skill-name>/`.
3. Fill in frontmatter and instructions. Keep `SKILL.md` under 500 lines.
4. Validate:

```bash
python3 scripts/validate.py
python3 scripts/validate.py --write-catalog
```

## Compatibility

Skills follow the portable [Agent Skills spec](https://agentskills.io/specification): required `name` + `description`, optional `license`, `compatibility`, and string `metadata`.

Agent-specific extras (Cursor `disable-model-invocation`, Hermes `metadata.hermes`, Claude `allowed-tools`) are allowed but optional. Prefer the portable subset so one folder works everywhere.

## License

[MIT](LICENSE) © Pranav Prakash
