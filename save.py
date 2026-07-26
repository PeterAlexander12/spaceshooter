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
        con.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER,
                score_coins INTEGER,
                score_level INTEGER,
                difficulty TEXT,
                date TEXT
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

def save_game(coins, loadout, profile_id):
    with sqlite3.connect(DB) as con:
        con.execute("""
            UPDATE game_save SET
                coins = ?,
                health_potions = ?,
                strength_potions = ?,
                bombs = ?
                WHERE profile_id = ?
        """, (
            coins,
            len(loadout.health_potions),
            len(loadout.strength_potions),
            len(loadout.bombs),
            profile_id
        ))

def save_keybinds(keybinds, profile_id):
    with sqlite3.connect(DB) as con:
        for action, value in keybinds.items():
            con.execute("INSERT OR REPLACE INTO keybinds (profile_id, action, value) VALUES (?, ?, ?)", (profile_id, action, value))

def load_keybinds(defaults, profile_id):
    _init_db()
    with sqlite3.connect(DB) as con:
        rows = con.execute("SELECT action, value FROM keybinds WHERE profile_id = ?", (profile_id,)).fetchall()
    keybinds = dict(defaults)
    for action, value in rows:
        if action in keybinds:
            keybinds[action] = value
    return keybinds

def save_score(profile_id, coins, level, difficulty, date):
    with sqlite3.connect(DB) as con:
        con.execute("""
            INSERT INTO leaderboard (profile_id, score_coins, score_level, difficulty, date)
            VALUES (?, ?, ?, ?, ?)
        """, (profile_id, coins, level, difficulty, date))

def load_scores():
    with sqlite3.connect(DB) as con:
        rows = con.execute("""
            SELECT p.name, MAX(l.score_coins)
            FROM leaderboard l
            JOIN profiles p ON l.profile_id = p.id
            GROUP BY l.profile_id
            ORDER BY MAX(l.score_coins) DESC
        """).fetchall()
    return rows

def load_game(loadout, profile_id):
    _init_db()
    with sqlite3.connect(DB) as con:
        row = con.execute("SELECT coins, health_potions, strength_potions, bombs FROM game_save WHERE profile_id = ?", (profile_id,)).fetchone()
    coins, health_potions, strength_potions, bombs = row
    for _ in range(health_potions):
        loadout.add_health_potion()
    for _ in range(strength_potions):
        loadout.add_strength_potion()
    for _ in range(bombs):
        loadout.add_bomb()
    return coins
