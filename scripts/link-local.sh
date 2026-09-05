#!/usr/bin/env bash
# Symlink PP Skills into local Cursor and Claude Code skill directories.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DRY_RUN=0
FORCE=0

usage() {
  cat <<'EOF'
Usage: scripts/link-local.sh [--dry-run] [--force]

Creates ~/.cursor/skills/<name> and ~/.claude/skills/<name> symlinks
for every skill under skills/<audience>/<name>.

Hermes: add this repo's skills/ folder as an external directory instead:

  skills:
    external_dirs:
      - /path/to/pp-skills/skills
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown flag: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

link_skill() {
  local src="$1"
  local dest="$2"
  if [[ -L "$dest" ]]; then
    local current
    current="$(readlink "$dest")"
    if [[ "$current" == "$src" ]]; then
      echo "ok   $dest"
      return
    fi
    if [[ $FORCE -eq 1 ]]; then
      [[ $DRY_RUN -eq 1 ]] && echo "relink $dest -> $src" && return
      ln -sfn "$src" "$dest"
      echo "relink $dest"
      return
    fi
    echo "skip $dest (symlink points at $current; pass --force to replace)" >&2
    return
  fi
  if [[ -e "$dest" ]]; then
    echo "skip $dest (exists and is not a symlink)" >&2
    return
  fi
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "link $dest -> $src"
    return
  fi
  mkdir -p "$(dirname "$dest")"
  ln -s "$src" "$dest"
  echo "link $dest"
}

count=0
while IFS= read -r skill_md; do
  skill_dir="$(dirname "$skill_md")"
  name="$(basename "$skill_dir")"
  for agent_root in "$HOME/.cursor/skills" "$HOME/.claude/skills"; do
    link_skill "$skill_dir" "$agent_root/$name"
  done
  count=$((count + 1))
done < <(find "$ROOT/skills" -mindepth 3 -maxdepth 3 -name SKILL.md | sort)

echo "$count skill(s) considered"
echo
echo "Hermes: set skills.external_dirs to $ROOT/skills"
