# Learning Log

Purpose: track Python learning progress without blocking game progress.

## Rules
- Wrong answers do not block progress.
- Record mistakes to adapt teaching level.
- Circle back to weak topics in later sessions.
- Every non-`(Dan)` coding or asset request should produce one Python check entry.
- Spelling and wording corrections should be tracked when they are corrected and tested.

## Topic Tracker

Use status values:
- `new`: introduced recently
- `practicing`: still needs reinforcement
- `secure`: child answers correctly consistently

| Topic | Related File | Status | Last Check Date | Notes |
|---|---|---|---|---|
| Variables and values | `config.py` | new |  |  |
| Functions and parameters | `world.py` | new |  |  |
| Game loop basics | `game.py` | practicing | 2026-05-13 | Added animated animals and monsters through update/draw loop; awaiting check answer. |
| If statements | `game.py` | new | 2026-05-13 | Used `if kind == "moss_cube"` to choose one monster sprite style. |
| Imports and modules | `main.py` | new |  |  |
| UI drawing flow | `ui.py` | new |  |  |
| Spelling and wording | chat prompts | practicing | 2026-05-13 | Corrected "cheep" to "sheep" successfully; corrected "do you now" to "do you know", awaiting follow-up. |

## Session Entries

Template:

### YYYY-MM-DD
- File focus:
- Python concept:
- Check question:
- Child answer summary:
- Correct/incorrect:
- What correction was given:
- Did progress continue: yes/no
- Next level adjustment:
- Circle-back topic (if needed):
- Spelling/wording correction (if any):
- Spelling/wording follow-up check:
- Spelling/wording outcome:

### 2026-05-13
- File focus: `game.py`
- Python concept: A list can hold many similar things; `self.animals` stores each animal dictionary so the update and draw loops can handle all animals.
- Check question: In `game.py`, what does the `for animal in self.animals:` loop help the game do?
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep list/loop examples concrete and tied to visible sprites.
- Circle-back topic (if needed): Lists and loops in `game.py`
- Spelling/wording correction (if any): Modeled "sheep" instead of "cheep" for the animal name.
- Spelling/wording follow-up check: How do you spell the animal: `sheep` or `cheep`?
- Spelling/wording outcome: Correct; child wrote "sheep" after the correction.

### 2026-05-13
- File focus: `game.py`
- Python concept: A dictionary can keep related values together; each monster stores keys like `"kind"`, `"rect"`, `"vx"`, and `"anim_time"`.
- Check question: In `game.py`, what does the `"kind"` value tell the monster drawing code?
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep dictionary examples visible and tied to sprite type selection.
- Circle-back topic (if needed): Dictionaries in `game.py`
- Spelling/wording correction (if any): Modeled "Do you know Minecraft?" instead of "do you now minecraft".
- Spelling/wording follow-up check: Which word fits here: "Do you ___ Minecraft?" `know` or `now`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-13
- File focus: `game.py`
- Python concept: An `if` statement lets the code choose between two paths; `if kind == "moss_cube"` draws the green block monster, otherwise it draws the purple one.
- Check question: In `game.py`, what does the `if kind == "moss_cube"` line help choose?
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Use simple visual examples for `if` checks.
- Circle-back topic (if needed): If statements in `game.py`
- Spelling/wording correction (if any): None.
- Spelling/wording follow-up check: Previous check still open: Which word fits here, `know` or `now`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-13
- File focus: `game.py`
- Python concept: Changing numbers inside `pygame.Rect(...)` changes where a blocky sprite part is drawn.
- Check question: In `pygame.Rect(16, 5, 32, 24)`, which number controls the rectangle width?
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep rectangle questions concrete and visible.
- Circle-back topic (if needed): Rect values in `game.py`
- Spelling/wording correction (if any): None.
- Spelling/wording follow-up check: Previous check still open: Which word fits here, `know` or `now`?
- Spelling/wording outcome: Not answered yet.
