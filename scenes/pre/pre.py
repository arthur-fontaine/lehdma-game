from lib.game.Game import Game, Scene, Sprite
from scenes.moms_house.moms_house import moms_house


def pre(game: Game):
    scene = Scene()

    pre_sprite = Sprite('assets/chapters-title/pre.png')
    pre_sprite.set_opacity_to(0)
    scene.add_sprite(pre_sprite)

    def on_scene_start(_):
        pre_sprite.set_opacity_to_in_seconds(1, 2)
        game.wait_then(12, lambda _: pre_sprite.set_opacity_to_in_seconds(0, 2), reset_timer=True)
        game.wait_then(2, lambda _: game.add_scene(moms_house(game), 'moms_house'))
        game.wait_then(0, lambda _: game.change_scene('moms_house', True))

    scene.on('pre_start', on_scene_start)

    return scene
