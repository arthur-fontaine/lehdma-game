from models.character.Character import Character


class NPC(Character):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
