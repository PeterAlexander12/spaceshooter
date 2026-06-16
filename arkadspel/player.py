import pygame




class Player:
    def __init__(self, screen, player_pic):
        self.screen = screen
        self.player_pic = player_pic
        self.rect = pygame.Rect(300, 300, player_pic.get_width(), player_pic.get_height())
        self.rect.center = (300, 300)

    def draw(self):
        self.screen.blit(self.player_pic, self.rect)