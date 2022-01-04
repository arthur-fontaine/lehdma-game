from typing import Optional, Callable

from lib.game.Game import Game, Scene, Sprite
from scenes.party.party import party
from sprites.bip1.bip1 import bip1
from sprites.bip2.bip2 import bip2
from sprites.bouncer.bouncer import bouncer
from sprites.jey.jey import jey
from sprites.yellow_car.yellow_car import yellow_car
from utils.load_map import load_map


def nightclub(game: Game):
    scene = Scene()

    map_sprite = load_map(game, 'nightclub', 'assets/map/map.png')
    scene.add_sprite(map_sprite)

    map_rows_coordinates = [-1200, -800, -240, 0]
    map_columns_coordinates = [-112.3674911660778, -540, -1075, -1490]
    map_intersections = [
        ['br', 'lr', 'bl', ''],
        ['tbr', 'blr', 'tblr', 'bl'],
        ['tbr', 'tblr', 'tblr', 'tbl'],
        ['tr', 'tlr', 'tlr', 'tl'],
    ]

    sprite_rows_coordinates = [550, 325, 365, 100]
    sprite_columns_coordinates = [75, 325, 460, 740]

    bouncer.build_bouncer(game)
    scene.add_sprite(bouncer.sprite)

    bip1.build_bip1(game)
    scene.add_sprite(bip1.sprite)

    bip2.build_bip2(game)
    scene.add_sprite(bip2.sprite)

    jey.build_jey(game)
    scene.add_sprite(jey.sprite)

    if jey.inventory.has('car'):
        yellow_car.build_yellow_car(game)
        scene.add_sprite(yellow_car.sprite)

    black_screen = Sprite('assets/black-screen.png')
    scene.add_sprite(black_screen)

    chapter_sprite = Sprite('assets/chapters-title/chapter-3.png')
    chapter_sprite.set_opacity_to(0)
    scene.add_sprite(chapter_sprite)

    def take_flight(position: Optional[list[int]] = None):
        if position is None:
            position = [map_columns_coordinates[3], map_rows_coordinates[2]]

        scene.clear_text()

        x_intersection = map_columns_coordinates.index(position[0])
        y_intersection = map_rows_coordinates.index(position[1])
        map_intersection = map_intersections[y_intersection][x_intersection]

        game.wait_then(0, lambda _: bip1.sprite.set_opacity_to(0), reset_timer=True)
        game.wait_then(0, lambda _: bip2.sprite.set_opacity_to(0))
        game.wait_then(0, lambda _: bouncer.sprite.set_opacity_to(0))
        game.wait_then(0, lambda _: animate_sprites([jey.sprite], map_sprite.pos, position))
        game.wait_then(0, lambda _: map_sprite.change_position_by_in_seconds(-(map_sprite.pos[0] - position[0]),
                                                                             -(map_sprite.pos[1] - position[1]),
                                                                             2))
        sprite_y = sprite_rows_coordinates[y_intersection]
        sprite_x = sprite_columns_coordinates[x_intersection]
        game.wait_then(0, lambda _: jey.sprite.go_to_in_seconds(sprite_x, sprite_y, 2))
        game.wait_then(2, lambda _: stop_animations([jey.sprite]))
        game.wait_then(0, lambda _: take_flight_choice())

        def animate_sprites(sprites_to_animate: list[Sprite], current_position: list[int], target_position: list[int]):
            animation_name = ''

            if current_position[0] < target_position[0]:
                animation_name = 'walkingleft'
            elif current_position[0] > target_position[0]:
                animation_name = 'walkingright'
            elif current_position[1] < target_position[1]:
                animation_name = 'walkforward'
            elif current_position[1] > target_position[1]:
                animation_name = 'walkingfromtheback'

            if animation_name != '':
                for sprite in sprites_to_animate:
                    sprite.play_animation(animation_name)

        def stop_animations(sprites_animated: list[Sprite]):
            for sprite in sprites_animated:
                sprite.stop_animation()

        def take_flight_choice():
            if not ((x_intersection == 0 and y_intersection == 2) or (x_intersection == 1 and y_intersection == 2)):
                displayed_text = """Dans quelle direction veux-tu aller ?"""

                if "t" in map_intersection:
                    displayed_text += "\n> [ref=top]Haut[/ref]"
                if "b" in map_intersection:
                    displayed_text += "\n> [ref=bottom]Bas[/ref]"
                if "l" in map_intersection:
                    displayed_text += "\n> [ref=left]Gauche[/ref]"
                if "r" in map_intersection:
                    displayed_text += "\n> [ref=right]Droite[/ref]"

                scene.display_text(displayed_text,
                                   on_top_click=lambda _: take_flight(
                                       [position[0], map_rows_coordinates[y_intersection - 1]]),
                                   on_bottom_click=lambda _: take_flight(
                                       [position[0], map_rows_coordinates[y_intersection + 1]]),
                                   on_left_click=lambda _: take_flight(
                                       [map_columns_coordinates[x_intersection - 1], position[1]]),
                                   on_right_click=lambda _: take_flight(
                                       [map_columns_coordinates[x_intersection + 1], position[1]]))
            else:
                displayed_text = """Où voulez-vous vous cacher ?
> [ref=store]Dans le magasin[/ref]"""

                if x_intersection == 0 and y_intersection == 2:
                    displayed_text += "\n> [ref=car_shop]Chez le concessionaire[/ref]"
                elif x_intersection == 1 and y_intersection == 2:
                    displayed_text += "\n> [ref=trash]Dans la poubelle[/ref]"

                scene.display_text(displayed_text,
                                   on_store_click=lambda _: hide_in_the_store(),
                                   on_car_shop_click=lambda _: hide_in_the_car_shop(),
                                   on_trash_click=lambda _: hide_in_the_trash())

        def hide_in_the_store():
            game.wait_then(0, lambda _: scene.clear_text(), reset_timer=True)

            if x_intersection == 0:
                game.wait_then(0, lambda _: jey.sprite.play_animation('walkingright'))
                game.wait_then(0, lambda _: map_sprite.change_x_by_in_seconds(-325, 2))
                game.wait_then(2, lambda _: jey.sprite.stop_animation())
            elif x_intersection == 1:
                game.wait_then(0, lambda _: jey.sprite.play_animation('walkingleft'))
                game.wait_then(0, lambda _: map_sprite.change_x_by_in_seconds(325, 2))
                game.wait_then(2, lambda _: jey.sprite.stop_animation())

            game.wait_then(0, lambda _: jey.sprite.play_animation('walkingfromtheback'))
            game.wait_then(0, lambda _: jey.sprite.change_y_by_in_seconds(80, 2))
            game.wait_then(2, lambda _: jey.sprite.stop_animation())
            game.wait_then(0, lambda _: jey.sprite.set_opacity_to(0))
            game.wait_then(0, lambda _: black_screen.set_opacity_to_in_seconds(1, 2))
            game.wait_then(2, lambda _: game.play_song('assets/songs/second-meet-mr-anderson.mp3'))
            game.wait_then(73, lambda _: game.add_scene(party(game), 'party'))
            game.wait_then(0, lambda _: game.change_scene('party', True))

        def hide_in_the_car_shop():
            pass

        def hide_in_the_trash():
            pass

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

        if not jey.inventory.has('car'):
            map_sprite.set_position_to(-297, 654)
            jey.sprite.set_position_to(400, 433)
            bip2.sprite.set_position_to(525, 353)
            bip1.sprite.set_position_to(525, 433)
            bouncer.sprite.set_position_to(287, 433)

    scene.on('nightclub_black_screen_is_disappearing', on_black_screen_is_disappearing)

    def on_black_screen_end(_):
        dialog_duration = 5

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
            game.wait_then(0, lambda _: scene.display_text("T'abuses frère, t'aurais pu venir nous chercher en "
                                                           "voiture."), reset_timer=True)
            game.wait_then(dialog_duration, lambda _: scene.clear_text())

        game.wait_then(1, lambda _: scene.display_text("Ça va pas être possible pour vous ce soir les mecs. Veuillez "
                                                       "disposer.", bouncer.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text("T'es sérieux là ? Tu nous vires ?", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("Circulez s'il vous plait.", bouncer.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.clear_text())
        game.wait_then(0, lambda _: choice_node_9(on_choice_node_9_use_knife_click, on_choice_node_9_hit_click,
                                                  on_choice_node_9_flight_click))

    scene.on('nightclub_black_screen_end', on_black_screen_end)

    def choice_node_9(on_use_knife_click: Callable, on_hit_click: Callable, on_flight_click: Callable):
        displayed_text = """Que faire ?
> [ref=use_knife]Utiliser la couteau[/ref]
> [ref=hit]Frapper le vigile[/ref]
> [ref=flight]Prendre la fuite[/ref]"""

        scene.display_text(displayed_text,
                           on_use_knife_click=on_use_knife_click,
                           on_hit_click=on_hit_click,
                           on_flight_click=on_flight_click)

    def on_choice_node_9_use_knife_click(_):
        # TODO: use knife -> police -> game over
        pass

    def on_choice_node_9_hit_click(_):
        # TODO: hit -> police -> game over
        pass

    def on_choice_node_9_flight_click(_):
        take_flight()

    def show_chapter_title(_):
        chapter_sprite.set_opacity_to_in_seconds(1, 2)

    def hide_chapter_title_and_black_screen(_):
        chapter_sprite.set_opacity_to_in_seconds(0, 2)
        black_screen.set_opacity_to_in_seconds(0, 2)

    def on_scene_start(_):
        black_screen.set_position_to(black_screen.size[0] / 2, black_screen.size[1] / 2)
        black_screen.set_scale_to(5)
        chapter_sprite.set_position_to(chapter_sprite.size[0] / 2, chapter_sprite.size[1] / 2)

        game.play_song('assets/songs/first-meet-mr-anderson.mp3')
        game.wait_then(37, lambda _: game.stop_song(), reset_timer=True)
        game.wait_then(2, show_chapter_title)
        game.wait_then(0, lambda _: scene.emit('nightclub_black_screen_is_disappearing'))
        game.wait_then(5, hide_chapter_title_and_black_screen)
        game.wait_then(2, lambda _: scene.emit('nightclub_black_screen_end'))

    scene.on('nightclub_start', on_scene_start)

    return scene
