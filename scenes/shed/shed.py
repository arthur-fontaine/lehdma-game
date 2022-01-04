from lib.game.Game import Game, Scene, Sprite
from sprites.bip1.bip1 import bip1
from sprites.bip2.bip2 import bip2
from sprites.cop1.cop1 import cop1
from sprites.cop2.cop2 import cop2
from sprites.jey.jey import jey
from utils.load_map import load_map


def shed(game: Game):
    scene = Scene()

    map_sprite = load_map(game, 'assets/map/buildings/shed/shed.png', 1)
    scene.add_sprite(map_sprite)

    jey.build_jey(game)
    scene.add_sprite(jey.sprite)

    bip1.build_bip1(game)
    scene.add_sprite(bip1.sprite)

    bip2.build_bip2(game)
    scene.add_sprite(bip2.sprite)

    cop1.build_cop1(game)
    scene.add_sprite(cop1.sprite)

    cop2.build_cop2(game)
    scene.add_sprite(cop2.sprite)

    black_screen = Sprite('assets/black-screen.png')
    scene.add_sprite(black_screen)

    white_screen = Sprite('assets/white-screen.png')
    white_screen.set_opacity_to(0)
    scene.add_sprite(white_screen)

    chapter_sprite = Sprite('assets/chapters-title/chapter-5.png')
    chapter_sprite.set_opacity_to(0)
    scene.add_sprite(chapter_sprite)

    end_sprite = Sprite('assets/chapters-title/end.png')
    end_sprite.set_opacity_to(0)
    scene.add_sprite(end_sprite)

    def on_black_screen_is_disappearing(_):
        # TODO: adjust position of sprites
        jey.sprite.set_scale_to(0.25)
        jey.sprite.set_position_to(400, 300)
        jey.sprite.change_x_by(150)

        bip1.sprite.set_scale_to(0.25)
        bip1.sprite.set_position_to(400, 300)
        bip1.sprite.change_x_by(150)
        bip1.sprite.change_y_by(-150)

        bip2.sprite.set_scale_to(0.25)
        bip2.sprite.set_position_to(400, 300)
        bip2.sprite.change_x_by(-150)
        bip2.sprite.change_y_by(-75)

        cop1.sprite.set_scale_to(0.25)
        cop1.sprite.set_position_to(400, 300)
        cop1.sprite.change_x_by(100)
        cop1.sprite.change_y_by(200)

        cop2.sprite.set_scale_to(0.25)
        cop2.sprite.set_position_to(400, 300)
        cop2.sprite.change_x_by(-100)
        cop2.sprite.change_y_by(200)

        map_sprite.set_position_to(map_sprite.size[0] / 2 - 112, map_sprite.size[1] / 2)

    scene.on('shed_black_screen_is_disappearing', on_black_screen_is_disappearing)

    def on_black_screen_end(_):
        dialog_duration = 5

        game.wait_then(0, lambda _: scene.display_text('Bon les gars, vous voyez cette arme, là ?', cop1.name),
                       reset_timer=True)
        game.wait_then(dialog_duration, lambda _: scene.display_text('Bien sûr qu\'ils la voient', cop2.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Bah c\'est pas mon arme de service, '
                                                                     'on va dire que c\'est une arme de loisir.',
                                                                     cop1.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text('On va dire qu\'elle est intraçable et qu\'on peut '
                                                    'faire c\'qu\'on veut avec.', cop2.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text('Ouais, et c\'qui va s\'passer, c\'est tout simple. '
                                                    'J\'vais la j\'ter au milieu d\'vous trois, et \n'
                                                    'j\'vais vous laisser vous entretuer, jusqu\'à '
                                                    'c\'qu\'il y en reste plus qu\'un seul.', cop1.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text('Et le grand gagnant pourra repartir la vie sauve. '
                                                    'Compris ?', cop2.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Allez, c\'est parti !', cop1.name))
        game.wait_then(dialog_duration, lambda _: scene.clear_text())

        game.wait_then(dialog_duration, lambda _: bip2.sprite.switch_costume('gun'))

        game.wait_then(1, lambda _: scene.display_text('Gros, tu fais quoi frère, lâche ça !', bip1.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Eh, vas-y m\'touche pas toi !', bip2.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text('Poto, calme toi, tu vois pas qu\'ils veulent juste '
                                                    'rentrer dans ta tête, on est des shrabs à la base, \n'
                                                    'on est fratés, liés jusqu\'à la fin', bip1.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Ouais tu dis ça mais tu t\'es toujours cru '
                                                                     'supérieur !',
                                                                     bip2.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text('Comment tu parles fils de pute ? Ça y est, c\'est '
                                                    'bon, t\'en peux plus parce qu\'t\'as un fer ?',
                                                    bip1.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('T\'es tout le temps fonce-dé et là tu me fais la '
                                                                     'morale ? T\'façon qu\'est-c\'tu peux faire ? \n'
                                                                     'C\'est moi j\'ai l\'ke-tru, là !', bip2.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Ok t\'as l\'ke-tru là mais qu\'est-c\'tu vas '
                                                                     'faire ? T\'as même pas les couilles ?',
                                                                     bip1.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Me pousse pas gros !', bip2.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Gros, j\'te pousse et qu\'est-c\'tu vas faire ?',
                                                                     bip1.name))
        game.wait_then(5, lambda _: scene.clear_text())

        game.wait_then(0.5, lambda _: white_screen.set_opacity_to_in_seconds(1, 0.5))
        game.wait_then(0.5, lambda _: bip1.sprite.set_opacity_to(0))
        game.wait_then(1, lambda _: white_screen.set_opacity_to_in_seconds(0, 0.5))

        game.wait_then(2, lambda _: bip2.sprite.switch_costume('back'))

        game.wait_then(0, lambda _: scene.display_text('Putain ! J\'arrête ! J\'arrête tout !', bip2.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text('Non non non, t\'arrêtes rien du tout ! Tu vas '
                                                                     'finir le travail !', cop1.name))

        game.wait_then(dialog_duration, lambda _: scene.clear_text())

        game.wait_then(2, lambda _: bip2.sprite.switch_costume('right'))
        game.wait_then(dialog_duration, lambda _: bip2.sprite.switch_costume('gun'))

        game.wait_then(0, lambda _: scene.display_text('J\'suis désolé, khey, jamais j\'aurais voulu '
                                                       't\'faire ça, à la base, on était frères.',
                                                       bip2.name))

        game.wait_then(dialog_duration, lambda _: scene.clear_text())
        game.wait_then(0, lambda _: black_screen.set_opacity_to(1))
        game.wait_then(2, lambda _: end_sprite.set_opacity_to_in_seconds(1, 2))

    scene.on('shed_black_screen_end', on_black_screen_end)

    def show_chapter_title(_):
        chapter_sprite.set_opacity_to_in_seconds(1, 2)

    def hide_chapter_title_and_black_screen(_):
        chapter_sprite.set_opacity_to_in_seconds(0, 2)
        black_screen.set_opacity_to_in_seconds(0, 2)

    def on_scene_start(_):
        black_screen.set_position_to(black_screen.size[0] / 2, black_screen.size[1] / 2)
        black_screen.set_scale_to(5)
        chapter_sprite.set_position_to(chapter_sprite.size[0] / 2, chapter_sprite.size[1] / 2)

        game.wait_then(2, show_chapter_title, reset_timer=True)
        game.wait_then(0, lambda _: scene.emit('shed_black_screen_is_disappearing'))
        game.wait_then(5, hide_chapter_title_and_black_screen)
        game.wait_then(2, lambda _: scene.emit('shed_black_screen_end'))

    scene.on('shed_start', on_scene_start)

    return scene
