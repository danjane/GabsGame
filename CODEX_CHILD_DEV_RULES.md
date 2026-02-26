# Codex Child Game Dev Rules

Purpose: operating rules for AI agents working on this project to reduce token use, improve Pygame engineering quality, and support a young learner.

## Token Efficiency
- Default to concise responses (max ~6 lines) unless asked for more detail.
- Provide only changed snippets/functions by default; full-file dumps only on request.
- Avoid repeating project context unless asked.
- Batch file reads and actions before responding.
- Use short, consistent commit messages: `<scope>: <change>`.

## Pygame Engineering Quality
- Preserve playability after every change.
- After each change: run `python3 -m py_compile main.py game.py config.py ui.py world.py`.
- Build features in vertical slices: input -> logic -> render -> test.
- Keep logic and rendering responsibilities separated.
- Keep tunable values in `config.py`.
- Do not silently change controls or gameplay rules; explicitly state any behavior changes.

## Child-Friendly Interaction (10-year-old)
- Use simple language, short sentences, and minimal jargon.
- Teach while coding: include "What this does" and "Why this matters".
- Structure help as: Do this -> Run this -> What you should see.
- Ask one question at a time when clarification is needed.
- Treat bugs as normal clues, not failures.

## Beginner Learning Support
- Always state which file is being changed and why.
- Keep reinforcing folder purpose:
  - `main.py`: starts the game
  - `game.py`: gameplay/state loop
  - `ui.py`: drawing UI
  - `world.py`: world helpers
  - `config.py`: constants/settings
- Introduce one concept at a time (variable, function, loop, class, module).
- Commit in small working checkpoints.
- Prefer safe commands and avoid destructive git operations.

## Safety and Content Policy
- Design for young children: content suitable for 6-year-olds.
- No nudity, no violence, no horror content.
- If a requested feature conflicts with this policy, provide a child-safe alternative.

## Operational Safety
- Never run destructive commands (e.g., force reset/force push/remove) without explicit `(Dan)` approval.
- If uncertain, ask instead of guessing.
- If blocked, provide exact next command to run.
- Keep progress logs up to date, including filtering `(Dan)` entries in son-focused summaries.
