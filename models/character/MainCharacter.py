from models.character.Character import Character
from models.inventory.Inventory import Inventory


class MainCharacter(Character):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)

        self.inventory = Inventory()
