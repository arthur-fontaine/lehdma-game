from lib.game.Game import Game, Sprite


def load_map(game: Game, map_path='assets/map/map.png'):
    sprite = Sprite(map_path)

    def on_game_start(_):
        sprite.set_scale_to(3)

    game.on('start', on_game_start)

    return sprite
