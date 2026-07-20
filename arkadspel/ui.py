import pygame

font = pygame.font.Font(None, 40)
stor_font = pygame.font.Font(None, 65)


class TextLabel:
    def __init__(self, font, text, color, pos, centered=True):
        self.font = font
        self.color = color
        self.pos = pos
        self.centered = centered
        self._render(text)

    def _render(self, text):
        self.surface = self.font.render(text, True, self.color)
        if self.centered:
            self.rect = self.surface.get_rect(center=self.pos)
        else:
            self.rect = self.surface.get_rect(topleft=self.pos)

    def update(self, text):
        self._render(text)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


def render_text(screen, font_obj, text, color, pos, centered=True):
    surf = font_obj.render(text, True, color)
    if centered:
        screen.blit(surf, surf.get_rect(center=pos))
    else:
        screen.blit(surf, surf.get_rect(topleft=pos))


# Login
label_select_profile = TextLabel(stor_font, "Select Profile", (0, 255, 0), (300, 100))
label_enter_confirm = TextLabel(font, "Enter to confirm, Esc to cancel", (178, 34, 34), (300, 545))
label_name_input = TextLabel(font, "Name: ", (0, 255, 200), (300, 500))

# Menu
label_choose_difficulty = TextLabel(stor_font, "Choose difficulty", (255, 255, 255), (370, 150))
label_easy = TextLabel(font, "1 - Easy", (0, 255, 0), (300, 250))
label_medium = TextLabel(font, "2 - Medium", (255, 255, 0), (300, 300))
label_hard = TextLabel(font, "3 - Hard", (255, 165, 0), (300, 350))
label_insane = TextLabel(font, "4 - Insane", (255, 0, 0), (300, 400))
label_leaderboard_hint = TextLabel(font, "L - Leaderboard", (200, 200, 200), (300, 450))
label_shop_key = TextLabel(stor_font, "S", (0, 255, 0), (225, 110))
label_inventory_key = TextLabel(stor_font, "E", (0, 255, 0), (395, 110))

# Leaderboard
label_leaderboard_title = TextLabel(stor_font, "Leaderboard", (255, 255, 255), (300, 50))
label_leaderboard_leave = TextLabel(font, "Esc - Back", (178, 34, 34), (10, 10), centered=False)

# Shop
label_shop_title = TextLabel(stor_font, "shop", (0, 255, 0), (250, 200))
label_bomb_item = TextLabel(font, "1 - Bomb", (255, 255, 255), (100, 250), centered=False)
label_health_item = TextLabel(font, "2 - Health Potion", (255, 255, 255), (100, 300), centered=False)
label_strength_item = TextLabel(font, "3 - Strength Potion", (255, 255, 255), (100, 350), centered=False)
label_leave_shop = TextLabel(font, "Esc - Leave shop", (178, 34, 34), (120, 30))
label_bomb_price = TextLabel(font, "5000 coins", (255, 255, 255), (400, 265))
label_health_price = TextLabel(font, "300 coins", (255, 255, 255), (400, 315))
label_strength_price = TextLabel(font, "400 coins", (255, 255, 255), (430, 365))
label_shop_message = TextLabel(font, "", (255, 215, 0), (300, 80))

# Inventory
label_bomb_count = TextLabel(font, "You have 0 bombs!", (255, 255, 255), (200, 250), centered=False)
label_health_count = TextLabel(font, "You have 0 health potions!", (255, 255, 255), (200, 300), centered=False)
label_strength_count = TextLabel(font, "You have 0 strength potions!", (255, 255, 255), (200, 350), centered=False)
label_leave_inventory = TextLabel(font, "Esc - Leave inventory", (178, 34, 34), (150, 30))
label_coin_count = TextLabel(font, "You have 0 coins!", (255, 215, 0), (150, 550), centered=False)
label_tab_switch_gears = TextLabel(font, "Gears", (255, 215, 0), (150, 550), centered=False)
# bullets tab
label_pointy_bullet_item = TextLabel(font, "Pointy bullet", (255, 215, 0), (300, 80), centered=False)
label_tab_switch_bullets = TextLabel(font, "Bullets", (255, 215, 0), (300, 80), centered=False)

# Keybinds
label_key_settings_title = TextLabel(stor_font, "Key Settings", (0, 255, 0), (300, 150))
label_bind_health = TextLabel(font, "1 - Use Health Potion: space", (255, 255, 255), (100, 250), centered=False)
label_bind_strength = TextLabel(font, "2 - Use Strength Potion: z", (255, 255, 255), (100, 300), centered=False)
label_bind_shop = TextLabel(font, "3 - Open Shop: s", (255, 255, 255), (100, 350), centered=False)
label_bind_inventory = TextLabel(font, "4 - Open inventory: e", (255, 255, 255), (100, 400), centered=False)
label_bind_bomb = TextLabel(font, "5 - Use Bomb: right click", (255, 255, 255), (100, 450), centered=False)
label_save_back = TextLabel(font, "Esc - Save and go back", (178, 34, 34), (100, 550), centered=False)
label_waiting = TextLabel(font, "", (255, 215, 0), (300, 530))

# Settings
label_settings_title = TextLabel(stor_font, "Settings", (0, 255, 0), (300, 50))
label_settings_logout = TextLabel(font, "Logout", (178, 34, 34), (250, 150), centered=False)
label_settings_key_settings = TextLabel(font, "K - Keybinds", (200, 200, 200), (250, 200), centered=False)
label_settings_leave = TextLabel(font, "Esc - go back", (178, 34, 34), (5, 5), centered=False)

# Game Over
label_game_over = TextLabel(stor_font, "Game Over!", (255, 0, 0), (300, 180))
label_press_space = TextLabel(font, "Press space too go to the menu ", (255, 255, 255), (300, 370))
label_score = TextLabel(font, "Coins this run: 0", (255, 215, 0), (300, 260))
label_rank = TextLabel(font, "Rank: #0 of 0", (255, 255, 255), (300, 300))

# Game HUD
label_life = TextLabel(font, "Life: 3", (255, 255, 255), (10, 10), centered=False)
label_coins_run = TextLabel(font, "Coins this run: 0", (255, 215, 0), (200, 10), centered=False)
label_level = TextLabel(font, "Level: 1", (255, 255, 255), (10, 570), centered=False)
label_potion_message = TextLabel(font, "", (255, 215, 0), (300, 50))
label_coin_message = TextLabel(font, "", (255, 215, 0), (300, 80))
