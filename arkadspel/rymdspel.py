from xml.etree.ElementPath import xpath_tokenizer

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

# spelare
spelare = pygame.Rect(300, 300, spelare_bild.get_width(), spelare_bild.get_height())
spelare.center = (300, 300)

antal_fiender = 5
liv = 3
lage = "spel"
xp = 0

# skapa fiender
fiende = []


def spawn_enemies():
    for i in range(antal_fiender):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = pygame.Rect(x, y, fiende_bild.get_width(), fiende_bild.get_height())
        r.center = (x, y)
        fiende.append(r)

missiler = []  # each missile: {"rect": Rect, "x_hastighet": float, "y_hastighet": float, "angle": float}

font = pygame.font.Font(None, 40)
stor_font = pygame.font.Font(None, 60)
spawn_enemies()

def restart():
    global liv, lage, fiende, missiler
    liv = 3
    lage = "spel"
    spelare.center = (300, 300)
    missiler = []
    fiende = []
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
            if lage == "vunnit" and event.key == pygame.K_ESCAPE:
                running = False
            if lage == "vunnit" and event.key == pygame.K_SPACE:
                fiende.clear()
                missiler.clear()
                spawn_enemies()
                lage = "spel"

    # 2. update
    if lage == "spel":
        # fiender rör sig mot spelaren
        for f in fiende:
            if f.centerx < spelare.centerx:
                f.x += 1
            if f.centerx > spelare.centerx:
                f.x -= 1
            if f.centery < spelare.centery:
                f.y += 1
            if f.centery > spelare.centery:
                f.y -= 1

        # fiende-spelare kollision
        for f in list(fiende):
            if f.colliderect(spelare):
                fiende.remove(f)
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

        # missil-fiende kollision
        for m in list(missiler):
            for f in list(fiende):
                if m["rect"].colliderect(f):
                    missiler.remove(m)
                    fiende.remove(f)
                    xp += 100
                    break
        
        if len(fiende) == 0:
            lage = "vunnit"

    # 3. draw
    screen.fill((0, 0, 0))

    if lage == "vunnit":
        text1 = stor_font.render("Alla fiender är döda!", True, (0, 255, 0))
        text2 = font.render("Tryck mellanslag för ny våg", True, (255, 255, 255))
        text3 = font.render("Tryck ESC för att avsluta", True, (255, 255, 255))
        screen.blit(text1, text1.get_rect(center=(300, 250)))
        screen.blit(text2, text2.get_rect(center=(300, 320)))
        screen.blit(text3, text3.get_rect(center=(300, 370)))
    elif lage == "slut":
        text1 = stor_font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Tryck mellanslag för att starta om", True, (255, 255, 255))
        screen.blit(text1, text1.get_rect(center=(300, 250)))
        screen.blit(text2, text2.get_rect(center=(300, 320)))
    else:
        screen.blit(spelare_bild, spelare)
        for f in fiende:
            screen.blit(fiende_bild, f)
        for m in missiler:
            roterad = pygame.transform.rotate(missil_bild, m["angle"])
            screen.blit(roterad, roterad.get_rect(center=m["rect"].center))
        liv_text = font.render("Liv: " + str(liv), True, (255, 255, 255))
        screen.blit(liv_text, (10, 10))
        xp_text = font.render("XP: " + str(liv), True, (255, 255, 255))
        screen.blit(xp_text, (250, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
