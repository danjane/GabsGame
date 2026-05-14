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
| For loops | `game.py` | secure | 2026-05-14 | Child correctly chose that a `for` loop repeats code for each item. |
| If statements | `game.py` | new | 2026-05-13 | Used `if kind == "moss_cube"` to choose one monster sprite style. |
| Imports and modules | `main.py` | new |  |  |
| Lists of objects | `game.py` | new | 2026-05-14 | Changed one house flag into `self.houses`, a list of house rectangles; awaiting check answer. |
| Removing unused code | `game.py`, `config.py` | new | 2026-05-14 | Removed monster setup, update, drawing, and constants; awaiting check answer. |
| UI drawing flow | `ui.py` | new |  |  |
| Spelling and wording | chat prompts | practicing | 2026-05-14 | Corrected "cheep" to "sheep" successfully; corrected "replays" to "replace" successfully; modeled "remove the monster part" and "make it so you can build houses everywhere"; "do you now" to "do you know" and "taler" to "taller" still await follow-up. |

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
- Python concept: Lower `y` values draw sprite parts higher on the screen; moving the head from `y=4` to `y=2` helps make the monster taller.
- Check question: In `pygame.Rect(14, 2, 36, 27)`, which number controls how high the rectangle starts?
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep rectangle-position checks visual and simple.
- Circle-back topic (if needed): Rect `y` position in `game.py`
- Spelling/wording correction (if any): Modeled "taller" instead of "taler".
- Spelling/wording follow-up check: Which spelling is right: `taller` or `taler`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-13
- File focus: `game.py`
- Python concept: A rectangle tuple uses `(x, y, width, height)`; changing the width and height makes sprite blocks chunkier.
- Check question: In `(14, 4, 36, 26)`, which two numbers are width and height?
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Continue with one tiny tuple question at a time.
- Circle-back topic (if needed): Rect tuples in `game.py`
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

### 2026-05-14
- File focus: `game.py`
- Python concept: A `for` loop repeats code for each item in a list; `for animal in self.animals:` lets the game handle each animal one at a time.
- Check question: What does a `for` loop help Python do? A. Repeat code for each item B. Stop the game forever C. Delete a file
- Child answer summary: Chose A.
- Correct/incorrect: correct
- What correction was given: Confirmed that a `for` loop repeats code for each item.
- Did progress continue: yes
- Next level adjustment: For loops can move toward simple "each item has data" examples next time.
- Circle-back topic (if needed): None.
- Spelling/wording correction (if any): Modeled "replace" instead of "replays" from an earlier prompt.
- Spelling/wording follow-up check: Which word fits: `replace`, `replays`, or `replase`?
- Spelling/wording outcome: Correct; child chose `replace`.

### 2026-05-14
- File focus: `game.py` and `config.py`
- Python concept: Removing a feature means removing each connected part: constants in `config.py`, setup in `__init__`, update calls, and draw code in `game.py`.
- Check question: If we remove a feature from `game.py`, should we also remove code that still tries to update or draw it? A. Yes B. No
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep feature-removal explanations concrete and tied to setup/update/draw.
- Circle-back topic (if needed): Removing unused code in `game.py`
- Spelling/wording correction (if any): Modeled "remove the monster part" instead of "delete the monster part".
- Spelling/wording follow-up check: Pending: Which word sounds better for a game feature, `remove` or `delete`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-14
- File focus: `game.py`
- Python concept: A list can store many things. `self.houses` stores each house rectangle, so the draw loop can show all built houses.
- Check question: In `self.houses.append(new_house)`, what does `append` do? A. Adds one item to the list B. Deletes the whole game
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep list examples tied to visible houses.
- Circle-back topic (if needed): Lists of objects in `game.py`
- Spelling/wording correction (if any): Modeled "make it so you can build houses everywhere" instead of "make that you can make houses everywhere".
- Spelling/wording follow-up check: Pending: Which phrase is clearer, `make it so` or `make that`?
- Spelling/wording outcome: Not answered yet.
