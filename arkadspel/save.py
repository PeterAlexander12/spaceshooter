def save_game(coins, loadout):
    with open("coins.txt", "w") as f:
        f.write(str(coins))
    with open("health_Potion.txt", "w") as f:
        f.write(str(sum(1 for p in loadout.potions if p == "health_potion")))
    with open("strength_Potion.txt", "w") as f:
        f.write(str(sum(1 for p in loadout.potions if p == "strength")))
    with open("bombs.txt", "w") as f:
        f.write(str(len(loadout.bombs)))


def load_game(loadout):
    with open("coins.txt", "r") as f:
        coins = int(f.read())

    with open("bombs.txt", "r") as f:
        for i in range(int(f.read())):
            loadout.add_bomb()

    with open("health_Potion.txt", "r") as f:
        for i in range(int(f.read())):
            loadout.add_potion("health_potion")

    with open("strength_Potion.txt", "r") as f:
        for i in range(int(f.read())):
            loadout.add_potion("strength")

    return coins
