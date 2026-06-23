class Loadout:
    def __init__(self):
        self.health_potions = []
        self.bombs = []

    def add_potion(self, potion):
        self.health_potions.append(potion)

    def get_potion(self):
        if len(self.health_potions) > 0:
            potion = self.health_potions.pop(0)
            return potion
        return None

    def add_bomb(self):
        self.bombs.append("bomb")

    def use_bomb(self):
        if len(self.bombs) > 0:
            self.bombs.pop(0)
            return True
        return False