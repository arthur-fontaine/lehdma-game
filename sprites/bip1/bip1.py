from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __Bip1(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_bip1(self, game: Game):
        self.sprite = load_sprite(game, 'bip-1')
        self.game = game


bip1 = __Bip1('Bip 1', 'Bip 1 is a friend of Jey.', 100)
