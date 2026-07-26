# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Context

This is a pygame space shooter built by Peter and his nephew Oliver as a learning project.
Oliver is a fast learner but still building his Python foundations — keep explanations concrete.
Always explain a proposed change and wait for explicit approval before editing any file.

## Running the game

Run from the project root using the PyCharm run configuration (`spaceshooter`) or:

```bash
python rymdspel.py
```

All image paths are relative (`images/`), so the working directory must be the project root.
The game requires a display (pygame). Dependencies are in `.venv/`.

There are no tests or linter configurations.

## Architecture

Single-file pygame game loop (`rymdspel.py`) built around three functions called every frame:
`handle_input()` → `update()` → `draw()`

### Central state

`GameState` (`gamestate.py`) is the single mutable state container. Every game variable — lives,
coins, mode, enemy list, missile list, cooldowns, keybinds, loadout, bullet ownership — lives here.
All three loop functions read and write it via a global `gamestate` instance in `rymdspel.py`.

### Game modes

`gamestate.mode` is a string that drives all branching in `handle_input()` and `draw()`:

| Value | Meaning |
|---|---|
| `"Login"` | Profile selection/creation screen |
| `"menu"` | Main menu with difficulty selection |
| `"game"` | Active gameplay |
| `"shop"` | Item store |
| `"inventory"` | Bullet equip screen + consumable counts |
| `"settings"` | Settings menu (logout, go to keybinds) |
| `"keybinds"` | Key rebinding screen |
| `"leaderboard"` | High score table |
| `"slut"` | Game over (Swedish: "end") |

### Projectiles

Two missile classes share the same interface (`__init__(start_pos, target_pos)`, `update()`,
`utanfor_skarm()`, `draw()`):

- `Missil` (`missil.py`) — basic bullet, damage=1, speed=3
- `PointyMissile` (`pointy_missile.py`) — upgraded bullet, damage=2, speed=5

Which one fires is determined by `gamestate.current_bullet` (a string: `"Basic Bullet"` or
`"Pointy Bullet"`). Owned bullets are listed in `gamestate.owned_bullets`.

### UI

`ui.py` defines `TextLabel` and pre-instantiates one label per UI element. Labels with dynamic
text call `.update(new_text)` before `.draw(screen)` each frame. `render_text()` is for
one-off text that never needs click detection (no `.rect` stored).

For clickable bullet rows in the inventory, `ui.bullet_labels` and `ui.equip_labels` are lists
of `TextLabel` indexed to match `gamestate.owned_bullets`.

### Persistence

`save.py` manages a local SQLite database (`save.db`) with four tables: `profiles`, `game_save`,
`keybinds`, `leaderboard`. The DB is auto-initialized on first access. Always call
`keybinds.load_keybinds(profile_id)` — not the raw `save.py` version directly.

### Naming conventions (PEP 8)

The codebase is being brought into PEP 8 compliance:
- Files and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `ALL_CAPS`

Swedish terms still in code: `spelare` (player), `fiende` (enemy), `missil` (missile),
`hastighet` (speed), `utanfor_skarm` (outside screen), `slut` (end/game over), `bild` (image).

### Known side-effects

`enemy.py`, `missil.py`, and `pointy_missile.py` each call `pygame.display.set_mode()` at module
import time. This works because pygame allows repeated `set_mode()` calls, but these modules
require `pygame.init()` to have already run — `rymdspel.py` calls it before any imports.

## Current work (last session)

We were building out the **bullet equip system** with Oliver:

- `gamestate.owned_bullets` — list of bullets the player owns
- `gamestate.current_bullet` — which bullet is currently equipped
- Inventory screen shows owned bullets; unequipped ones have a clickable "Equip" label
- `ui.bullet_labels` and `ui.equip_labels` in `ui.py` are the label lists for this

**Open bug**: equipping Pointy Bullet in inventory does not appear to change what fires in game.
The firing code at the `MOUSEBUTTONDOWN` handler in `rymdspel.py` checks `gamestate.current_bullet`
and should spawn `PointyMissile` — but the user reported it still fires `Missil`. Root cause not
yet confirmed (we could not add debug output before the session ended).

**Also deferred**:
- Shop tabs (Gadgets / Bullets) using `SubMenu` — class exists in `sub_menu.py`, not wired up yet
- Inventory tabs — same, planned for later
- Pointy Bullet is currently always in `owned_bullets` for testing; it should only appear after
  being purchased in the shop (no shop tab for bullets exists yet)
