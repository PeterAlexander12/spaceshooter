# Spaceshooter — Architecture Overview

## Game Loop

`rymdspel.py` runs a loop every frame:

```
handle_input() → update() → draw()
```

- **handle_input()** — reads keyboard and mouse events, changes state
- **update()** — moves enemies, missiles, checks collisions, handles timers
- **draw()** — renders everything to the screen based on current mode

---

## State Machine

All mutable game state lives in the `GameState` class (`gamestate.py`).
The most important field is `gamestate.mode` — a string that controls which screen is active.

| Mode | Screen |
|---|---|
| `"Login"` | Profile select / create |
| `"menu"` | Difficulty selection + icons |
| `"game"` | Actual gameplay |
| `"slut"` | Game over / score |
| `"shop"` | Buy consumables |
| `"inventory"` | Equip bullets, view items |
| `"settings"` | Logout, go to keybinds |
| `"keybinds"` | Rebind keys |
| `"leaderboard"` | Top scores |

In `handle_input()` and `draw()`, every block is gated on the current mode:

```python
if gamestate.mode == "shop":
    # handle shop input / draw shop
elif gamestate.mode == "inventory":
    # handle inventory input / draw inventory
```

---

## File Structure

| File | Responsibility |
|---|---|
| `rymdspel.py` | Main loop, input handling, draw calls |
| `gamestate.py` | Central state container (mode, coins, life, bullets, …) |
| `ui.py` | All `TextLabel` instances and label lists |
| `sub_menu.py` | `SubMenu` class for tab navigation |
| `missil.py` | Basic bullet missile class |
| `pointy_missile.py` | Pointy bullet missile class |
| `player.py` | Player sprite and movement |
| `enemy.py` | Enemy sprite and AI |
| `loadout.py` | Bombs, health potions, strength potions |
| `save.py` | SQLite save/load (coins, loadout, scores, keybinds) |
| `keybinds.py` | Default keybind constants and helpers |

---

## UI System

`ui.py` holds two types of text rendering:

**`TextLabel`** — creates a surface and stores a `.rect`. Use when you need to click on text.
```python
label_easy = TextLabel(font, "1 - Easy", (0, 255, 0), (300, 250))
# later:
label_easy.rect.collidepoint(event.pos)  # click detection
label_easy.draw(screen)
```

**`render_text()`** — draws text once and throws the position away. Use for headings and static text that never needs to be clicked.

---

## Bullet System

Owned bullets are tracked in `GameState`:

```python
self.owned_bullets = ["Basic Bullet", "Pointy Bullet"]
self.current_bullet = "Basic Bullet"
```

When the player fires (left click in game mode), the current bullet determines which missile class is spawned:

```python
if gamestate.current_bullet == "Pointy Bullet":
    gamestate.missiles.append(PointyMissile(...))
else:
    gamestate.missiles.append(Missil(...))
```

Equipping is done in the inventory screen by clicking the "Equip" label next to a bullet.

---

## Save System

`save.py` uses SQLite. It stores:
- **Profiles** — player name and id
- **Coins and loadout** — saved on shop purchase and on exit
- **Keybinds** — saved when leaving the keybinds screen
- **Scores** — saved on game over; leaderboard shows each player's personal best
