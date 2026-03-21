import pgzrun
import time
import random

WIDTH = 600
HEIGHT = 700

hp = 100
xp = 0

ship = Actor("ship", (WIDTH/2, HEIGHT-100))
missiles = []
meteors = []
explosions = []
METEOR_IMAGES = ["meteors-1", "meteors-2", "meteors-3", "meteors-4"]
background = Actor("background", (WIDTH, HEIGHT), anchor=("right", "bottom"))
meteor_time = time.time()*1000

mode = "menu"

highscore_file = open("highscore.txt","r")
highscore = int(highscore_file.read())
highscore_file.close()

def draw():
    screen.fill((0,0,0))
    background.draw()
    if mode == "menu":
        screen.draw.text("SPACE SHOOTER", center=(WIDTH/2, 300), fontsize=50)
        screen.draw.text("Tryck space för att spela!", center=(WIDTH/2,350))
        screen.draw.text("Highscore: " + str(highscore), center=(WIDTH/2,370))
    if mode == "game":
        ship.draw()
        for m in missiles:
            m.draw()
        for m in meteors:
            m.draw()
        for e in explosions:
            e.draw()
        screen.draw.text("hp: " + str(hp), (50, 15))
        screen.draw.text("xp: " + str(xp), (50, 30))
    if mode == "end":
        screen.draw.text("Bra jobbat! Du fick: " + str(xp) + " xp", center=(WIDTH/2, HEIGHT/2-10))
        screen.draw.text("Tryck escape för att komma till meny", center=(WIDTH/2, HEIGHT/2+10))

def update():
    global xp, hp, mode, highscore
    update_background()
    if mode == "menu":
        # kod för meny
        if keyboard.space:
            mode = "game"
            xp = 0
            hp = 100
            ship.x = WIDTH/2
    if mode == "game":
        update_missiles()
        update_meteors()
        update_ship()
        xp += 1
        if hp < 0:
            mode = "end"

            if xp > highscore:
                highscore = xp
                highscore_file = open("highscore.txt","w")
                highscore_file.write(str(highscore))
                highscore_file.close()
    if mode == "end":
        if keyboard.escape or keyboard.space:
            mode = "menu"

def update_ship():
    global hp
    if keyboard.left and ship.left > 0:
        ship.x -= 6
    if keyboard.right and ship.right < WIDTH:
        ship.x += 6
    if keyboard.space:
        shoot()
    if ship.collidelist(meteors) != -1:
        hp -= 1

def update_background():
    background.y += 10
    if background.y >= 600+HEIGHT:
        background.y = HEIGHT

def update_meteors():
    global meteor_time
    current_time = time.time()*1000
    if current_time - meteor_time > 600:
        meteor_image = METEOR_IMAGES[random.randint(0,len(METEOR_IMAGES)-1)]
        meteor_x = random.randint(20,WIDTH-20)
        meteor = Actor(meteor_image, (meteor_x, -100))
        meteors.append(meteor)
        meteor_time = time.time()*1000
    for m in meteors:
        m.y += 20
        m.angle -= 4

        if m.y > HEIGHT+100:
            meteors.remove(m)

def remove_explosion():
    explosions.pop()

def update_missiles():
    global xp
    for m in missiles:
        m.y -= 16

        for meteor in meteors:
            if m.colliderect(meteor):
                explosion = Actor("explosion", (m.x, m.top))
                explosions.append(explosion)
                clock.schedule_unique(remove_explosion, 0.02)
                missiles.remove(m)
                meteors.remove(meteor)
                xp += 200

        if m.bottom < 0 and m in missiles:
            missiles.remove(m)


def shoot():
    if missiles == [] or missiles[-1].y < HEIGHT/2:
        missile = Actor("missile", (ship.x, HEIGHT-180))
        missiles.append(missile)


pgzrun.go()