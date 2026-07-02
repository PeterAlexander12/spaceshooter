import sqlite3

DB = "save.db"

def _init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS game_save (
                profile_id INTEGER PRIMARY KEY,
                coins INTEGER,
                health_potions INTEGER,
                strength_potions INTEGER,
                bombs INTEGER
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS keybinds (
                profile_id INTEGER,
                action TEXT,
                value INTEGER,
                PRIMARY KEY (profile_id, action)
            )
        """)

def get_profiles():
    _init_db()
    with sqlite3.connect(DB) as con:
        rows = con.execute("SELECT id, name FROM profiles").fetchall()
    return rows

def create_profile(name):
    _init_db()
    with sqlite3.connect(DB) as con:
        con.execute("INSERT INTO profiles (name) VALUES (?)", (name,))
        profile_id = con.execute("SELECT id FROM profiles WHERE name = ?", (name,)).fetchone()[0]
        con.execute("INSERT INTO game_save (profile_id, coins, health_potions, strength_potions, bombs) VALUES (?, 0, 0, 0, 0)", (profile_id,))
    return profile_id

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
            len(loadout.health_potions),
            len(loadout.strength_potions),
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
        loadout.add_health_potion()
    for _ in range(strength_potions):
        loadout.add_strength_potion()
    for _ in range(bombs):
        loadout.add_bomb()
    return coins
