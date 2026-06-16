import pygame, sys
import random
import math

from pygame.cursors import sizer_x_strings

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
Backpack_pic = pygame.image.load("images/backpack.png").convert_alpha()
Backpack_pic = pygame.transform.scale(Backpack_pic, (100, 100))
StrengthPotion_pic = pygame.image.load("images/strength_potion.png").convert_alpha()
StrengthPotion_pic = pygame.transform.scale(StrengthPotion_pic, (30, 30))

font = pygame.font.Font(None, 40)
stor_font = pygame.font.Font(None, 65)


from player import Player

from enemy import Enemy

from missil import Missil

from loadout import Loadout
from save import save_game, load_game

# game variables
Player = Player(screen, player_pic)
loadout = Loadout()
loadout.add_potion("health")
loadout.add_potion("health")
loadout.add_potion("health")
loadout.add_bomb()
loadout.add_bomb()
explosion_size = 0
missiles = []
Life = 3
bonus_coins = 10
bomb_price = 5000
potion_price = 300
kill_count = 0
level = 1
# enemies
number_of_enemies = 5
enemies = []
# for upgrades
shoot_power = 1
enemy_speed = 1
# Block
enemyBlockChance = 1
MaxDodgeChance = 20
blocked_message = ""
blocked_message_timer = 0
mode = "menu"
degree_of_difficulty = None
# coin
coin_message = ""
coin_message_timer = 0
coins_this_run = 0
# cooldown
potion_cooldown = 0
bomb_cooldown = 0


coins = load_game(loadout)


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
    global Life, mode, enemies, missiles, kill_count, level, shoot_power, enemy_speed, coins_this_run
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




def handle_input():
    global running, mode, degree_of_difficulty, Life, enemy_speed, explosion_size, number_of_enemies, potion_cooldown, bomb_cooldown
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if mode == "menu":
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
                    number_of_enemies += 1
                if event.key == pygame.K_3:
                    degree_of_difficulty = "hard"
                    mode = "game"
                    enemy_speed = 2
                    spawn_enemies(3)
                    number_of_enemies += 2
                    Life = 2
                if event.key == pygame.K_4:
                    degree_of_difficulty = "insane"
                    mode = "game"
                    Life = 1
                    enemy_speed = 3
                    spawn_enemies(3)
                    number_of_enemies += 3

                if event.key == pygame.K_ESCAPE:
                    mode = "menu"
                if event.key == pygame.K_s:
                    mode = "shop"
                if event.key == pygame.K_e:
                    mode = "Backpack"

            if mode == "game":

                if event.key == pygame.K_SPACE:
                    if potion_cooldown == 0:
                        potion = loadout.get_potion()
                        if potion == "health":
                            Life += 1
                        potion_cooldown = 150

                if event.key == pygame.K_ESCAPE:
                    mode = "menu"
                    enemies.clear()

            if mode == "Backpack":
                if event.key == pygame.K_ESCAPE:
                    mode = "menu"

            if mode == "shop":
                global coins
                if event.key == pygame.K_2:
                    if coins > 499:
                        loadout.add_potion("health")
                        coins -= 500
                        save_game()
                if event.key == pygame.K_1:
                    if coins > 4999:
                        loadout.add_bomb()
                        coins -= 5000
                        save_game()
                if event.key == pygame.K_ESCAPE:
                    mode = "menu"

            if mode == "slut" and event.key == pygame.K_SPACE:
                restart()



        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and mode == "game":
                missiles.append(Missil(Player.rect.center, event.pos))
            if event.button == 3 and mode == "game":
                if bomb_cooldown == 0:
                    if loadout.use_bomb():
                        enemies.clear()
                        explosion_size = 10
                        bomb_cooldown = 600

def update():
    global mode, kill_count, Life, explosion_size, coin_message_timer, potion_cooldown, blocked_message_timer
    if explosion_size > 0:
        explosion_size += 30
        if explosion_size > WIDTH * 1.5:
            explosion_size = 0

    if coin_message_timer > 0:
        coin_message_timer -= 1
    if potion_cooldown > 0:
        potion_cooldown -= 1
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
                save_game()

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
                    blocked_message_timer = 15
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

    if mode == "menu":
        screen.blit(stor_font.render("Choose difficulty", True, (255, 255, 255)), stor_font.render("Choose " "svårighetsgrad", True, (255, 255, 255)).get_rect(center=(370, 150)))
        screen.blit(font.render("1 - Easy", True, (0, 255, 0)), font.render("1 - Easy", True, (0, 255, 0)).get_rect(center=(300, 250)))
        screen.blit(font.render("2 - Medium", True, (255, 255, 0)), font.render("2 - Medium", True, (255, 255, 0)).get_rect(center=(300, 300)))
        screen.blit(font.render("3 - Hard", True, (255, 165, 0)), font.render("3 - Hard", True, (255, 165, 0)).get_rect(center=(300, 350)))
        screen.blit(font.render("4 - Insane", True, (255, 0, 0)), font.render("4 - Insane", True, (255, 0, 0)).get_rect(center=(300, 400)))
        screen.blit(Shop_pic, Shop_pic.get_rect(center=(225, 50)))
        screen.blit(stor_font.render("S", True, (0, 255, 0)), stor_font.render("S", True, (0, 255, 0)).get_rect(center=(225, 110)))
        screen.blit(Backpack_pic, Backpack_pic.get_rect(center=(400, 50)))
        screen.blit(stor_font.render("E", True, (0, 255, 0)),stor_font.render("E", True, (0, 255, 0)).get_rect(center=(395, 110)))

    elif mode == "shop":
        t_Title = stor_font.render("shop", True, (0, 255, 0))
        t_Bomb = font.render("1 - Bomb", True, (255, 255, 255))
        t_Potion = font.render("2 - Potion", True, (255, 255, 255))
        t_Leave_shop = font.render("Esc - Leave shop", True, (178, 34, 34))

        t_bomb_price = font.render(str(bomb_price) + " coins", True, (255, 255, 255))
        t_potion_price = font.render(str(potion_price) + " coins", True, (255, 255, 255))

        screen.blit(t_Title, t_Title.get_rect(center=(250, 200)))
        screen.blit(t_Bomb, (100, 250))
        screen.blit(t_Potion, (100, 300))
        screen.blit(t_Leave_shop, t_Leave_shop.get_rect(center=(120, 30)))
        screen.blit(t_bomb_price, t_bomb_price.get_rect(center=(400, 265)))
        screen.blit(t_potion_price, t_potion_price.get_rect(center=(400, 315)))

    elif mode == "Backpack":
        t_Bomb_count = font.render("You have " + str(len(loadout.bombs)) + " bombs!", True, (255, 255, 255))
        t_Potion_count = font.render("You have " + str(len(loadout.potions)) + " potions!", True, (255, 255, 255))
        t_Leave_backpack = font.render("Esc - Leave backpack", True, (178, 34, 34))
        t_coin_count = font.render("You have " + str(coins) + " coins!", True, (255, 215, 0))

        screen.blit(t_Bomb_count, (200, 250))
        screen.blit(t_Potion_count, (200, 300))
        screen.blit(t_Leave_backpack, t_Leave_backpack.get_rect(center=(150, 30)))
        screen.blit(t_coin_count, (150, 550))

    elif mode == "slut":
        text1 = stor_font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Press space too go to the menu ", True, (255, 255, 255))
        screen.blit(text1, text1.get_rect(center=(300, 250)))
        screen.blit(text2, text2.get_rect(center=(300, 320)))
    else:
        Player.draw()
        for f in enemies:
            f.draw()
        for m in missiles:
            m.draw()
        screen.blit(font.render("Life: " + str(Life), True, (255, 255, 255)), (10, 10))
        screen.blit(font.render("Coins this run: " + str(coins_this_run), True, (255, 215, 0)), (200, 10))
        screen.blit(font.render("Level: " + str(level), True, (255, 255, 255)), (10, 570))
        for i in range(len(loadout.potions)):
            screen.blit(potion_pic, (10 + i * 40, 530))
        for i in range(len(loadout.bombs)):
            screen.blit(bomb_pic, (10 + i * 40, 490))
        if explosion_size > 0:
            scaled = pygame.transform.scale(explosion_pic, (explosion_size, explosion_size))
            screen.blit(scaled, scaled.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        # draw coin message while timer is running
        if coin_message_timer > 0:
            t_coin = font.render(coin_message, True, (255, 215, 0))
            screen.blit(t_coin, t_coin.get_rect(center=(WIDTH // 2, 80)))
        # draw blocked message while timer is running
        #if blocked_message_timer > 0:
        #t_blocked = font.render(blocked_message, True, (255, 255, 255))
        #screen.blit(t_blocked, t_blocked.get_rect())



# start game
running = True
while running:
    handle_input()
    update()
    draw()
    pygame.display.flip()
    clock.tick(30)