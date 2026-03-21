import pgzrun
import time
import random
from pgzero.builtins import Actor

# behind pygame zero:
# while True:
#    handle_input()
#    update()
#    draw()

WIDTH = 600
HEIGHT = 700
SECONDS_BETWEEN_METEORS = 3

hp = 100
xp = 0


ship = Actor("ship", (WIDTH/2, HEIGHT-100)) # Actor: image with a position that can move (sprite)
missiles = [] # empty list
meteors = [] # empty list
explosions = [] # empty list
METEOR_IMAGES = ["meteors-1", "meteors-2", "meteors-3", "veronica-huvud-5"]
background = Actor("background", (WIDTH, HEIGHT), anchor=("right", "bottom"))
meteor_time = time.time()*1000

mode = "menu"

highscore_file = open("highscore.txt","r")
highscore = int(highscore_file.read())
highscore_file.close()

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

def draw():
    screen.fill((0,0,0))
    background.draw()
    if mode == "menu":
        screen.draw.text("SPACE SHOOTER", center=(WIDTH/2, 300), fontsize=50)
        screen.draw.text("Tryck mellanslag för att spela!", center=(WIDTH/2,350))
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
    background.y += 6 
    if background.y >= 600+HEIGHT:
        background.y = HEIGHT

def update_meteors():
    global meteor_time
    current_time = time.time() * 1000

    if current_time - meteor_time > SECONDS_BETWEEN_METEORS * 1000:
        selected_meteor_image = METEOR_IMAGES[random.randint(0, len(METEOR_IMAGES) - 1)]
        starting_x_position = random.randint(20, WIDTH - 20)
        new_meteor = Actor(selected_meteor_image, (starting_x_position, -100))
        new_meteor.horizontal_speed = random.choice([-3, 3])
        meteors.append(new_meteor)
        meteor_time = time.time() * 1000

    for meteor in meteors[:]:
        meteor.y += 6
        meteor.x += meteor.horizontal_speed

        if meteor.left <= 0 or meteor.right >= WIDTH:
            meteor.horizontal_speed = -meteor.horizontal_speed

        rotate_meteor(meteor)

        if meteor.y > HEIGHT + 100:
            meteors.remove(meteor)

def rotate_meteor(m):
    # rotera inte bilden om det är veronica
    if m.image != "veronica-huvud-5": 
        m.angle -= 4

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