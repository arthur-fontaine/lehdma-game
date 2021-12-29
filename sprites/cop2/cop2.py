from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __Cop2(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_cop2(self, game: Game):
        self.sprite = load_sprite(game, 'cop')
        self.game = game


cop2 = __Cop2('Policier 2', '', 100)
