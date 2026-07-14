import pygame, sys
import random
import datetime

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# load pictures
player_pic = pygame.image.load("images/spelare.png").convert_alpha()
enemy_pic = pygame.image.load("images/fiende.png").convert_alpha()
enemy_pic = pygame.transform.scale(enemy_pic, (50, 50))
potion_pic = pygame.image.load("images/Red_potion.png").convert_alpha()
potion_pic = pygame.transform.scale(potion_pic, (30, 30))
explosion_pic = pygame.image.load("images/nuclear_explosion.png").convert_alpha()
bomb_pic = pygame.transform.scale(explosion_pic, (30, 30))
player_pic = pygame.transform.scale(player_pic, (50, 50))
missil_pic = pygame.image.load("images/bullet.png").convert_alpha()
background_pic = pygame.image.load("images/background.png").convert()
Shop_pic = pygame.image.load("images/shop.png").convert_alpha()
Shop_pic = pygame.transform.scale(Shop_pic, (80, 80))
cogwheel_pic = pygame.image.load("images/cogwheel.png").convert_alpha()
cogwheel_pic = pygame.transform.scale(cogwheel_pic, (120, 120))
cogwheel_rect = pygame.Rect(490, 10, 80, 80)
Backpack_pic = pygame.image.load("images/backpack.png").convert_alpha()
Backpack_pic = pygame.transform.scale(Backpack_pic, (100, 100))
Strength_potion_pic = pygame.image.load("images/strength_potion.png").convert_alpha()
Strength_potion_pic = pygame.transform.scale(Strength_potion_pic, (30, 30))

from player import Player

from enemy import Enemy

from missil import Missil
from loadout import Loadout
from save import save_game, load_game, save_keybinds, get_profiles, create_profile, load_scores, save_score
from keybinds import load_keybinds, bind_name, DEFAULT_KEYBINDS
import ui

# game variables
Player = Player(screen, player_pic)
loadout = Loadout()
explosion_size = 0
missiles = []
Life = 3
#shop
bomb_price = 5000
health_potion_price = 300
strength_potion_price = 400
shop_message = ""
shop_message_timer = 0
# potions
strength_potion_timer = 0
potion_message_timer = 0
potion_message = ""
#level
kill_count = 0
level = 1
# enemies
number_of_enemies = 5
enemies = []
# for upgrades
shoot_power = 1
enemy_speed = 1
# Dodge
enemyBlockChance = 1
MaxDodgeChance = 20
# Login
mode = "Login"
Current_profile_id = None
login_input = ""
creating_profile = False
# difficulty
degree_of_difficulty = None
# coin
bonus_coins = 10
coin_message = ""
coin_message_timer = 0
coins_this_run = 0
# cooldown
health_potion_cooldown = 0
strength_potion_cooldown = 0
bomb_cooldown = 0
keybinds = dict(DEFAULT_KEYBINDS)
keybind_selecting = None


coins = 0


def spawn_enemies(hp):
    for i in range(number_of_enemies):
        enemies.append(Enemy(hp, enemy_speed))


def level_up():
    global level, Life, shoot_power, enemy_speed, coins, bonus_coins, coin_message, coin_message_timer, coins_this_run, enemyBlockChance
    level += 1

    if degree_of_difficulty == "easy":
        coins += bonus_coins * level
        coins_this_run += bonus_coins * level
    if degree_of_difficulty == "medium":
        bonus_coins = 20
        coins += bonus_coins * level
        coins_this_run += bonus_coins * level
    if degree_of_difficulty == "hard":
        bonus_coins = 30
        coins += bonus_coins * level
        coins_this_run += bonus_coins * level
    if degree_of_difficulty == "insane":
        bonus_coins = 50
        coins += bonus_coins * level
        coins_this_run += bonus_coins * level

    coin_message = "+" + str(bonus_coins * level) + " coins!"
    coin_message_timer = 90

    upgrade = random.choice(["extra_Life", "shoot_power"])
    if upgrade == "extra_Life":
        Life += 1
    if upgrade == "shoot_power":
        shoot_power += 1

    enemy_upgrade = random.choice(["enemy_dodge", "enemy_speed"])
    if enemy_upgrade == "enemy_dodge":
        enemyBlockChance = min(MaxDodgeChance, enemyBlockChance + 1)
    if enemy_upgrade == "enemy_speed":
        enemy_speed += 1

    return 3 + level


def restart():
    global Life, mode, enemies, missiles, kill_count, level, shoot_power, enemy_speed, coins_this_run, bomb_cooldown, health_potion_cooldown, strength_potion_cooldown
    Life = 3
    mode = "menu"
    kill_count = 0
    level = 1
    shoot_power = 1
    enemy_speed = 1
    Player.rect.center = (300, 300)
    missiles = []
    enemies = []
    coins_this_run = 0
    spawn_enemies(3)
    bomb_cooldown = 0
    health_potion_cooldown = 0
    strength_potion_cooldown = 0




def handle_input():
    global running, mode, degree_of_difficulty, Life, enemy_speed, explosion_size, number_of_enemies, health_potion_cooldown, strength_potion_cooldown, bomb_cooldown, keybind_selecting, coins, shop_message, shop_message_timer, shoot_power, potion_message_timer, potion_message, Current_profile_id, login_input, creating_profile, keybinds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(coins, loadout, Current_profile_id)
            running = False

        if event.type == pygame.KEYDOWN:
            if mode == "Login":
                if not creating_profile:
                    profiles = get_profiles()
                    for i, (pid, name) in enumerate(profiles):
                        if event.key == pygame.K_1 + i:
                            Current_profile_id = pid
                            coins = load_game(loadout, Current_profile_id)
                            keybinds = load_keybinds(Current_profile_id)
                            mode = "menu"
                    if event.key == pygame.K_n:
                        creating_profile = True
                else:
                    if event.key == pygame.K_RETURN:
                        if login_input.strip():
                            Current_profile_id = create_profile(login_input.strip())
                            coins = load_game(loadout, Current_profile_id)
                            keybinds = load_keybinds(Current_profile_id)
                            login_input = ""
                            creating_profile = False
                            mode = "menu"
                    elif event.key == pygame.K_BACKSPACE:
                        login_input = login_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        login_input = ""
                        creating_profile = False
                    else:
                        login_input += event.unicode

            elif mode == "menu":
                if event.key == pygame.K_1:
                    degree_of_difficulty = "easy"
                    mode = "game"
                    Life = 5
                    spawn_enemies(3)
                    number_of_enemies -= 1
                if event.key == pygame.K_2:
                    degree_of_difficulty = "medium"
                    mode = "game"
                    spawn_enemies(3)
                if event.key == pygame.K_3:
                    degree_of_difficulty = "hard"
                    mode = "game"
                    enemy_speed = 2
                    spawn_enemies(3)
                    number_of_enemies += 1
                    Life = 2
                if event.key == pygame.K_4:
                    degree_of_difficulty = "insane"
                    mode = "game"
                    Life = 1
                    enemy_speed = 3
                    spawn_enemies(3)
                    number_of_enemies += 2

                if event.key == pygame.K_ESCAPE:
                    mode = "menu"
                if event.key == keybinds["open_shop"]:
                    mode = "shop"
                if event.key == keybinds["open_backpack"]:
                    mode = "Backpack"
                if event.key == pygame.K_k:
                    mode = "keybinds"

                if event.key == pygame.K_l:
                    mode = "leaderboard"

            if mode == "game":

                if event.key == keybinds["use_health_potion"]:
                    if health_potion_cooldown == 0:
                        loadout.get_health_potion()
                        potion_message = "You drank a Health Potion!"
                        Life += 1
                        health_potion_cooldown = 150
                        potion_message_timer = 30

                if event.key == keybinds["use_strength_potion"]:
                    if strength_potion_cooldown == 0:
                        loadout.get_strength_potion()
                        potion_message = "You drank a Strength Potion!"
                        shoot_power += 1
                        strength_potion_cooldown = 150
                        potion_message_timer = 30

                if event.key == keybinds["use_bomb"]:
                    if bomb_cooldown == 0:
                        if loadout.use_bomb():
                            enemies.clear()
                            explosion_size = 10
                            bomb_cooldown = 600

                if event.key == pygame.K_ESCAPE:
                    save_game(coins, loadout, Current_profile_id)
                    mode = "menu"
                    restart()

            if mode == "leaderboard":
                if event.key == pygame.K_ESCAPE:
                    mode = "menu"

            if mode == "Backpack":
                if event.key == pygame.K_ESCAPE:
                    mode = "menu"

            if mode == "shop":
                if event.key == pygame.K_2:
                    if coins > 299:
                        loadout.add_health_potion()
                        coins -= 300
                        save_game(coins, loadout, Current_profile_id)
                        shop_message = "You bought a health potion"
                    else:
                        shop_message = "You brokey! You don´t have enough coins!"
                    shop_message_timer = 30
                if event.key == pygame.K_1:
                    if coins > 4999:
                        loadout.add_bomb()
                        coins -= 5000
                        save_game(coins, loadout, Current_profile_id)
                        shop_message = "You bought a bomb"
                if event.key == pygame.K_3:
                    if coins > 299:
                        loadout.add_strength_potion()
                        coins -= 300
                        save_game(coins, loadout, Current_profile_id)
                        shop_message = "You bought a strength potion"
                    else:
                        shop_message = "You brokey! You don't have enough coins"
                    shop_message_timer = 30

                if event.key == pygame.K_ESCAPE:
                    mode = "menu"

            if mode == "keybinds":
                if keybind_selecting is None:
                    if event.key == pygame.K_1:
                        keybind_selecting = "use_health_potion"
                    if event.key == pygame.K_2:
                        keybind_selecting = "use_strength_potion"
                    if event.key == pygame.K_3:
                        keybind_selecting = "open_shop"
                    if event.key == pygame.K_4:
                        keybind_selecting = "open_backpack"
                    if event.key == pygame.K_5:
                        keybind_selecting = "use_bomb"
                    if event.key == pygame.K_ESCAPE:
                        save_keybinds(keybinds, Current_profile_id)
                        mode = "menu"
                else:
                    keybinds[keybind_selecting] = event.key
                    keybind_selecting = None

            if mode == "slut" and event.key == pygame.K_SPACE:
                restart()



        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "keybinds" and keybind_selecting is not None:
                keybinds[keybind_selecting] = event.button
                keybind_selecting = None

            if event.button == 1 and mode == "menu":
                if cogwheel_rect.collidepoint(event.pos):
                    mode = "keybinds"
            if event.button == 1 and mode == "game":
                missiles.append(Missil(Player.rect.center, event.pos))
            if event.button == keybinds["use_bomb"] and mode == "game":
                if bomb_cooldown == 0:
                    if loadout.use_bomb():
                        enemies.clear()
                        explosion_size = 10
                        bomb_cooldown = 600

def update():
    global mode, kill_count, Life, explosion_size, coin_message_timer, health_potion_cooldown, strength_potion_cooldown, bomb_cooldown, shop_message_timer, potion_message_timer
    if explosion_size > 0:
        explosion_size += 30
        if explosion_size > WIDTH * 1.5:
            explosion_size = 0

    if coin_message_timer > 0:
        coin_message_timer -= 1
    if shop_message_timer > 0:
        shop_message_timer -= 1
    if potion_message_timer > 0:
        potion_message_timer -= 1

    if health_potion_cooldown > 0:
        health_potion_cooldown -= 1
    if strength_potion_cooldown > 0:
        strength_potion_cooldown -= 1
    if bomb_cooldown > 0:
        bomb_cooldown -= 1
    if mode != "game":
        return

    # enemies move towards the player
    for f in enemies:
        f.move_toward(Player)

    # enemies-player collision
    for f in list(enemies):
        if f.rect.colliderect(Player.rect):
            enemies.remove(f)
            Life -= 1
            if Life <= 0:
                mode = "slut"
                save_game(coins, loadout, Current_profile_id)
                save_score(Current_profile_id, coins_this_run, level, degree_of_difficulty, datetime.date.today().isoformat())

    # move missile
    for m in list(missiles):
        m.update()
        if m.utanfor_skarm():
            missiles.remove(m)

    # missile-enemies collision
    for m in list(missiles):
        for f in list(enemies):
            if m.rect.colliderect(f.rect):
                # roll to see if enemy dodges
                if random.randint(1, MaxDodgeChance) <= enemyBlockChance:
                    # enemy dodged and the missile disapear
                    missiles.remove(m)
                    break
                # enemy didn´t dodge so it takes damage
                f.hp -= shoot_power
                if f.hp <= 0:
                    enemies.remove(f)
                    kill_count += 1
                missiles.remove(m)
                break

    # new wave
    if len(enemies) == 0:
        new_enemy_hp = 3
        if kill_count > 1:
            new_enemy_hp = level_up()
            kill_count = 0
        spawn_enemies(new_enemy_hp)



def draw():
    screen.blit(background_pic, (0, 0))

    if mode == "Login":
        ui.label_select_profile.draw(screen)
        profiles = get_profiles()
        for i, (profile_id, name) in enumerate(profiles):
            ui.render_text(screen, ui.font, str(i + 1) + " - " + name, (255, 255, 255), (300, 200 + i * 50))
        ui.render_text(screen, ui.font, "N - New profile", (255, 215, 0), (300, 200 + len(profiles) * 50))
        if creating_profile:
            ui.label_name_input.update("Name: " + login_input)
            ui.label_name_input.draw(screen)
            ui.label_enter_confirm.draw(screen)

    elif mode == "menu":
        ui.label_choose_difficulty.draw(screen)
        ui.label_easy.draw(screen)
        ui.label_medium.draw(screen)
        ui.label_hard.draw(screen)
        ui.label_insane.draw(screen)
        screen.blit(Shop_pic, Shop_pic.get_rect(center=(225, 50)))
        screen.blit(cogwheel_pic, cogwheel_rect)
        ui.label_shop_key.update(pygame.key.name(keybinds["open_shop"]).upper())
        ui.label_shop_key.draw(screen)
        screen.blit(Backpack_pic, Backpack_pic.get_rect(center=(400, 50)))
        ui.label_backpack_key.update(pygame.key.name(keybinds["open_backpack"]).upper())
        ui.label_backpack_key.draw(screen)
        ui.label_key_settings_hint.draw(screen)
        ui.label_leaderboard_hint.draw(screen)

    elif mode == "leaderboard":
        screen.fill((0, 0, 0))
        ui.label_leaderboard_title.draw(screen)
        ui.label_esc_back.draw(screen)
        scores = load_scores()
        y = 120
        for i, (name, score_coins) in enumerate(scores):
            ui.render_text(screen, ui.font, str(i + 1) + ". " + name + " - " + str(score_coins) + " coins", (255, 255, 255), (20, y), centered=False)
            y += 35

    elif mode == "shop":
        ui.label_shop_title.draw(screen)
        ui.label_bomb_item.draw(screen)
        ui.label_health_item.draw(screen)
        ui.label_strength_item.draw(screen)
        ui.label_leave_shop.draw(screen)
        ui.label_bomb_price.draw(screen)
        ui.label_health_price.draw(screen)
        ui.label_strength_price.draw(screen)
        if shop_message_timer > 0:
            ui.label_shop_message.update(shop_message)
            ui.label_shop_message.draw(screen)

    elif mode == "Backpack":
        ui.label_bomb_count.update("You have " + str(len(loadout.bombs)) + " bombs!")
        ui.label_health_count.update("You have " + str(len(loadout.health_potions)) + " health potions!")
        ui.label_strength_count.update("You have " + str(len(loadout.strength_potions)) + " strength potions!")
        ui.label_coin_count.update("You have " + str(coins) + " coins!")
        ui.label_bomb_count.draw(screen)
        ui.label_health_count.draw(screen)
        ui.label_strength_count.draw(screen)
        ui.label_leave_backpack.draw(screen)
        ui.label_coin_count.draw(screen)

    elif mode == "keybinds":
        ui.label_key_settings_title.draw(screen)
        ui.label_bind_health.update("1 - Use Health Potion: " + bind_name(keybinds["use_health_potion"]))
        ui.label_bind_strength.update("2 - Use Strength Potion: " + bind_name(keybinds["use_strength_potion"]))
        ui.label_bind_shop.update("3 - Open Shop:     " + bind_name(keybinds["open_shop"]))
        ui.label_bind_backpack.update("4 - Open Backpack: " + bind_name(keybinds["open_backpack"]))
        ui.label_bind_bomb.update("5 - Use Bomb:      " + bind_name(keybinds["use_bomb"]))
        ui.label_bind_health.draw(screen)
        ui.label_bind_strength.draw(screen)
        ui.label_bind_shop.draw(screen)
        ui.label_bind_backpack.draw(screen)
        ui.label_bind_bomb.draw(screen)
        ui.label_save_back.draw(screen)
        if keybind_selecting:
            ui.label_waiting.update("Press any key for: " + keybind_selecting)
            ui.label_waiting.draw(screen)

    elif mode == "slut":
        scores = load_scores()
        rank = sum(1 for s in scores if s[1] > coins_this_run) + 1
        ui.label_game_over.draw(screen)
        ui.label_score.update("Coins this run: " + str(coins_this_run))
        ui.label_score.draw(screen)
        ui.label_rank.update("Rank: #" + str(rank) + " of " + str(len(scores)))
        ui.label_rank.draw(screen)
        ui.label_press_space.draw(screen)

    else:
        Player.draw()
        for f in enemies:
            f.draw()
        for m in missiles:
            m.draw()
        ui.label_life.update("Life: " + str(Life))
        ui.label_coins_run.update("Coins this run: " + str(coins_this_run))
        ui.label_level.update("Level: " + str(level))
        ui.label_life.draw(screen)
        ui.label_coins_run.draw(screen)
        ui.label_level.draw(screen)
        if potion_message_timer > 0:
            ui.label_potion_message.update(potion_message)
            ui.label_potion_message.draw(screen)
        for i in range(len(loadout.health_potions)):
            screen.blit(potion_pic, (10 + i * 40, 530))
        for i in range(len(loadout.strength_potions)):
            screen.blit(Strength_potion_pic, (10 + i * 40, 490))
        for i in range(len(loadout.bombs)):
            screen.blit(bomb_pic, (10 + i * 40, 450))
        if explosion_size > 0:
            scaled = pygame.transform.scale(explosion_pic, (explosion_size, explosion_size))
            screen.blit(scaled, scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        if coin_message_timer > 0:
            ui.label_coin_message.update(coin_message)
            ui.label_coin_message.draw(screen)



# start game
running = True
while running:
    handle_input()
    update()
    draw()
    pygame.display.flip()
    clock.tick(30)