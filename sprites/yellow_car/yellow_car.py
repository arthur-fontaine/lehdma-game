from lib.game.Game import Game
from models.character.MainCharacter import MainCharacter
from utils.load_sprite import load_sprite


class __YellowCar(MainCharacter):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_yellow_car(self, game: Game):
        self.sprite = load_sprite(game, 'yellow-car', f"assets/objects/yellow-car")
        self.game = game


yellow_car = __YellowCar('YellowCar', '', 100)
