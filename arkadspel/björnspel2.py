import pgzrun
# importera pygame zero, alltså där man spelar
import random
import time


WIDTH = 800
HEIGHT = 700

poang = 0
lage = "meny"

highscore_file = open("highscoresBjörnspel2.txt", "r")
highscore = int(highscore_file.read())
highscore_file.close()

spelare = Actor("bear")

vit = Actor("ball")
vit.x = random.randint(0,WIDTH)
vit.y = random.randint(0,HEIGHT)

svart = Actor("blackball")
svart.x = random.randint(0,WIDTH)
svart.y = random.randint(0,HEIGHT)


def draw():
    screen.fill((125,165,232))
    if lage == "meny":
        screen.draw.text("Tryck mellanslag för att spela!", center=(400,300))
    if lage == "spel":
        spelare.draw()
        vit.draw()
        svart.draw()
        screen.draw.text("Poäng: " + str(poang), center=(400,40))
    if lage == "slut":
        screen.draw.text("Din poäng blev: " + str(poang), center=(400,250))
        screen.draw.text("Tryck mellanslag för att spela!", center=(400,300))
        screen.draw.text("Highscore är " + str(highscore), center=(400,275))


def update():
    global poang, lage, highscore

    if lage == "meny":
        if keyboard.space:
            lage ="spel"
            spelare.x = 0
            spelare.y = 0
            poang = 0
    if lage == "spel":
        if keyboard.up:
            spelare.y -= 5
        if keyboard.down:
            spelare.y += 5
        if keyboard.left:
            spelare.x -= 5
        if keyboard.right:
            spelare.x += 5

        if spelare.colliderect(vit):
            poang += 1
            vit.x = random.randint(0,WIDTH)
            vit.y = random.randint(0,HEIGHT)
            svart.y = random.randint(0, HEIGHT)
        if spelare.colliderect(svart):
            print("Spelet är slut")
            lage = "slut"

            if poang > highscore:
                highscore = poang
                highscore_file = open("highscoresBjörnspel2.txt", "w")
                highscore_file.write(str(poang))
                highscore_file.close()


    if lage == "slut":
        if keyboard.space:
            lage = "meny"


pgzrun.go()