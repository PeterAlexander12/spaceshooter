import pgzrun
import random
import time

WIDTH = 600
HEIGHT = 600

fiende = []
spelare = Actor("ball", (300,300))
missiler = []

for i in range(1):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    fiende.append(Actor("bear", (x, y)))


def draw():
    global fiende
    screen.fill((0,0,0))
    spelare.draw()
    fiende[0].draw()
    for m in missiler:
        m.draw()
        
def update():
    i = 0
    while i < len(missiler):
        m = missiler[i]
        m.x += m.x_hastighet
        m.y += m.y_hastighet

        if m.x < 0 or m.x > WIDTH or m.y < 0 or m.y > HEIGHT:
            missiler.remove(m)
        else:
            i += 1



def on_mouse_down(pos):
    ny_missil = Actor("bullet", spelare.pos)
    x_led = pos[0] - spelare.x
    y_led = pos[1] - spelare.y
    avstand = (x_led**2 + y_led**2)**0.5
    ny_missil.x_hastighet = x_led/avstand*3
    ny_missil.y_hastighet = y_led/avstand*3
    ny_missil.angle = ny_missil.angle_to(pos) + 270
    missiler.append(ny_missil)



pgzrun.go()