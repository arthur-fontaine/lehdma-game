from models.Character import Character


class MainCharacter(Character):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
