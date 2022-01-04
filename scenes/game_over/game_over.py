from lib.game.Game import Game, Scene, Sprite


def game_over(game: Game):
    scene = Scene()

    game_over_sprite = Sprite('assets/chapters-title/game-over.png')
    game_over_sprite.set_opacity_to(0)
    scene.add_sprite(game_over_sprite)

    def on_scene_start(_):
        game_over_sprite.set_opacity_to_in_seconds(1, 2)

    scene.on('game_over_start', on_scene_start)

    return scene
