# AI Memory for GabsGame

Purpose: quick continuity context for a new AI coding agent joining this repository.

## Project Identity
- Name: `GabsGame`
- Repo: `git@github.com:danjane/GabsGame.git`
- Engine: Python + Pygame
- Style: 2.5D isometric rendering (gameplay logic remains in top-down world coordinates)

## Current Architecture
- `main.py`: entrypoint (`Game().run()`)
- `game.py`: core orchestration (state, events, update loop, rendering, quest logic)
- `world.py`: world/spatial helpers (`random_spawn_rect`, `is_near`, `nearest_rect`)
- `ui.py`: UI rendering helpers (craft panel/details panel/marker line)
- `config.py`: constants and tunables (sizes, costs, timings, quest count)
- `README.md`: run instructions + roadmap + TODO
- `SON_AI_INTERACTIONS.md`: filtered non-`(Dan)` interaction summaries
- `assets/`: sprite/UI placeholder folder structure for incoming art

## Gameplay Systems (implemented)
- Movement: arrow keys
- Cut trees: `L`
- Mine stones: `X` (requires pickaxe)
- Make fire: `F` (cost: `1 wood + 2 stone`)
- Build house: `B` (in home area)
- Craft menu: `C` (in home area)
- Home button (`🏠`): teleport + quest turn-in
- Inventory bar with clickable detail panels
- Resource respawn timers
- Random quest chain with turn-in flow

## Quest System (implemented)
- Quests are randomized and sequential.
- `QUEST_COUNT` in `config.py` controls total quests per run (currently 5).
- Quest progress uses cumulative stats (not raw inventory values) to avoid regression when resources are spent.
- On completion of current quest, player must press home (`🏠`) to claim and receive the next quest.

## Rendering Model (important)
- Rendering is 2.5D isometric in `game.py`.
- Core interactions/collisions still use top-down `pygame.Rect` world-space logic.
- Isometric conversion is visualized via projection helpers (`iso_point`, `iso_rect_poly`, prism drawing).
- If gameplay bugs occur, verify whether they are logic-space vs render-space mismatches.

## Assets Plan
Use these folders for downloaded/generated images:
- `assets/sprites/player/`
- `assets/sprites/trees/`
- `assets/sprites/stones/`
- `assets/sprites/house/`
- `assets/ui/`

## Collaboration Rules from Dan
- Messages prefixed with `(Dan)` are parent instructions/context.
- In summaries of son progress, `(Dan)` interactions should be excluded.
- `SON_AI_INTERACTIONS.md` should be maintained accordingly.
- Dan requested commits after each code/structure change.

## Git / Commit Workflow
- Commit after each meaningful code or structure change.
- Push to `origin/main` when network allows.
- Current environment may intermittently fail DNS for `github.com`; if push fails, leave a clean local commit and report exact command to run.

## Known Open Work
- Integrate actual sprite animations from `assets/` into render pipeline.
- Add save/load persistence for game/quest state.
- Continue isometric polish (depth sorting edge cases, readability, potential occlusion handling).
- Improve quest balancing/reward pacing.

## Safe First Steps for New Agent
1. Run compile check: `python3 -m py_compile main.py game.py config.py ui.py world.py`
2. Run game: `python main.py`
3. Confirm controls + quest turn-in work.
4. If touching summaries, update `SON_AI_INTERACTIONS.md` with `(Dan)` filtering.
5. Commit + push.
