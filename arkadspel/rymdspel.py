import pgzrun
import random

# behind pygame zero:
# while True:
#    handle_input()
#    update()
#    draw()

WIDTH = 600
HEIGHT = 600

fiende = []
spelare = Actor("ball", (300,300))
missiler = []

antal_fiender = 5
liv = 3
lage = "spel"

#skapa fiender
for i in range(antal_fiender):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    fiende.append(Actor("bear", (x, y)))
    
# 1 input
def on_mouse_down(pos):
    ny_missil = Actor("bullet", spelare.pos)
    x_led = pos[0] - spelare.x
    y_led = pos[1] - spelare.y
    avstand = (x_led ** 2 + y_led ** 2) ** 0.5
    ny_missil.x_hastighet = x_led / avstand * 3
    ny_missil.y_hastighet = y_led / avstand * 3
    ny_missil.angle = ny_missil.angle_to(pos) + 270
    missiler.append(ny_missil)

def on_mouse_up(pos, button):
    pass

def on_mouse_move(pos, rel, buttons):
    pass

def on_key_down(key, mod, unicode):
    pass

def on_key_up(key, mod):
    pass

def on_music_end():
    pass


# 2 update
def update():

    global liv, lage # global: change the outer variable

    if lage == "slut":
        if keyboard.space:
            restart()
        return

    # 1. Spelarrörelse
    if keyboard.up:
        spelare.y -= 5
    if keyboard.down:
        spelare.y += 5
    if keyboard.left:
        spelare.x -= 5
    if keyboard.right:
        spelare.x += 5

    # Fiender rör sig mot spelaren (en pixel närmare)
    for f in fiende:
        if f.x < spelare.x:
            f.x += 1
        if f.x > spelare.x:
            f.x -= 1
        if f.y < spelare.y:
            f.y += 1
        if f.y > spelare.y:
            f.y -= 1

    for f in list(fiende):
        if f.colliderect(spelare):
            fiende.remove(f)
            liv -= 1
        if liv <= 0:
            lage = "slut"

# 3 draw
def draw():
    screen.fill((0,0,0))
    if lage == "slut":
        screen.draw.text("Game Over!", center=(300, 250), color="red", fontsize=60)
        screen.draw.text("Tryck mellanslag för att starta om", center=(300, 320), color="white", fontsize=30)
        return
    spelare.draw()
    for f in fiende:
        f.draw()
    for m in missiler:
        m.draw()
    screen.draw.text("Liv: " + str(liv), (10, 10), color="white", fontsize=40)


    #Flytta missiler
    i = 0
    while i < len(missiler):
        m = missiler[i]
        m.x += m.x_hastighet
        m.y += m.y_hastighet

        if m.x < 0 or m.x > WIDTH or m.y < 0 or m.y > HEIGHT:
            missiler.remove(m)
        else:
            i += 1

    # 3. Kollision mellan missiler och fiender
    for m in list(missiler):
        for f in list(fiende):
            if m.colliderect(f):
                missiler.remove(m)
                fiende.remove(f)
                break


def restart():
    global liv, lage, fiende, missiler
    liv = 3
    lage = "spel"
    spelare.x = 300
    spelare.y = 300
    missiler = []
    fiende = []
    for i in range(5):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        fiende.append(Actor("bear", (x, y)))


pgzrun.go()