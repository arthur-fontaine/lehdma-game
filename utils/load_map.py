from lib.game.Game import Game, Sprite


def load_map(game: Game, map_path='assets/map/map.png', initial_scale=3):
    sprite = Sprite(map_path)

    def on_game_start(_):
        sprite.set_scale_to(initial_scale)

    game.on('start', on_game_start)

    return sprite
