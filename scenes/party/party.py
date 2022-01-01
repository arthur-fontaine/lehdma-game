from re import L
from typing import Callable

from lib.game.Game import Game, Scene, Sprite
from models.inventory.items.Car import Car
from models.inventory.items.Knife import Knife
from models.inventory.items.MoneyEnvelope import MoneyEnvelope
from sprites.car_dealer.car_dealer import car_dealer
from sprites.jey.jey import jey
from sprites.beaten_guy.beaten_guy import beaten_guy
from sprites.bip1.bip1 import bip1
from sprites.bip2.bip2 import bip2
from utils.load_map import load_map


def party(game: Game):
    scene = Scene()

    map_sprite = load_map(game)
    scene.add_sprite(map_sprite)

    jey.build_jey(game)
    scene.add_sprite(jey.sprite)

    beaten_guy.build_beaten_guy(game)
    scene.add_sprite(beaten_guy.sprite)

    bip1.build_bip1(game)
    scene.add_sprite(bip1.sprite)

    bip2.build_bip2(game)
    scene.add_sprite(bip2.sprite)

    white_screen = Sprite('assets/white-screen.png')
    white_screen.set_opacity_to(0)
    scene.add_sprite(white_screen)

    black_screen = Sprite('assets/black-screen.png')
    scene.add_sprite(black_screen)

    chapter_sprite = Sprite('assets/chapters-title/chapter-2.png')
    chapter_sprite.set_opacity_to(0)
    scene.add_sprite(chapter_sprite)

    def on_black_screen_is_disappearing(_):
        jey.sprite.set_scale_to(0.25)
        jey.sprite.set_position_to(jey.sprite.size[0] / 2, jey.sprite.size[1] / 2)
        jey.sprite.change_y_by(- jey.sprite.size[1] / 4)

        bip1.sprite.set_scale_to(0.25)
        bip1.sprite.set_position_to(bip1.sprite.size[0] / 2, bip1.sprite.size[1] / 2)
        bip1.sprite.change_y_by(- bip1.sprite.size[1] / 4)
        bip1.sprite.change_x_by(- 300)

        bip2.sprite.set_scale_to(0.25)
        bip2.sprite.set_position_to(bip2.sprite.size[0] / 2, bip2.sprite.size[1] / 2)
        bip2.sprite.change_y_by(- bip2.sprite.size[1] / 4)
        bip2.sprite.change_x_by(- 150)

        beaten_guy.sprite.set_scale_to(0.25)
        beaten_guy.sprite.set_position_to(beaten_guy.sprite.size[0] / 2, beaten_guy.sprite.size[1] / 2)
        beaten_guy.sprite.set_opacity_to(0)

        map_sprite.set_position_to(map_sprite.size[0] / 2 - 700, map_sprite.size[1] / 2 - 500)

    scene.on('black_screen_is_disappearing', on_black_screen_is_disappearing)

    def on_black_screen_end(_):
        dialog_duration = 5

        jey.sprite.play_animation('walkingfromtheback')
        jey.sprite.change_y_by_in_seconds(115, 2)
        game.wait_then(2, lambda _: jey.sprite.stop_animation(), reset_timer=True)
        game.wait_then(0, lambda _: jey.sprite.switch_costume("back"))

        game.wait_then(0, lambda _: scene.display_text(
            "\"Ouais bien ou quoi ? C'est Jay. J'voulais savoir si j'peux passer chez toi là ?\"", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("\"Euh, c'est compliqué là.\"", '???'))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text("\"Arrête j'entends pleins d'bruits derrière toi là.\"", jey.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text("\"Ouais mais là c'est vraiment pas l'ambiance.\"", '???'))
        game.wait_then(dialog_duration, lambda _: scene.display_text("\"Vas-y on est en bas là.\"", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("??? a raccroché.", jey.name))
        game.wait_then(dialog_duration,
                       lambda _: choice_node_12(on_choice_node_12_stay_click, on_choice_node_12_leave_click))

    scene.on('black_screen_end', on_black_screen_end)

    def leave():
        game.wait_then(0, lambda _: jey.sprite.play_animation('walkforward'), reset_timer=True)
        game.wait_then(0, lambda _: jey.sprite.change_y_by_in_seconds(-115, 2))
        game.wait_then(2, lambda _: jey.sprite.stop_animation())

        game.wait_then(0, lambda _: jey.sprite.play_animation('walkingright'))
        game.wait_then(0, lambda _: bip1.sprite.play_animation('walkingright'))
        game.wait_then(0, lambda _: bip2.sprite.play_animation('walkingright'))
        game.wait_then(0, lambda _: jey.sprite.change_x_by_in_seconds(805, 14))
        game.wait_then(0, lambda _: bip1.sprite.change_x_by_in_seconds(805, 14))
        game.wait_then(0, lambda _: bip2.sprite.change_x_by_in_seconds(805, 14))

    def choice_node_12(on_stay_click: Callable, on_leave_click: Callable):
        displayed_text = """Voulez-vous rester ou partir ?
> [ref=stay]Rester[/ref]
> [ref=leave]Partir[/ref]"""

        scene.display_text(displayed_text,
                           on_stay_click=on_stay_click,
                           on_leave_click=on_leave_click)

    def on_choice_node_12_stay_click(_):
        dialog_duration = 5

        scene.clear_text()
        game.wait_then(1, lambda _: jey.sprite.play_animation('walkingright'), reset_timer=True)
        game.wait_then(0, lambda _: jey.sprite.change_x_by_in_seconds(130, 2))
        game.wait_then(2, lambda _: jey.sprite.stop_animation())
        game.wait_then(0, lambda _: jey.sprite.switch_costume('left'))

        game.wait_then(1, lambda _: beaten_guy.sprite.set_opacity_to(1))
        game.wait_then(0, lambda _: beaten_guy.sprite.play_animation('walkforward'))
        game.wait_then(0, lambda _: beaten_guy.sprite.change_y_by_in_seconds(-35, 1))
        game.wait_then(1, lambda _: beaten_guy.sprite.stop_animation())
        game.wait_then(0, lambda _: beaten_guy.sprite.switch_costume('right'))

        game.wait_then(1, lambda _: jey.sprite.play_animation('walkingleft'))
        game.wait_then(0, lambda _: jey.sprite.change_x_by_in_seconds(-30, 1))
        game.wait_then(1, lambda _: jey.sprite.stop_animation())
        game.wait_then(0, lambda _: jey.sprite.switch_costume('left'))

        game.wait_then(1, lambda _: scene.display_text("\"Hé toi là ! Tu fais l'beau ? T'étais à la soirée ?\"", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("\"Bien sûr il y étais frère !\"", bip1.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("\"Mais j'vous connais même pas.\"", beaten_guy.name))
        game.wait_then(dialog_duration, lambda _: scene.clear_text())
        game.wait_then(1, lambda _: white_screen.set_opacity_to_in_seconds(1, 0.5))
        game.wait_then(0.5, lambda _: white_screen.set_opacity_to_in_seconds(0, 0.5))
        game.wait_then(0.5, lambda _: scene.display_text("\"Tiens fils de pute !\"", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("\"P'tit bâtard !\"", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("\"Nan vas-y, laisse le, on s'en va.\"", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.clear_text())

        game.wait_then(0, lambda _: leave())

        # TODO: change the scene

    def on_choice_node_12_leave_click(_):
        game.wait_then(0, lambda _: scene.clear_text(), reset_timer=True)
        game.wait_then(0, lambda _: leave())

    def show_chapter_title(_):
        chapter_sprite.set_opacity_to_in_seconds(1, 2)

    def hide_chapter_title_and_black_screen(_):
        chapter_sprite.set_opacity_to_in_seconds(0, 2)
        black_screen.set_opacity_to_in_seconds(0, 2)

    def on_scene_start(_):
        black_screen.set_position_to(black_screen.size[0] / 2, black_screen.size[1] / 2)
        black_screen.set_scale_to(5)
        chapter_sprite.set_position_to(chapter_sprite.size[0] / 2, chapter_sprite.size[1] / 2)

        game.wait_then(2, show_chapter_title)
        game.wait_then(0, lambda _: scene.emit('black_screen_is_disappearing'))
        game.wait_then(5, hide_chapter_title_and_black_screen)
        game.wait_then(2, lambda _: scene.emit('black_screen_end'))

    scene.on('start', on_scene_start)

    return scene
