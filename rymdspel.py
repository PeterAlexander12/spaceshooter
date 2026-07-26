import pygame, sys
import random
import datetime

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# load pictures
player_pic = pygame.transform.scale(pygame.image.load("images/spelare.png").convert_alpha(), (50, 50))
enemy_pic = pygame.transform.scale(pygame.image.load("images/fiende.png").convert_alpha(), (50, 50))
potion_pic = pygame.transform.scale(pygame.image.load("images/Red_potion.png").convert_alpha(), (30, 30))
explosion_pic = pygame.image.load("images/nuclear_explosion.png").convert_alpha()
bomb_pic = pygame.transform.scale(explosion_pic, (30, 30))
missile_pic = pygame.image.load("images/bullet.png").convert_alpha()
background_pic = pygame.image.load("images/background.png").convert()
shop_pic = pygame.transform.scale(pygame.image.load("images/shop.png").convert_alpha(), (80, 80))
shop_rect = pygame.Rect(185, 10, 80, 80)
cogwheel_pic = pygame.transform.scale(pygame.image.load("images/cogwheel.png").convert_alpha(), (120, 120))
cogwheel_rect = pygame.Rect(490, 10, 80, 80)
inventory_pic = pygame.transform.scale(pygame.image.load("images/inventory.png").convert_alpha(), (100, 100))
inventory_rect = pygame.Rect(350, 5, 100, 100)
Strength_potion_pic = pygame.transform.scale(pygame.image.load("images/strength_potion.png").convert_alpha(), (30, 30))

from player import Player

from enemy import Enemy

from missil import Missil
from pointy_missile import Pointy_Missile
from loadout import Loadout
from save import save_game, load_game, save_keybinds, get_profiles, create_profile, load_scores, save_score
from keybinds import load_keybinds, bind_name, DEFAULT_KEYBINDS
from gamestate import GameState
import ui

# game variables
Player = Player(screen, player_pic)
gamestate = GameState()
bomb_price = 5000
health_potion_price = 300
strength_potion_price = 400
MaxDodgeChance = 20


def spawn_enemies(hp):
    for i in range(gamestate.number_of_enemies):
        gamestate.enemies.append(Enemy(hp, gamestate.enemy_speed))


def level_up():
    gamestate.level += 1

    if gamestate.degree_of_difficulty == "easy":
        gamestate.coins += gamestate.bonus_coins * gamestate.level
        gamestate.coins_this_run += gamestate.bonus_coins * gamestate.level
    if gamestate.degree_of_difficulty == "medium":
        gamestate.bonus_coins = 20
        gamestate.coins += gamestate.bonus_coins * gamestate.level
        gamestate.coins_this_run += gamestate.bonus_coins * gamestate.level
    if gamestate.degree_of_difficulty == "hard":
        gamestate.bonus_coins = 30
        gamestate.coins += gamestate.bonus_coins * gamestate.level
        gamestate.coins_this_run += gamestate.bonus_coins * gamestate.level
    if gamestate.degree_of_difficulty == "insane":
        gamestate.bonus_coins = 50
        gamestate.coins += gamestate.bonus_coins * gamestate.level
        gamestate.coins_this_run += gamestate.bonus_coins * gamestate.level

    gamestate.coin_message = "+" + str(gamestate.bonus_coins * gamestate.level) + " coins!"
    gamestate.coin_message_timer = 90

    upgrade = random.choice(["extra_Life", "shoot_power"]) # to do after sub menu, add extra upgrade, phace
    if upgrade == "extra_Life":
        gamestate.Life += 1
    if upgrade == "shoot_power":
        gamestate.shoot_power += 1

    enemy_upgrade = random.choice(["enemy_dodge", "enemy_speed"])
    if enemy_upgrade == "enemy_dodge":
        gamestate.enemyBlockChance = min(MaxDodgeChance, gamestate.enemyBlockChance + 1)
    if enemy_upgrade == "enemy_speed":
        gamestate.enemy_speed += 1

    return 3 + gamestate.level


def restart():
    gamestate.Life = 3
    gamestate.mode = "menu"
    gamestate.kill_count = 0
    gamestate.level = 1
    gamestate.shoot_power = 1
    gamestate.enemy_speed = 1
    Player.rect.center = (300, 300)
    gamestate.missiles = []
    gamestate.enemies = []
    gamestate.coins_this_run = 0
    spawn_enemies(3)
    gamestate.bomb_cooldown = 0
    gamestate.health_potion_cooldown = 0
    gamestate.strength_potion_cooldown = 0




def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(gamestate.coins, gamestate.loadout, gamestate.Current_profile_id)
            gamestate.running = False

        if event.type == pygame.KEYDOWN:
            if gamestate.mode == "Login":
                if not gamestate.creating_profile:
                    profiles = get_profiles()
                    for i, (pid, name) in enumerate(profiles):
                        if event.key == pygame.K_1 + i:
                            gamestate.Current_profile_id = pid
                            gamestate.coins = load_game(gamestate.loadout, gamestate.Current_profile_id)
                            gamestate.keybinds = load_keybinds(gamestate.Current_profile_id)
                            gamestate.mode = "menu"
                    if event.key == pygame.K_n:
                        gamestate.creating_profile = True
                else:
                    if event.key == pygame.K_RETURN:
                        if gamestate.login_input.strip():
                            gamestate.Current_profile_id = create_profile(gamestate.login_input.strip())
                            gamestate.coins = load_game(gamestate.loadout, gamestate.Current_profile_id)
                            gamestate.keybinds = load_keybinds(gamestate.Current_profile_id)
                            gamestate.login_input = ""
                            gamestate.creating_profile = False
                            gamestate.mode = "menu"
                    elif event.key == pygame.K_BACKSPACE:
                        gamestate.login_input = gamestate.login_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        gamestate.login_input = ""
                        gamestate.creating_profile = False
                    else:
                        gamestate.login_input += event.unicode

            elif gamestate.mode == "menu":
                if event.key == pygame.K_1:
                    gamestate.degree_of_difficulty = "easy"
                    gamestate.mode = "game"
                    gamestate.Life = 5
                    spawn_enemies(3)
                    gamestate.number_of_enemies -= 1
                if event.key == pygame.K_2:
                    gamestate.degree_of_difficulty = "medium"
                    gamestate.mode = "game"
                    spawn_enemies(3)
                if event.key == pygame.K_3:
                    gamestate.degree_of_difficulty = "hard"
                    gamestate.mode = "game"
                    gamestate.enemy_speed = 2
                    spawn_enemies(3)
                    gamestate.number_of_enemies += 1
                    gamestate.Life = 2
                if event.key == pygame.K_4:
                    gamestate.degree_of_difficulty = "insane"
                    gamestate.mode = "game"
                    gamestate.Life = 1
                    gamestate.enemy_speed = 3
                    spawn_enemies(3)
                    gamestate.number_of_enemies += 2

                if event.key == pygame.K_ESCAPE:
                    gamestate.mode = "menu"
                if event.key == gamestate.keybinds["open_shop"]:
                    gamestate.mode = "shop"
                if event.key == gamestate.keybinds["open_inventory"]:
                    gamestate.mode = "inventory"
                if event.key == pygame.K_k:
                    gamestate.mode = "keybinds"
                if event.key == pygame.K_l:
                    gamestate.mode = "leaderboard"

            # settings
            if gamestate.mode == "settings":
                if event.key == pygame.K_ESCAPE:
                    gamestate.mode = "menu"


            if gamestate.mode == "game":
                if event.key == gamestate.keybinds["use_health_potion"]:
                    if gamestate.health_potion_cooldown == 0:
                        gamestate.loadout.get_health_potion()
                        gamestate.potion_message = "You drank a Health Potion!"
                        gamestate.Life += 1
                        gamestate.health_potion_cooldown = 150
                        gamestate.potion_message_timer = 30

                if event.key == gamestate.keybinds["use_strength_potion"]:
                    if gamestate.strength_potion_cooldown == 0:
                        gamestate.loadout.get_strength_potion()
                        gamestate.potion_message = "You drank a Strength Potion!"
                        gamestate.shoot_power += 1
                        gamestate.strength_potion_cooldown = 150
                        gamestate.potion_message_timer = 30

                if event.key == gamestate.keybinds["use_bomb"]:
                    if gamestate.bomb_cooldown == 0:
                        if gamestate.loadout.use_bomb():
                            gamestate.enemies.clear()
                            gamestate.explosion_size = 10
                            gamestate.bomb_cooldown = 600

                if event.key == pygame.K_ESCAPE:
                    save_game(gamestate.coins, gamestate.loadout, gamestate.Current_profile_id)
                    gamestate.mode = "menu"
                    restart()

            if gamestate.mode == "leaderboard":
                if event.key == pygame.K_ESCAPE:
                    gamestate.mode = "menu"

            if gamestate.mode == "inventory":
                if event.key == pygame.K_ESCAPE:
                    gamestate.mode = "menu"

            if gamestate.mode == "shop":

                if event.key == pygame.K_1:
                    if gamestate.coins > 4999:
                        gamestate.loadout.add_bomb()
                        gamestate.coins -= 5000
                        save_game(gamestate.coins, gamestate.loadout, gamestate.Current_profile_id)
                        gamestate.shop_message = "You bought a bomb"
                    else:
                        gamestate.shop_message = "You brokey! You don't have enough coins!"
                    gamestate.shop_message_timer = 30

                if event.key == pygame.K_2:
                    if gamestate.coins > 299:
                        gamestate.loadout.add_health_potion()
                        gamestate.coins -= 300
                        save_game(gamestate.coins, gamestate.loadout, gamestate.Current_profile_id)
                        gamestate.shop_message = "You bought a health potion"
                    else:
                        gamestate.shop_message = "You brokey! You don´t have enough coins!"
                    gamestate.shop_message_timer = 30

                if event.key == pygame.K_3:
                    if gamestate.coins > 299:
                        gamestate.loadout.add_strength_potion()
                        gamestate.coins -= 300
                        save_game(gamestate.coins, gamestate.loadout, gamestate.Current_profile_id)
                        gamestate.shop_message = "You bought a strength potion"
                    else:
                        gamestate.shop_message = "You brokey! You don't have enough coins!"
                    gamestate.shop_message_timer = 30

                if event.key == pygame.K_ESCAPE:
                    gamestate.mode = "menu"

            if gamestate.mode == "keybinds":
                if gamestate.keybind_selecting is None:
                    if event.key == pygame.K_1:
                        gamestate.keybind_selecting = "use_health_potion"
                    if event.key == pygame.K_2:
                        gamestate.keybind_selecting = "use_strength_potion"
                    if event.key == pygame.K_3:
                        gamestate.keybind_selecting = "open_shop"
                    if event.key == pygame.K_4:
                        gamestate.keybind_selecting = "open_inventory"
                    if event.key == pygame.K_5:
                        gamestate.keybind_selecting = "use_bomb"
                    if event.key == pygame.K_ESCAPE:
                        save_keybinds(gamestate.keybinds, gamestate.Current_profile_id)
                        gamestate.mode = "settings"
                else:
                    gamestate.keybinds[gamestate.keybind_selecting] = event.key
                    gamestate.keybind_selecting = None

            if gamestate.mode == "slut" and event.key == pygame.K_SPACE:
                restart()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if gamestate.mode == "keybinds" and gamestate.keybind_selecting is not None:
                gamestate.keybinds[gamestate.keybind_selecting] = event.button
                gamestate.keybind_selecting = None

            if event.button == 1 and gamestate.mode == "menu":

                # settings
                if cogwheel_rect.collidepoint(event.pos):
                    gamestate.mode = "settings"

                # leaderboard
                if ui.label_leaderboard_hint.rect.collidepoint(event.pos):
                    gamestate.mode = "leaderboard"

                # shop
                if shop_rect.collidepoint(event.pos):
                    gamestate.mode = "shop"

                # inventory
                if inventory_rect.collidepoint(event.pos):
                    gamestate.mode = "inventory"

                # difficulty
                if ui.label_easy.rect.collidepoint(event.pos):
                    gamestate.degree_of_difficulty = "easy"
                    gamestate.mode = "game"
                    gamestate.Life = 5
                    spawn_enemies(3)
                if ui.label_medium.rect.collidepoint(event.pos):
                    gamestate.degree_of_difficulty = "medium"
                    gamestate.mode = "game"
                    spawn_enemies(3)
                if ui.label_hard.rect.collidepoint(event.pos):
                    gamestate.degree_of_difficulty = "hard"
                    gamestate.mode = "game"
                    gamestate.Life = 2
                    spawn_enemies(3)
                if ui.label_insane.rect.collidepoint(event.pos):
                    gamestate.degree_of_difficulty = "insane"
                    gamestate.mode = "game"
                    gamestate.Life = 1
                    spawn_enemies(3)

            if event.button == 1 and gamestate.mode == "game":
                if gamestate.current_bullet == "Pointy Bullet":
                        gamestate.missiles.append(Pointy_Missile(Player.rect.center, event.pos))
                else: # to do, change to elif
                    gamestate.missiles.append(Missil(Player.rect.center, event.pos))

            if event.button == gamestate.keybinds["use_bomb"] and gamestate.mode == "game":
                if gamestate.bomb_cooldown == 0:
                    if gamestate.loadout.use_bomb():
                        gamestate.enemies.clear()
                        gamestate.explosion_size = 10
                        gamestate.bomb_cooldown = 600

            if gamestate.mode == "shop":
                if event.button == 1:
                    if ui.label_leave_shop.rect.collidepoint(event.pos):
                        gamestate.mode = "menu"


            if gamestate.mode == "inventory":
                if event.button == 1:
                    if ui.label_leave_inventory.rect.collidepoint(event.pos):
                        gamestate.mode = "menu"
                    for i,bullet in enumerate(gamestate.owned_bullets):
                        if ui.equip_labels[i].rect.collidepoint(event.pos):
                            if bullet != gamestate.current_bullet:
                                gamestate.current_bullet = bullet


            if event.button == 1 and gamestate.mode == "leaderboard":
                if ui.label_leaderboard_leave.rect.collidepoint(event.pos):
                    gamestate.mode = "menu"

            if event.button == 1 and gamestate.mode == "settings":
                if ui.label_settings_key_settings.rect.collidepoint(event.pos):
                    gamestate.mode = "keybinds"
                if ui.label_settings_logout.rect.collidepoint(event.pos):
                    gamestate.mode = "Login"
                    gamestate.Current_profile_id = None
                    gamestate.loadout = Loadout()

                if ui.label_settings_leave.rect.collidepoint(event.pos):
                    gamestate.mode = "menu"


            if event.button == 1 and gamestate.mode == "keybinds":
                if ui.label_bind_shop.rect.collidepoint(event.pos):
                    gamestate.keybind_selecting = "open_shop"
                if ui.label_bind_inventory.rect.collidepoint(event.pos):
                    gamestate.keybind_selecting = "use_inventory"
                if ui.label_bind_bomb.rect.collidepoint(event.pos):
                    gamestate.keybind_selecting = "use_bomb"
                if ui.label_bind_health.rect.collidepoint(event.pos):
                    gamestate.keybind_selecting = "use_health_potion"
                if ui.label_bind_strength.rect.collidepoint(event.pos):
                    gamestate.keybind_selecting = "use_strength_potion"

                #if ui.label_save_back.rect.collidepoint(event.pos):
                    #save_game(gamestate.keybinds, gamestate.Current_profile_id)
                    #gamestate.mode = "menu"



def update():
    if gamestate.explosion_size > 0:
        gamestate.explosion_size += 30
        if gamestate.explosion_size > WIDTH * 1.5:
            gamestate.explosion_size = 0

    if gamestate.coin_message_timer > 0:
        gamestate.coin_message_timer -= 1
    if gamestate.shop_message_timer > 0:
        gamestate.shop_message_timer -= 1
    if gamestate.potion_message_timer > 0:
        gamestate.potion_message_timer -= 1

    if gamestate.health_potion_cooldown > 0:
        gamestate.health_potion_cooldown -= 1
    if gamestate.strength_potion_cooldown > 0:
        gamestate.strength_potion_cooldown -= 1
    if gamestate.bomb_cooldown > 0:
        gamestate.bomb_cooldown -= 1
    if gamestate.mode != "game":
        return

    # enemies move towards the player
    for f in gamestate.enemies:
        f.move_toward(Player)

    # enemies-player collision
    for f in list(gamestate.enemies):
        if f.rect.colliderect(Player.rect):
            gamestate.enemies.remove(f)
            gamestate.Life -= 1
            if gamestate.Life <= 0:
                gamestate.mode = "slut"
                save_game(gamestate.coins, gamestate.loadout, gamestate.Current_profile_id)
                save_score(gamestate.Current_profile_id, gamestate.coins_this_run, gamestate.level, gamestate.degree_of_difficulty, datetime.date.today().isoformat())

    # move missile
    for m in list(gamestate.missiles):
        m.update()
        if m.utanfor_skarm():
            gamestate.missiles.remove(m)

    # missile-enemies collision
    for m in list(gamestate.missiles):
        for f in list(gamestate.enemies):
            if m.rect.colliderect(f.rect):
                # roll to see if enemy dodges
                if random.randint(1, MaxDodgeChance) <= gamestate.enemyBlockChance:
                    # enemy dodged and the missile disappear
                    gamestate.missiles.remove(m)
                    break
                # enemy didn´t dodge so it takes damage
                f.hp -= gamestate.shoot_power * m.damage
                if f.hp <= 0:
                    gamestate.enemies.remove(f)
                    gamestate.kill_count += 1
                gamestate.missiles.remove(m)
                break

    # new wave
    if len(gamestate.enemies) == 0:
        new_enemy_hp = 3
        if gamestate.kill_count > 1:
            new_enemy_hp = level_up()
            gamestate.kill_count = 0
        spawn_enemies(new_enemy_hp)



def draw():
    screen.blit(background_pic, (0, 0))

    if gamestate.mode == "Login":
        ui.label_select_profile.draw(screen)
        profiles = get_profiles()
        for i, (profile_id, name) in enumerate(profiles):
            ui.render_text(screen, ui.font, str(i + 1) + " - " + name, (255, 255, 255), (300, 200 + i * 50))
        ui.render_text(screen, ui.font, "N - New profile", (255, 215, 0), (300, 200 + len(profiles) * 50))
        if gamestate.creating_profile:
            ui.label_name_input.update("Name: " + gamestate.login_input)
            ui.label_name_input.draw(screen)
            ui.label_enter_confirm.draw(screen)

    elif gamestate.mode == "menu":
        ui.label_choose_difficulty.draw(screen)
        ui.label_easy.draw(screen)
        ui.label_medium.draw(screen)
        ui.label_hard.draw(screen)
        ui.label_insane.draw(screen)
        screen.blit(shop_pic, shop_rect)
        screen.blit(cogwheel_pic, cogwheel_rect)
        ui.label_shop_key.update(pygame.key.name(gamestate.keybinds["open_shop"]).upper())
        ui.label_shop_key.draw(screen)
        screen.blit(inventory_pic, inventory_rect)
        ui.label_inventory_key.update(pygame.key.name(gamestate.keybinds["open_inventory"]).upper())
        ui.label_inventory_key.draw(screen)
        ui.label_leaderboard_hint.draw(screen)

    elif gamestate.mode == "leaderboard":
        screen.fill((0, 0, 0))
        ui.label_leaderboard_title.draw(screen)
        ui.label_leaderboard_leave.draw(screen)
        scores = load_scores()
        y = 120
        for i, (name, score_coins) in enumerate(scores):
            ui.render_text(screen, ui.font, str(i + 1) + ". " + name + " - " + str(score_coins) + " coins", (255, 255, 255), (20, y), centered=False)
            y += 35

    elif gamestate.mode == "shop":
        ui.label_shop_title.draw(screen)
        ui.label_bomb_item.draw(screen)
        ui.label_health_item.draw(screen)
        ui.label_strength_item.draw(screen)
        ui.label_leave_shop.draw(screen)
        ui.label_bomb_price.draw(screen)
        ui.label_health_price.draw(screen)
        ui.label_strength_price.draw(screen)
        if gamestate.shop_message_timer > 0:
            ui.label_shop_message.update(gamestate.shop_message)
            ui.label_shop_message.draw(screen)

    elif gamestate.mode == "inventory":
        screen.fill((0, 0, 0))
        ui.label_inventory_title.draw(screen)
        for i,bullet in enumerate(gamestate.owned_bullets):
            ui.bullet_labels[i].draw(screen)
            if bullet != gamestate.current_bullet:
                ui.equip_labels[i].draw(screen)

        ui.label_bomb_count.update("You have " + str(len(gamestate.loadout.bombs)) + " bombs!")
        ui.label_health_count.update("You have " + str(len(gamestate.loadout.health_potions)) + " health potions!")
        ui.label_strength_count.update("You have " + str(len(gamestate.loadout.strength_potions)) + " strength potions!")
        ui.label_coin_count.update("You have " + str(gamestate.coins) + " coins!")
        ui.label_bomb_count.draw(screen)
        ui.label_health_count.draw(screen)
        ui.label_strength_count.draw(screen)
        ui.label_leave_inventory.draw(screen)
        ui.label_coin_count.draw(screen)

    elif gamestate.mode == "settings":
        screen.fill((0, 0, 0))
        ui.label_settings_title.draw(screen)
        ui.label_settings_logout.draw(screen)
        ui.label_settings_key_settings.draw(screen)
        ui.label_settings_leave.draw(screen)

    elif gamestate.mode == "keybinds":
        ui.label_key_settings_title.draw(screen)
        ui.label_bind_health.update("1 - Use Health Potion: " + bind_name(gamestate.keybinds["use_health_potion"]))
        ui.label_bind_strength.update("2 - Use Strength Potion: " + bind_name(gamestate.keybinds["use_strength_potion"]))
        ui.label_bind_shop.update("3 - Open Shop:     " + bind_name(gamestate.keybinds["open_shop"]))
        ui.label_bind_inventory.update("4 - Open inventory: " + bind_name(gamestate.keybinds["open_inventory"]))
        ui.label_bind_bomb.update("5 - Use Bomb:      " + bind_name(gamestate.keybinds["use_bomb"]))
        ui.label_bind_health.draw(screen)
        ui.label_bind_strength.draw(screen)
        ui.label_bind_shop.draw(screen)
        ui.label_bind_inventory.draw(screen)
        ui.label_bind_bomb.draw(screen)
        ui.label_save_back.draw(screen)
        if gamestate.keybind_selecting:
            ui.label_waiting.update("Press any key for: " + gamestate.keybind_selecting)
            ui.label_waiting.draw(screen)

    elif gamestate.mode == "slut":
        scores = load_scores()
        rank = sum(1 for s in scores if s[1] > gamestate.coins_this_run) + 1
        ui.label_game_over.draw(screen)
        ui.label_score.update("Coins this run: " + str(gamestate.coins_this_run))
        ui.label_score.draw(screen)
        ui.label_rank.update("Rank: #" + str(rank) + " of " + str(len(scores)))
        ui.label_rank.draw(screen)
        ui.label_press_space.draw(screen)

    else:
        Player.draw()
        for f in gamestate.enemies:
            f.draw()
        for m in gamestate.missiles:
            m.draw()
        ui.label_life.update("Life: " + str(gamestate.Life))
        ui.label_coins_run.update("Coins this run: " + str(gamestate.coins_this_run))
        ui.label_level.update("Level: " + str(gamestate.level))
        ui.label_life.draw(screen)
        ui.label_coins_run.draw(screen)
        ui.label_level.draw(screen)
        if gamestate.potion_message_timer > 0:
            ui.label_potion_message.update(gamestate.potion_message)
            ui.label_potion_message.draw(screen)
        for i in range(len(gamestate.loadout.health_potions)):
            screen.blit(potion_pic, (10 + i * 40, 530))
        for i in range(len(gamestate.loadout.strength_potions)):
            screen.blit(Strength_potion_pic, (10 + i * 40, 490))
        for i in range(len(gamestate.loadout.bombs)):
            screen.blit(bomb_pic, (10 + i * 40, 450))
        if gamestate.explosion_size > 0:
            scaled = pygame.transform.scale(explosion_pic, (gamestate.explosion_size, gamestate.explosion_size))
            screen.blit(scaled, scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        if gamestate.coin_message_timer > 0:
            ui.label_coin_message.update(gamestate.coin_message)
            ui.label_coin_message.draw(screen)


# start game
while gamestate.running:
    handle_input()
    update()
    draw()
    pygame.display.flip()
    clock.tick(30)