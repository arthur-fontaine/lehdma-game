from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __Jey(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_jey(self, game: Game):
        self.sprite = load_sprite(game, 'jey')
        self.game = game


jey = __Jey('Jey', 'Jey is a main character', 100)
