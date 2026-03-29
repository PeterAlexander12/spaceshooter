import time

import pgzrun
from pgzero.keyboard import keyboard

WIDTH = 800
HEIGHT = 600

spelare1_poang = 0
spelare2_poang = 0

spelare1 = Actor("rectangle", (20, 300))
spelare2 = Actor("rectangle", (780, 400))
boll = Actor("ball", (400, 300))
x_hastighet = 3
y_hastighet = 3

def draw():
    screen.fill((0,0,0))
    spelare1.draw()
    spelare2.draw()
    boll.draw()
    screen.draw.text(str(spelare1_poang), (450,30), fontsize=60)
    screen.draw.text(str(spelare2_poang), (350,30), fontsize=60)

def update():
    global y_hastighet, x_hastighet
    global spelare2_poang, spelare1_poang

    boll.x += x_hastighet
    boll.y += y_hastighet

    if boll.y < 0 or boll.y > HEIGHT:
        y_hastighet = -y_hastighet

    if spelare1.colliderect(boll) or spelare2.colliderect(boll):
        x_hastighet = -x_hastighet
    if spelare1.colliderect(boll):
        y_hastighet += 3
        x_hastighet += 3

    if keyboard.down and spelare1.bottom < HEIGHT:
        spelare1.y += 5
    if keyboard.up and spelare1.top > 0:
        spelare1.y -= 5
    if keyboard.w and spelare2.top > 0:
        spelare2.y -= 5
    if keyboard.s and spelare2.bottom < HEIGHT:
        spelare2.y += 5

    if boll.x > WIDTH:
        boll.y = HEIGHT/2
        boll.x = WIDTH/2
        spelare2_poang += 1

    if boll.x < 0:
        boll.y = HEIGHT/2
        boll.x = WIDTH/2
        spelare1_poang += 1

if x_hastighet > 20 or y_hastighet > 20:
    x_hastighet = 3
    y_hastighet = 3


pgzrun.go()