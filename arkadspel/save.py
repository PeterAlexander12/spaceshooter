import sqlite3

DB = "save.db"

def _init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS game_save (
                coins INTEGER,
                health_potions INTEGER,
                strength_potions INTEGER,
                bombs INTEGER
            )
        """)
        if con.execute("SELECT COUNT(*) FROM game_save").fetchone()[0] == 0:
            con.execute("INSERT INTO game_save VALUES (0, 0, 0, 0)")
        con.execute("""
            CREATE TABLE IF NOT EXISTS keybinds (
                action TEXT PRIMARY KEY,
                value INTEGER
            )
        """)

def save_game(coins, loadout):
    with sqlite3.connect(DB) as con:
        con.execute("""
            UPDATE game_save SET
                coins = ?,
                health_potions = ?,
                strength_potions = ?,
                bombs = ?
        """, (
            coins,
            sum(1 for p in loadout.potions if p == "health_potion"),
            sum(1 for p in loadout.potions if p == "strength"),
            len(loadout.bombs)
        ))

def save_keybinds(keybinds):
    with sqlite3.connect(DB) as con:
        for action, value in keybinds.items():
            con.execute("INSERT OR REPLACE INTO keybinds (action, value) VALUES (?, ?)", (action, value))

def load_keybinds(defaults):
    _init_db()
    with sqlite3.connect(DB) as con:
        rows = con.execute("SELECT action, value FROM keybinds").fetchall()
    keybinds = dict(defaults)
    for action, value in rows:
        if action in keybinds:
            keybinds[action] = value
    return keybinds

def load_game(loadout):
    _init_db()
    with sqlite3.connect(DB) as con:
        row = con.execute("SELECT coins, health_potions, strength_potions, bombs FROM game_save").fetchone()
    coins, health_potions, strength_potions, bombs = row
    for _ in range(health_potions):
        loadout.add_potion("health_potion")
    for _ in range(strength_potions):
        loadout.add_potion("strength")
    for _ in range(bombs):
        loadout.add_bomb()
    return coins
