from lib.game.Game import Game, Sprite


def load_map(game: Game, scene_name: str, map_path='assets/map/map.png', initial_scale: float = 3):
    sprite = Sprite(map_path)

    def on_scene_start(_):
        sprite.set_scale_to(initial_scale)

    game.on(scene_name + '_start', on_scene_start)

    return sprite
