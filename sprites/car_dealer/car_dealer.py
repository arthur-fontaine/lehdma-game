from lib.game.Game import Game
from models.character.NPC import NPC
from utils.load_sprite import load_sprite


class __CarDealer(NPC):
    def __init__(self, name: str, description: str, health: int):
        super().__init__(name, description, health)
        self.game = None
        self.sprite = None

    def build_car_dealer(self, game: Game):
        self.sprite = load_sprite(game, 'car-dealer')
        self.game = game


car_dealer = __CarDealer('Jey', 'A car dealer', 100)
