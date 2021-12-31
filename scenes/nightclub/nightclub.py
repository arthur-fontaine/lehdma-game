from typing import Callable

from lib.game.Game import Game, Scene, Sprite
from models.inventory.items.Car import Car
from sprites.bip1.bip1 import bip1
from sprites.bip2.bip2 import bip2
from sprites.bouncer.bouncer import bouncer
from sprites.jey.jey import jey
from sprites.yellow_car.yellow_car import yellow_car
from utils.load_map import load_map


def nightclub(game: Game):
    scene = Scene()

    map_sprite = load_map(game)
    scene.add_sprite(map_sprite)

    bouncer.build_bouncer(game)
    scene.add_sprite(bouncer.sprite)

    bip1.build_bip1(game)
    scene.add_sprite(bip1.sprite)

    bip2.build_bip2(game)
    scene.add_sprite(bip2.sprite)

    jey.build_jey(game)
    scene.add_sprite(jey.sprite)

    jey.inventory.add_items(Car())

    if jey.inventory.has('car'):
        yellow_car.build_yellow_car(game)
        scene.add_sprite(yellow_car.sprite)

    black_screen = Sprite('assets/black-screen.png')
    scene.add_sprite(black_screen)

    chapter_sprite = Sprite('assets/chapters-title/chapter-2.png')
    chapter_sprite.set_opacity_to(0)
    scene.add_sprite(chapter_sprite)

    def on_black_screen_is_disappearing(_):
        jey.sprite.set_scale_to(0.25)
        jey.sprite.set_position_to(jey.sprite.size[0] / 2, jey.sprite.size[1] / 2)
        jey.sprite.change_y_by(-200)

        bip1.sprite.set_scale_to(0.25)
        bip1.sprite.set_position_to(bip1.sprite.size[0] / 2, bip1.sprite.size[1] / 2)
        bip1.sprite.change_y_by(-100)

        bip2.sprite.set_scale_to(0.25)
        bip2.sprite.set_position_to(bip2.sprite.size[0] / 2, bip2.sprite.size[1] / 2)
        bip2.sprite.change_x_by(150)
        bip2.sprite.change_y_by(-100)

        bouncer.sprite.set_scale_to(0.25)
        bouncer.sprite.set_position_to(bouncer.sprite.size[0] / 2, bouncer.sprite.size[1] / 2)
        bouncer.sprite.change_x_by(-105)
        bouncer.sprite.change_y_by(380)

        if jey.inventory.has('car'):
            jey.sprite.set_opacity_to(0)

            yellow_car.sprite.set_scale_to(0.25)
            yellow_car.sprite.set_position_to(yellow_car.sprite.size[0] / 2, yellow_car.sprite.size[1] / 2)
            yellow_car.sprite.change_y_by(-225)
            yellow_car.sprite.switch_costume('left')

        map_sprite.set_position_to(map_sprite.size[0] / 2 - 1490, map_sprite.size[1] / 2)

    scene.on('black_screen_is_disappearing', on_black_screen_is_disappearing)

    def on_black_screen_end(_):
        if jey.inventory.has('car'):
            game.wait_then(0, lambda _: bip1.sprite.play_animation('walkforward'), reset_timer=True)
            game.wait_then(0, lambda _: bip1.sprite.change_y_by_in_seconds(-20, 1))
            game.wait_then(1, lambda _: bip1.sprite.set_opacity_to(0))
            game.wait_then(0, lambda _: bip1.sprite.stop_animation())

            game.wait_then(0, lambda _: bip2.sprite.play_animation('walkingleft'))
            game.wait_then(0, lambda _: bip2.sprite.change_x_by_in_seconds(-150, 3))
            game.wait_then(3, lambda _: bip2.sprite.stop_animation())
            game.wait_then(0, lambda _: bip2.sprite.play_animation('walkforward'))
            game.wait_then(0, lambda _: bip2.sprite.change_y_by_in_seconds(-20, 1))
            game.wait_then(1, lambda _: bip2.sprite.set_opacity_to(0))
            game.wait_then(0, lambda _: bip2.sprite.stop_animation())

            game.wait_then(1, lambda _: yellow_car.sprite.switch_costume('left'))
            game.wait_then(0, lambda _: yellow_car.sprite.change_x_by_in_seconds(-175, 2))
            game.wait_then(0, lambda _: map_sprite.change_x_by_in_seconds(175, 2))
            game.wait_then(0, lambda _: bouncer.sprite.change_x_by_in_seconds(175, 2))

            game.wait_then(2, lambda _: yellow_car.sprite.switch_costume('back'))
            game.wait_then(0, lambda _: yellow_car.sprite.change_y_by_in_seconds(250, 2))
            game.wait_then(0, lambda _: map_sprite.change_y_by_in_seconds(-250, 2))
            game.wait_then(0, lambda _: bouncer.sprite.change_y_by_in_seconds(-250, 2))

            game.wait_then(2, lambda _: yellow_car.sprite.switch_costume('right'))
            game.wait_then(0, lambda _: yellow_car.sprite.change_x_by_in_seconds(180, 2))
            game.wait_then(0, lambda _: map_sprite.change_x_by_in_seconds(-180, 2))
            game.wait_then(0, lambda _: bouncer.sprite.change_x_by_in_seconds(-180, 2))

            game.wait_then(0, lambda _: bip2.sprite.set_y_to(433))
            game.wait_then(0, lambda _: bip1.sprite.set_y_to(433))
            game.wait_then(0, lambda _: jey.sprite.set_y_to(433))

            game.wait_then(3, lambda _: bip2.sprite.set_opacity_to(1))
            game.wait_then(0, lambda _: bip2.sprite.play_animation('walkingright'))
            game.wait_then(0, lambda _: bip2.sprite.change_x_by_in_seconds(125, 3))
            game.wait_then(3, lambda _: bip2.sprite.stop_animation())
            game.wait_then(0, lambda _: bip2.sprite.play_animation('walkforward'))
            game.wait_then(0, lambda _: bip2.sprite.change_y_by_in_seconds(-80, 1))
            game.wait_then(1, lambda _: bip2.sprite.stop_animation())
            game.wait_then(0, lambda _: bip2.sprite.switch_costume('left'))

            game.wait_then(0, lambda _: bip1.sprite.set_opacity_to(1))
            game.wait_then(0, lambda _: bip1.sprite.play_animation('walkingright'))
            game.wait_then(0, lambda _: bip1.sprite.change_x_by_in_seconds(125, 3))
            game.wait_then(3, lambda _: bip1.sprite.stop_animation())
            game.wait_then(0, lambda _: bip1.sprite.switch_costume('left'))

            game.wait_then(0, lambda _: yellow_car.sprite.set_opacity_to(0))
            game.wait_then(0, lambda _: jey.sprite.set_opacity_to(1))
        else:
            scene.display_text("T'abuses frère, t'as pas de voiture.")

        dialog_duration = 5

        game.wait_then(1, lambda _: scene.display_text("Désolé messieurs mais vous ne pourrez pas rentrer."))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text("Vous avez été débarqué par la porte de la voiture."),
                       bouncer.name)
        game.wait_then(dialog_duration, lambda _: scene.display_text("Comment ça ?"), jey.name)
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text("Vous n'êtes plus autorisé ici. Donc veuillez partir."),
                       bouncer.name)
        game.wait_then(dialog_duration, lambda _: scene.display_text("Vous avez été débarqué par la porte de la voiture."), jey.name)

    scene.on('black_screen_end', on_black_screen_end)

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
