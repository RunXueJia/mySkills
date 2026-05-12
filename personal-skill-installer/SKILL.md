---
name: personal-skill-installer
description: Override Codex skill installation location for this user's personal skills. Use whenever installing, listing, updating, or discussing user-installed Codex skills so installation commands target C:\Users\16084\.agents\skills instead of $CODEX_HOME/skills or ~/.codex/skills.
---

# Personal Skill Installer

Use this skill together with the system `skill-installer` workflow whenever the user asks to install personal Codex skills, list installable skills with installed annotations, install a skill from GitHub, or update a personal skill.

## Installation Root

Treat this path as the default personal skills root:

```text
C:\Users\16084\.agents\skills
```

Do not default personal skill installation to `$CODEX_HOME/skills` or `~/.codex/skills` for this user.

## Install Behavior

- When running `skill-installer` scripts, pass `--dest C:\Users\16084\.agents\skills` unless the user explicitly gives another destination.
- When listing installable skills, compare already-installed skills against `C:\Users\16084\.agents\skills`.
- When reporting the install destination, state that the skill was installed under `C:\Users\16084\.agents\skills`.
- After installing a skill, still tell the user to restart Codex to pick up new skills.
- After every successful new skill install or personal skill update, update `C:\Users\16084\.agents\skills\INDEX.md` so it includes the skill name, category, trigger/use case, and any maintenance notes.
- If a requested skill already exists in `C:\Users\16084\.agents\skills`, do not overwrite it unless the user explicitly asks to update or replace it.

## Command Pattern

For curated or GitHub installs, adapt the system installer commands by adding the destination:

```powershell
python scripts/install-skill-from-github.py --repo openai/skills --path skills/.curated/<skill-name> --dest C:\Users\16084\.agents\skills
```

For listings, prefer installer support for installed annotations if available; otherwise inspect `C:\Users\16084\.agents\skills` directly and annotate manually.
