from sub_menu import SubMenu
from loadout import Loadout
from storage.keybinds import DEFAULT_KEYBINDS


class GameState:
    def __init__(self):
        self.running = True
        self.mode = "Login"
        # player
        self.Life = 3
        self.coins = 0
        self.coins_this_run = 0
        self.xp = 0
        self.shoot_power = 1
        self.loadout = Loadout()
        # login
        self.current_profile_id = None
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
        self.inventory_menu = SubMenu(["Gadgets", "Bullets"])
        # bullets
        self.current_bullet = "Basic Bullet"
        self.owned_bullets = ["Basic Bullet", "Pointy Bullet"]
        # quests
        self.quests = [
            {"description": "Deal 10 damage on insane mode", "Goal": 10, "Progress": 0, "Completed": False, "Reward": "100 XP", "Reward type": "XP"},
            {"description": "Drink 10 potions", "Goal": 10, "Progress": 0, "Completed": False, "Reward": "100 XP", "Reward type": "XP"},
        ]
        self.pass_tiers = [
            {"tier": 1, "XP required": 0, "Reward": "100 coins", "Claimed": True},
            {"tier": 2, "XP required": 200, "Reward": "1 health potion", "Claimed": False},
            {"tier": 3, "XP required": 400, "Reward": "5 strenght potion", "Claimed": False},
            {"tier": 4, "XP required": 600, "Reward": "100 coins", "Claimed": False},
            {"tier": 5, "XP required": 800, "Reward": "100 coins", "Claimed": False},
            {"tier": 6, "XP required": 1100, "Reward": "100 coins", "Claimed": False},
            {"tier": 7, "XP required": 1400, "Reward": "100 coins", "Claimed": False},
            {"tier": 8, "XP required": 1700, "Reward": "100 coins", "Claimed": False},
            {"tier": 8, "XP required": 2000, "Reward": "100 coins", "Claimed": False},
            {"tier": 9, "XP required": 2300, "Reward": "100 coins", "Claimed": False},
            {"tier": 9, "XP required": 2600, "Reward": "100 coins", "Claimed": False},
            {"tier": 10, "XP required": 2900, "Reward": "100 coins", "Claimed": False},

        ]
