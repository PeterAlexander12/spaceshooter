import pygame
import random
import math

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ladda bilder
spelare_bild = pygame.image.load("images/ball.png").convert_alpha()
fiende_bild = pygame.image.load("images/bear.png").convert_alpha()
missil_bild = pygame.image.load("images/bullet.png").convert_alpha()
bakgrund_bild = pygame.image.load("images/background.png").convert()

# spelare
spelare = pygame.Rect(300, 300, spelare_bild.get_width(), spelare_bild.get_height())
spelare.center = (300, 300)

antal_fiender = 5
liv = 3
lage = "spel"
xp = 0
kill_count = 0
level = 1
shoot_power = 1

# skapa fiender
fiender = []


def spawn_enemies():
    for i in range(antal_fiender):
        x = random.choice([random.randint(-200, 0), random.randint(600, 800)])
        y = random.choice([random.randint(-200, 0), random.randint(600, 800)])
        r = pygame.Rect(x, y, fiende_bild.get_width(), fiende_bild.get_height())
        r.center = (x, y)
        fiender.append({"rect": r, "hp": 3})

def level_up():
    global level
    global liv
    global shoot_power
    level += 1
    upgradering = random.choice(["extra_liv", "shoot_power"])
    if upgradering == "extra_liv":
        liv += 1
    if upgradering == "shoot_power":
        shoot_power += 1

missiler = []  # each missile: {"rect": Rect, "x_hastighet": float, "y_hastighet": float, "angle": float}

font = pygame.font.Font(None, 40)
stor_font = pygame.font.Font(None, 60)
spawn_enemies()

def restart():
    global liv, lage, fiender, missiler
    liv = 3
    lage = "spel"
    spelare.center = (300, 300)
    missiler = []
    fiender = []
    spawn_enemies()

# game loop
running = True
while running:
    # 1. handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and lage == "spel":
                mx, my = event.pos
                x_led = mx - spelare.centerx
                y_led = my - spelare.centery
                avstand = math.sqrt(x_led ** 2 + y_led ** 2)
                if avstand > 0:
                    hastighet = 3
                    missil_rect = missil_bild.get_rect(center=spelare.center)
                    angle = math.degrees(math.atan2(-y_led, x_led)) - 90
                    missiler.append({
                        "rect": missil_rect,
                        "x_hastighet": x_led / avstand * hastighet,
                        "y_hastighet": y_led / avstand * hastighet,
                        "angle": angle
                    })

        if event.type == pygame.KEYDOWN:
            if lage == "slut" and event.key == pygame.K_SPACE:
                restart()

    # 2. update
    if lage == "spel":
        # fiender rör sig mot spelaren
        for f in fiender:
            if f["rect"].centerx < spelare.centerx:
                f["rect"].x += 1
            if f["rect"].centerx > spelare.centerx:
                f["rect"].x -= 1
            if f["rect"].centery < spelare.centery:
                f["rect"].y += 1
            if f["rect"].centery > spelare.centery:
                f["rect"].y -= 1

        # fiender-spelare kollision
        for f in list(fiender):
            if f["rect"].colliderect(spelare):
                fiender.remove(f)
                liv -= 1
                if liv <= 0:
                    lage = "slut"

        # flytta missiler
        i = 0
        while i < len(missiler):
            m = missiler[i]
            m["rect"].x += m["x_hastighet"]
            m["rect"].y += m["y_hastighet"]

            if m["rect"].x < 0 or m["rect"].x > WIDTH or m["rect"].y < 0 or m["rect"].y > HEIGHT:
                missiler.pop(i)
            else:
                i += 1

        # missil-fiender kollision
        for m in list(missiler):
            for f in list(fiender):
                if m["rect"].colliderect(f["rect"]):
                    f["hp"] -= shoot_power
                    if f["hp"] <= 0:
                        fiender.remove(f)
                        kill_count += 1
                        xp += 100
                    missiler.remove(m)
                    
                    break
        
        if len(fiender) == 0:
            if kill_count > 14:
                level_up()
                kill_count = 0
            spawn_enemies()

    # 3. draw
    screen.blit(bakgrund_bild, (0, 0))

    if lage == "slut":
        text1 = stor_font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Tryck mellanslag för att starta om", True, (255, 255, 255))
        screen.blit(text1, text1.get_rect(center=(300, 250)))
        screen.blit(text2, text2.get_rect(center=(300, 320)))
    else:
        screen.blit(spelare_bild, spelare)
        for f in fiender:
            screen.blit(fiende_bild, f["rect"])
        for m in missiler:
            roterad = pygame.transform.rotate(missil_bild, m["angle"])
            screen.blit(roterad, roterad.get_rect(center=m["rect"].center))
        liv_text = font.render("Liv: " + str(liv), True, (255, 255, 255))
        screen.blit(liv_text, (10, 10))
        xp_text = font.render("XP: " + str(xp), True, (255, 255, 255))
        screen.blit(xp_text, (250, 10))
        level_text = font.render("Level: " + str(level), True, (255, 255, 255))
        screen.blit(level_text, (10, 570))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
