import pgzrun
from pgzero import screen
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
import random
import time

WIDTH = 800
HEIGHT = 600
# hur bret och långt banan ska vara

starttid = time.time()
spelare = Actor("bear") # vilken gube spelaren ska vara/kan styra

bana1 = []

bana1.append(Actor("tree", (200,350)))
bana1.append(Actor("tree", (100,350)))
bana1.append(Actor("tree", (300,550)))
bana1.append(Actor("tree", (500,80)))
bana1.append(Actor("tree", (600,450)))
bana1.append(Actor("tree", (220,30)))

bana2 = []
for i in range(15):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    bana2.append(Actor("tree", (x, y)))


bana3 = []
for i in range(7):
    bana3.append(Actor("tree", (100+i*100, HEIGHT/2)))

banor = []
banor.append(bana1)
banor.append(bana2)
banor.append(bana3)

nuvarande_bana = 0

slutet = Actor("ball")
def update_slutet():
    bana = banor[nuvarande_bana]
    slumpvalt_trad = random.randint(0, len(bana)-1)
    slutet.x = bana[slumpvalt_trad].x
    slutet.y = bana[slumpvalt_trad].y
update_slutet()

def draw():
    screen.fill((104,163,60))
    spelare.draw()
    slutet.draw()
    bana = banor[nuvarande_bana]
    for t in bana:
        t.draw()
    tid = round(time.time() - starttid)
    screen.draw.text(str(tid), (WIDTH-50, 30), color="white", fontsize=50)


def update():
    global nuvarande_bana, starttid
    if keyboard.up:
        spelare.y -= 5
    if keyboard.down:
        spelare.y += 5
    if keyboard.left:
        spelare.x -= 5
    if keyboard.right:
        spelare.x += 5

    if spelare.colliderect(slutet):
        if nuvarande_bana < (len(banor)-1):
            nuvarande_bana += 1
            update_slutet()
        else:
            nuvarande_tid =time.time()
            sluttid = round(nuvarande_tid - starttid)
            print("Du klarade spelet på: " + str(sluttid) + " sekunder")
            nuvarande_bana = 0
            update_slutet()
            starttid = time.time()




pgzrun.go()