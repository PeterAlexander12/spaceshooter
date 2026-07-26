import pygame as pg

class SubMenu:
    def __init__(self, tabs):
        self.tabs = tabs
        self.active = 0

    def next(self):
        self.active = (self.active + 1) % len(self.tabs)

    def prev(self):
        self.active = (self.active - 1) % len(self.tabs)

    def current(self):
        return self.tabs[self.active]

