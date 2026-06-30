import pygame
from save import save_keybinds, load_keybinds as _load_keybinds

DEFAULT_KEYBINDS = {
    "use_health_potion": pygame.K_SPACE,
    "use_strength_potion": pygame.K_z,
    "open_shop": pygame.K_s,
    "open_backpack": pygame.K_e,
    "use_bomb": 3,
    
}

MOUSE_NAMES = {
    1: "left click", 
    2: "middle click", 
    3: "right click", 
    4: "scroll up", 
    5: "scroll down"
}

def bind_name(value):
    if value in MOUSE_NAMES:
        return MOUSE_NAMES[value]
    return pygame.key.name(value)

def load_keybinds():
    return _load_keybinds(DEFAULT_KEYBINDS)
