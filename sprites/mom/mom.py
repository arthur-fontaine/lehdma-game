from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __Mom(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_mom(self, game: Game):
        self.sprite = load_sprite(game, 'mom')
        self.game = game


mom = __Mom('Mom', 'The mom of Jey.', 100)
