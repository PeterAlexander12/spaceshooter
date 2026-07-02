class Loadout:
    def __init__(self):
        self.health_potions = []
        self.strength_potions = []
        self.bombs = []

    def add_health_potion(self):
        self.health_potions.append("health_potion")

    def get_health_potion(self):
        if len(self.health_potions) > 0:
            potion = self.health_potions.pop(0)
            return potion
        return None

    def add_strength_potion(self):
        self.strength_potions.append("strength_potion")

    def get_strength_potion(self):
        if len(self.strength_potions) > 0:
            potion = self.strength_potions.pop(0)
            return potion
        return None

    def add_bomb(self):
        self.bombs.append("bomb")

    def use_bomb(self):
        if len(self.bombs) > 0:
            self.bombs.pop(0)
            return True
        return False