import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
import random
import time

WIDTH = 800
HEIGHT = 600

spelare1 = Actor("bear", (50,300))
spelare2 = Actor("bear", (750,300))

spelare1_poang = 0
spelare2_poang = 0

bana = []
for i in range(30):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    bana.append(Actor("tree", (x, y)))

def draw():
    screen.fill((104,163,60))
    spelare1.draw()
    spelare2.draw()
    screen.draw.text(str(spelare1_poang), (450, 30), fontsize=60)
    screen.draw.text(str(spelare2_poang), (350, 30), fontsize=60)

def uppdate():
    global spelare1_poang, spelare2_poang
    if spelare1.left > WIDTH:
        spelare1.right = 0

    if spelare2.left > WIDTH:
        spelare2.right = 0

    if keyboard.w:
        spelare1.x += 5


pgzrun.go()