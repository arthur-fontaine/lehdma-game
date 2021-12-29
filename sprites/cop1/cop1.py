from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __Cop1(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_cop1(self, game: Game):
        self.sprite = load_sprite(game, 'cop')
        self.game = game


cop1 = __Cop1('Policier 1', '', 100)
