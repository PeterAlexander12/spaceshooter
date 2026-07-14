import pygame
import random
import math

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pointy_missile_pic = pygame.transform.scale(pygame.image.load("images/pointy_bullet.png").convert_alpha(),(100, 100))

class Pointy_Missile:
    def __init__(self, start_pos, target_pos):
        self.rect = pointy_missile_pic.get_rect(center=start_pos)
        x_led = target_pos[0] - start_pos[0]
        y_led = target_pos[1] - start_pos[1]
        avstand = math.sqrt(x_led ** 2 + y_led ** 2)
        hastighet = 5
        self.x_hastighet = x_led / avstand * hastighet
        self.y_hastighet = y_led / avstand * hastighet
        self.angle = math.degrees(math.atan2(-y_led, x_led)) - 90
        self.damage = 2

    def update(self):
        self.rect.x += self.x_hastighet
        self.rect.y += self.y_hastighet

    def utanfor_skarm(self):
        return self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT

    def draw(self):
        roterad = pygame.transform.rotate(pointy_missile_pic, self.angle)
        screen.blit(roterad, roterad.get_rect(center=self.rect.center))