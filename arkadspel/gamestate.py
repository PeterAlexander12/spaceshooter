from arkadspel.sub_menu import SubMenu
from loadout import Loadout
from keybinds import DEFAULT_KEYBINDS


class GameState:
    def __init__(self):
        self.running = True
        self.mode = "Login"
        # player
        self.Life = 3
        self.coins = 0
        self.coins_this_run = 0
        self.shoot_power = 1
        self.loadout = Loadout()
        # login
        self.Current_profile_id = None
        self.login_input = ""
        self.creating_profile = False
        # difficulty
        self.degree_of_difficulty = None
        # level
        self.level = 1
        self.kill_count = 0
        self.bonus_coins = 10
        # enemies
        self.enemies = []
        self.enemy_speed = 1
        self.number_of_enemies = 5
        self.enemyBlockChance = 1
        # missiles & explosion
        self.missiles = []
        self.explosion_size = 0
        # keybinds
        self.keybinds = dict(DEFAULT_KEYBINDS)
        self.keybind_selecting = None
        # messages
        self.shop_message = ""
        self.shop_message_timer = 0
        self.potion_message = ""
        self.potion_message_timer = 0
        self.coin_message = ""
        self.coin_message_timer = 0
        # cooldowns
        self.health_potion_cooldown = 0
        self.strength_potion_cooldown = 0
        self.bomb_cooldown = 0
        # sub menu
        self.shop_menu = SubMenu(["Gadgets", "Bullets"])
        # bullets
        self.current_bullet = "Basic Bullet"
        self.owned_bullets = ["Basic Bullet", "Pointy Bullet"]
