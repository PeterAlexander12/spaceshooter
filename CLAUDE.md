# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the game

```bash
cd arkadspel
python rymdspel.py
```

The game requires a display (it uses pygame). Dependencies are in `.venv/` — activate it first:

```bash
.venv\Scripts\activate   # Windows
python rymdspel.py
```

There are no tests or linter configurations.

## Architecture

This is a single-file pygame game loop (`rymdspel.py`) built around three functions called every frame: `handle_input()`, `update()`, and `draw()`. All modules must be run from inside the `arkadspel/` subdirectory because images are loaded with relative paths (`images/`).

### Central state

`GameState` (in `gamestate.py`) is the single mutable state container. Every game variable — lives, coins, mode, enemy list, missile list, cooldowns, keybinds, loadout — lives here. All three loop functions read and write it via a global `gamestate` instance in `rymdspel.py`.

### Game modes

`gamestate.mode` is a string that drives all branching in `handle_input()` and `draw()`. Valid values:

| Value | Meaning |
|---|---|
| `"Login"` | Profile selection/creation screen |
| `"menu"` | Main menu with difficulty selection |
| `"game"` | Active gameplay |
| `"shop"` | Item store |
| `"backpack"` | Inventory viewer |
| `"keybinds"` | Key rebinding screen |
| `"leaderboard"` | High score table |
| `"slut"` | Game over (Swedish: "end") |

### Projectiles

Two missile classes both share the same interface (`__init__(start_pos, target_pos)`, `update()`, `utanfor_skarm()`, `draw()`):

- `Missil` (`missil.py`) — basic bullet, damage=1, speed=3, used on level 1
- `Pointy_Missile` (`pointy_missile.py`) — upgraded bullet, damage=2, speed=5, used from level 2+

**Dead code**: `pointy_missil.py` (class `PointyMissil`) is an older duplicate of `pointy_missile.py` that is never imported anywhere.

### Persistence

`save.py` manages a local SQLite database (`save.db`) with four tables: `profiles`, `game_save`, `keybinds`, `leaderboard`. The DB is auto-initialized on first access. `save.py::load_keybinds` takes `(defaults, profile_id)` but should always be called through the wrapper in `keybinds.py::load_keybinds(profile_id)`.

### UI

`ui.py` defines a `TextLabel` class and pre-instantiates one module-level label per UI element. Labels for dynamic text (e.g. `label_life`, `label_score`) are updated each frame by calling `.update(new_text)` before `.draw(screen)`.

### Naming convention

The codebase mixes Swedish and English. Swedish terms that appear in code: `spelare` (player), `fiende` (enemy), `missil` (missile), `hastighet` (speed), `utanfor_skarm` (outside screen), `slut` (end/game over), `bild` (image), `x_led`/`y_led` (x/y direction).

### Known side-effects

`enemy.py`, `missil.py`, and `pointy_missile.py` each call `pygame.display.set_mode()` at module import time. This is a side effect of loading assets at module level. It works because pygame allows repeated `set_mode()` calls, but importing these modules requires `pygame.init()` to have already run.

### Dead files

- `backpack.py` — entirely commented out; was a prototype for an equip/unequip UI
- `tag.py` — standalone pgzero prototype for a two-player tag game; not part of the main game
