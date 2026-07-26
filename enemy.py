import pygame
import random

WIDTH = 600
HEIGHT = 600

enemy_bild = pygame.image.load("images/fiende.png").convert_alpha()
enemy_bild = pygame.transform.scale(enemy_bild, (50, 50))

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Enemy:
    def __init__(self, base_hp, base_speed):
        x = random.choice([random.randint(-200, 0), random.randint(600, 800)])
        y = random.choice([random.randint(-200, 0), random.randint(600, 800)])
        self.rect = pygame.Rect(x, y, enemy_bild.get_width(), enemy_bild.get_height())
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
        screen.blit(enemy_bild, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x, self.rect.y - 10, 50, 15))
        pygame.draw.rect(screen, (144, 238, 144), (self.rect.x, self.rect.y - 10, 50 * (self.hp / self.max_hp), 15))