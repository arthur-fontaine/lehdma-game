from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __BeatenGuy(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_beaten_guy(self, game: Game):
        self.sprite = load_sprite(game, 'beaten-guy')
        self.game = game


beaten_guy = __BeatenGuy('Random Guy', '', 100)
