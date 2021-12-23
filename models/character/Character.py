class Character:
    def __init__(self, name: str, description: str, health: int):
        self.name = name
        self.description = description
        self.health = health
        self.inventory = []
