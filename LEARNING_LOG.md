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
| Animation timers | `game.py` | secure | 2026-05-14 | Child correctly chose that `player_anim_time` helps the sprite animate while walking. |
| Boolean state | `game.py` | new | 2026-05-14 | Added `inside_house` to switch between outside world drawing and house interior drawing; awaiting check answer. |
| Rect movement | `game.py` | practicing | 2026-05-14 | Added `indoor_player` rectangle so the character can move inside the house view; awaiting check answer. |
| Dictionaries | `game.py` | practicing | 2026-05-31 | Child correctly chose that `"smelted_stone"` is a dictionary key; keep practicing with inventory examples. |
| UI drawing flow | `ui.py` | new |  |  |
| Random seeds | `config.py`, `game.py`, `world.py` | practicing | 2026-05-31 | Added `LANDSCAPE_SEED`, `random.Random(...)`, and seeded spawn helpers for repeatable starting landscapes; changed default seed to `minecraft`; awaiting check answer. |
| Spelling and wording | chat prompts | practicing | 2026-05-31 | Corrected "cheep" to "sheep", "replays" to "replace", "to" to "too", "wy" to "why", and "do you now" to "do you know" successfully; modeled "pickaxe" instead of "picacks" and "will" instead of "wil"; "taler" to "taller", "make it so", and "changes to brown" still await follow-up. |

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

### 2026-05-14
- File focus: `game.py`
- Python concept: A timer variable can make animation change over time. `player_anim_time` grows while the player walks, and `math.sin(...)` turns that time into a smooth bobbing motion.
- Check question: What does `player_anim_time` help the player sprite do? A. Animate while walking B. Stop drawing forever
- Child answer summary: Chose A.
- Correct/incorrect: correct
- What correction was given: Confirmed that `player_anim_time` helps the sprite animate while walking.
- Did progress continue: yes
- Next level adjustment: Keep animation explanations tied to visible movement.
- Circle-back topic (if needed): Animation timers in `game.py`
- Spelling/wording correction (if any): Modeled "too" instead of "to" in "could the main character be animated too".
- Spelling/wording follow-up check: Pending: Which word means "also", `too` or `to`?
- Spelling/wording outcome: Correct; child chose `too`.

### 2026-05-14
- File focus: `game.py`
- Python concept: A boolean stores yes/no state. `inside_house` is `True` when the house interior should draw, and `False` when the outside world should draw.
- Check question: When `inside_house` is `True`, what should the game draw? A. The house interior B. Only trees
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep boolean checks tied to visible screen changes.
- Circle-back topic (if needed): Boolean state in `game.py`
- Spelling/wording correction (if any): Modeled "changes to brown" instead of "changes too brown".
- Spelling/wording follow-up check: Pending: Which word shows direction here, `to` or `too`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-14
- File focus: `game.py`
- Python concept: A `pygame.Rect` stores position and size. The new `indoor_player` rect lets the player move around inside the house without changing the outdoor world position.
- Check question: Which value changes when a rect moves left or right? A. `x` B. `height`
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep rect movement checks concrete.
- Circle-back topic (if needed): Rect movement in `game.py`
- Spelling/wording correction (if any): Modeled "why" instead of "wy".
- Spelling/wording follow-up check: Pending: Which spelling is right, `why` or `wy`?
- Spelling/wording outcome: Correct; child chose `why`.

### 2026-05-14
- File focus: `game.py`
- Python concept: A dictionary stores values by name. The inventory dictionary now has keys like `"furnace"`, `"smelted_stone"`, and `"smelted_pickaxe"`.
- Check question: In `self.inventory["smelted_stone"]`, what is `"smelted_stone"`? A. A dictionary key B. A screen color
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep dictionary checks tied to inventory items.
- Circle-back topic (if needed): Dictionaries in `game.py`
- Spelling/wording correction (if any): Modeled "pickaxe" instead of "picacks".
- Spelling/wording follow-up check: Pending: Which spelling is right, `pickaxe` or `picacks`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-31
- File focus: `game.py`
- Python concept: A dictionary stores values by name. The inventory dictionary uses keys like `"stone"` and `"smelted_stone"` so the game can count each item.
- Check question: In `self.inventory["smelted_stone"]`, what is `"smelted_stone"`? A. A dictionary key B. A screen color
- Child answer summary: Chose A.
- Correct/incorrect: correct
- What correction was given: Confirmed that `"smelted_stone"` is a dictionary key.
- Did progress continue: yes
- Next level adjustment: Keep dictionary examples tied to inventory; next check can ask what value a key points to.
- Circle-back topic (if needed): Dictionaries in `game.py`
- Spelling/wording correction (if any): Used the prior correction "why" instead of "wy".
- Spelling/wording follow-up check: Which spelling is right? A. `why` B. `wy`
- Spelling/wording outcome: Correct; child chose A.

### 2026-05-31
- File focus: `world.py`
- Python concept: A seed is a value that can make random world generation repeat the same way.
- Check question: Which word fits? "Do you ___ what a seed is?" A. `know` B. `now`
- Child answer summary: Chose A.
- Correct/incorrect: correct
- What correction was given: Confirmed that `know` is the right word.
- Did progress continue: yes
- Next level adjustment: If seeds are added to the game later, tie the concept to `random.seed(...)` in world setup.
- Circle-back topic (if needed): Random seeds in world generation.
- Spelling/wording correction (if any): Modeled "Do you know..." instead of "do you now...".
- Spelling/wording follow-up check: Which word fits? A. `know` B. `now`
- Spelling/wording outcome: Correct; child chose A.

### 2026-05-31
- File focus: `config.py`, `game.py`, and `world.py`
- Python concept: `random.Random(seed)` makes its own random number picker. If the seed is the same, the starting tree, stone, and animal positions repeat.
- Check question: If two games use the same landscape seed, what should happen? A. Same starting landscape B. Always a totally different landscape
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep seed checks concrete and tied to visible trees/stones.
- Circle-back topic (if needed): Random seeds in world generation.
- Spelling/wording correction (if any): Modeled "Can you add a landscape seed to our game?" as clearer wording.
- Spelling/wording follow-up check: Pending: Which phrase is clearer, `our game` or `my I mean our game`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-31
- File focus: setup command
- Python concept: The project virtual environment has its own installed packages; `venv/bin/python` can use `pygame` even when plain `python3` cannot.
- Check question: Not asked; this was an install/setup request.
- Child answer summary: Not applicable.
- Correct/incorrect: practicing
- What correction was given: Explained that `pygame` is already installed in `venv`.
- Did progress continue: yes
- Next level adjustment: Keep setup commands short and concrete.
- Circle-back topic (if needed): Virtual environments.
- Spelling/wording correction (if any): Modeled `will` instead of `wil` after "I wil try it".
- Spelling/wording follow-up check: Pending: Which spelling is right, `will` or `wil`?
- Spelling/wording outcome: Not answered yet.

### 2026-05-31
- File focus: `config.py`
- Python concept: A constant is a named value the game can reuse. `LANDSCAPE_SEED = "minecraft"` sets the default landscape seed in one place.
- Check question: If `LANDSCAPE_SEED = "minecraft"`, what is the seed value? A. `minecraft` B. `stone`
- Child answer summary: Not answered yet.
- Correct/incorrect: practicing
- What correction was given: Not yet; answer pending.
- Did progress continue: yes
- Next level adjustment: Keep constants tied to visible game settings.
- Circle-back topic (if needed): Random seeds and constants.
- Spelling/wording correction (if any): None.
- Spelling/wording follow-up check: Pending from earlier: Which spelling is right, `will` or `wil`?
- Spelling/wording outcome: Not answered yet.
