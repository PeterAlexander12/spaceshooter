import pygame
import random

WIDTH = 600
HEIGHT = 600

enemy_bild = pygame.image.load("images/enemy.png").convert_alpha()
enemy_bild = pygame.transform.scale(enemy_bild, (50, 50))

screen = pygame.display.set_mode((WIDTH, HEIGHT))

DODGE_DURATION = 10  # frames the dodge animation lasts
DODGE_DISTANCE = 20  # how far sideways the enemy steps during a dodge

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

        self.dodge_timer = 0
        self.dodge_direction = 1

    def dodge(self):
        self.dodge_timer = DODGE_DURATION
        self.dodge_direction = random.choice([-1, 1])

    def dodge_offset(self):
        if self.dodge_timer <= 0:
            return 0
        half = DODGE_DURATION / 2
        elapsed = DODGE_DURATION - self.dodge_timer
        progress = elapsed / half if elapsed < half else (DODGE_DURATION - elapsed) / half
        return self.dodge_direction * DODGE_DISTANCE * progress

    def move_toward(self, target):
        if self.dodge_timer > 0:
            self.dodge_timer -= 1

        if self.rect.centerx < target.rect.centerx:
            self.rect.x += self.speed
        if self.rect.centerx > target.rect.centerx:
            self.rect.x -= self.speed
        if self.rect.centery < target.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > target.rect.centery:
            self.rect.y -= self.speed

    def draw(self):
        draw_rect = self.rect.move(self.dodge_offset(), 0)
        screen.blit(enemy_bild, draw_rect)
        pygame.draw.rect(screen, (255, 255, 255), (draw_rect.x, draw_rect.y - 10, 50, 15))
        pygame.draw.rect(screen, (144, 238, 144), (draw_rect.x, draw_rect.y - 10, 50 * (self.hp / self.max_hp), 15))