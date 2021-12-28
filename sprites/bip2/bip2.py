from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __Bip2(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_bip2(self, game: Game):
        self.sprite = load_sprite(game, 'bip-2')
        self.game = game


bip2 = __Bip2('Bip 2', 'Bip 2 is a friend of Jey.', 100)
