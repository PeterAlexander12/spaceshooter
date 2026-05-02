import pygame
import random
import math

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ladda bilder
spelare_bild = pygame.image.load("images/spelare.png").convert_alpha()
fiende_bild = pygame.image.load("images/fiende.png").convert_alpha()
fiende_bild = pygame.transform.scale(fiende_bild, (50, 50))
spelare_bild = pygame.transform.scale(spelare_bild, (50, 50))
missil_bild = pygame.image.load("images/bullet.png").convert_alpha()
bakgrund_bild = pygame.image.load("images/background.png").convert()

font = pygame.font.Font(None, 40)
stor_font = pygame.font.Font(None, 60)


class Spelare:
    def __init__(self):
        self.rect = pygame.Rect(300, 300, spelare_bild.get_width(), spelare_bild.get_height())
        self.rect.center = (300, 300)

    def draw(self):
        screen.blit(spelare_bild, self.rect)


class Fiende:
    def __init__(self, base_hp, base_speed):
        x = random.choice([random.randint(-200, 0), random.randint(600, 800)])
        y = random.choice([random.randint(-200, 0), random.randint(600, 800)])
        self.rect = pygame.Rect(x, y, fiende_bild.get_width(), fiende_bild.get_height())
        self.rect.center = (x, y)

        boost = random.choice(["speed", "hp"])
        if boost == "speed":
            self.hp = base_hp
            self.max_hp = base_hp
            self.speed = base_speed + 1
        else:
            self.hp = base_hp + 2
            self.max_hp = base_hp + 2
            self.speed = base_speed

    def move_toward(self, target):
        if self.rect.centerx < target.rect.centerx:
            self.rect.x += self.speed
        if self.rect.centerx > target.rect.centerx:
            self.rect.x -= self.speed
        if self.rect.centery < target.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > target.rect.centery:
            self.rect.y -= self.speed

    def draw(self):
        screen.blit(fiende_bild, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x, self.rect.y - 10, 50, 15))
        pygame.draw.rect(screen, (144, 238, 144), (self.rect.x, self.rect.y - 10, 50 * (self.hp / self.max_hp), 15))

class Missil:
    def __init__(self, start_pos, target_pos):
        self.rect = missil_bild.get_rect(center=start_pos)
        x_led = target_pos[0] - start_pos[0]
        y_led = target_pos[1] - start_pos[1]
        avstand = math.sqrt(x_led ** 2 + y_led ** 2)
        hastighet = 3
        self.x_hastighet = x_led / avstand * hastighet
        self.y_hastighet = y_led / avstand * hastighet
        self.angle = math.degrees(math.atan2(-y_led, x_led)) - 90

    def update(self):
        self.rect.x += self.x_hastighet
        self.rect.y += self.y_hastighet

    def utanfor_skarm(self):
        return self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT

    def draw(self):
        roterad = pygame.transform.rotate(missil_bild, self.angle)
        screen.blit(roterad, roterad.get_rect(center=self.rect.center))

class Loadout:
    def __init__(self):
        self.potions = []

    def add_potion(self, potion):
        self.potions.append(potion)

    def get_potion(self):
        if len(self.potions) > 0:
            potion = self.potions.pop(0)
            # apply potion effect here later
            return potion
        return None

# spelvariabler
spelare = Spelare()
loadout = Loadout()
loadout.add_potion("health")
loadout.add_potion("health")
loadout.add_potion("health")
fiender = []
missiler = []
liv = 3
xp = 0
kill_count = 0
level = 1
shoot_power = 1
enemy_speed = 1
antal_fiender = 5
lage = "meny"
vald_svarighetsgrad = None


def spawn_enemies(hp):
    for i in range(antal_fiender):
        fiender.append(Fiende(hp, enemy_speed))


def level_up():

    global level, liv, shoot_power, enemy_speed
    level += 1
    upgradering = random.choice(["extra_liv", "shoot_power"])
    if upgradering == "extra_liv":
        liv += 1
        enemy_speed += 1
    if upgradering == "shoot_power":
        shoot_power += 1

    return 3 + level


def restart():
    global liv, lage, fiender, missiler, xp, kill_count, level, shoot_power, enemy_speed
    liv = 3
    lage = "meny"
    xp = 0
    kill_count = 0
    level = 1
    shoot_power = 1
    enemy_speed = 1
    spelare.rect.center = (300, 300)
    missiler = []
    fiender = []
    spawn_enemies(3)


def handle_input():
    global running, lage, vald_svarighetsgrad, liv, enemy_speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if lage == "meny":
                if event.key == pygame.K_1:
                    vald_svarighetsgrad = "easy"
                    lage = "spel"
                    liv = 5
                    spawn_enemies(3)
                if event.key == pygame.K_2:
                    vald_svarighetsgrad = "medium"
                    lage = "spel"
                    spawn_enemies(3)
                if event.key == pygame.K_3:
                    vald_svarighetsgrad = "hard"
                    lage = "spel"
                    enemy_speed = 2
                    spawn_enemies(3)
                if event.key == pygame.K_4:
                    vald_svarighetsgrad = "insane"
                    lage = "spel"
                    liv = 1
                    enemy_speed = 2
                    spawn_enemies(3)
            if lage == "slut" and event.key == pygame.K_SPACE:
                restart()
            if lage == "spel" and event.key == pygame.K_SPACE:
                potion = loadout.get_potion()
                if potion == "health":
                    liv += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and lage == "spel":
                missiler.append(Missil(spelare.rect.center, event.pos))


def update():
    global lage, kill_count, xp, liv
    if lage != "spel":
        return

    # fiender rör sig mot spelaren
    for f in fiender:
        f.move_toward(spelare)

    # fiender-spelare kollision
    for f in list(fiender):
        if f.rect.colliderect(spelare.rect):
            fiender.remove(f)
            liv -= 1
            if liv <= 0:
                lage = "slut"

    # flytta missiler
    for m in list(missiler):
        m.update()
        if m.utanfor_skarm():
            missiler.remove(m)

    # missil-fiender kollision
    for m in list(missiler):
        for f in list(fiender):
            if m.rect.colliderect(f.rect):
                f.hp -= shoot_power
                if f.hp <= 0:
                    fiender.remove(f)
                    kill_count += 1
                    xp += 100
                missiler.remove(m)
                break

    # ny våg
    if len(fiender) == 0:
        new_enemy_hp = 3
        if kill_count > 14:
            new_enemy_hp = level_up()
            kill_count = 0
        spawn_enemies(new_enemy_hp)


def draw():
    screen.blit(bakgrund_bild, (0, 0))

    if lage == "meny":
        screen.blit(stor_font.render("Välj svårighetsgrad", True, (255, 255, 255)), stor_font.render("Välj "
                                                                                                     "svårighetsgrad", True, (255, 255, 255)).get_rect(center=(300, 150)))
        screen.blit(font.render("1 - Easy", True, (0, 255, 0)), font.render("1 - Easy", True, (0, 255, 0)).get_rect(center=(300, 250)))
        screen.blit(font.render("2 - Medium", True, (255, 255, 0)), font.render("2 - Medium", True, (255, 255, 0)).get_rect(center=(300, 300)))
        screen.blit(font.render("3 - Hard", True, (255, 165, 0)), font.render("3 - Hard", True, (255, 165, 0)).get_rect(center=(300, 350)))
        screen.blit(font.render("4 - Insane", True, (255, 0, 0)), font.render("4 - Insane", True, (255, 0, 0)).get_rect(center=(300, 400)))
    elif lage == "slut":
        text1 = stor_font.render("Game Over!", True, (255, 0, 0))
        text2 = font.render("Tryck mellanslag för att starta om", True, (255, 255, 255))
        screen.blit(text1, text1.get_rect(center=(300, 250)))
        screen.blit(text2, text2.get_rect(center=(300, 320)))
    else:
        spelare.draw()
        for f in fiender:
            f.draw()
        for m in missiler:
            m.draw()
        screen.blit(font.render("Liv: " + str(liv), True, (255, 255, 255)), (10, 10))
        screen.blit(font.render("XP: " + str(xp), True, (255, 255, 255)), (250, 10))
        screen.blit(font.render("Level: " + str(level), True, (255, 255, 255)), (10, 570))


# starta spelet
running = True
while running:
    handle_input()
    update()
    draw()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()