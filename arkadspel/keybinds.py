import pygame

DEFAULT_KEYBINDS = {
    "use_potion": pygame.K_SPACE,
    "open_shop": pygame.K_s,
    "open_backpack": pygame.K_e,
    "use_bomb": 3,
    
}

def save_keybinds(keybinds):
    with open("keybinds.txt", "w") as f:
        for action, key in keybinds.items():
            f.write(action + ":" + str(key) + "\n")

def load_keybinds():
    keybinds = dict(DEFAULT_KEYBINDS)
    try:
        with open("keybinds.txt", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2 and parts[0] in keybinds:
                    keybinds[parts[0]] = int(parts[1])
    except FileNotFoundError:
        pass
    return keybinds
