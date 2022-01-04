from typing import Callable

from lib.game.Game import Game, Scene, Sprite
from models.inventory.items.Car import Car
from models.inventory.items.Knife import Knife
from scenes.nightclub.nightclub import nightclub
from sprites.car_dealer.car_dealer import car_dealer
from sprites.jey.jey import jey
from utils.load_map import load_map


def car_shop(game: Game):
    scene = Scene()

    map_sprite = load_map(game, 'car_shop', 'assets/map/map.png')
    scene.add_sprite(map_sprite)

    jey.build_jey(game)
    scene.add_sprite(jey.sprite)

    car_dealer.build_car_dealer(game)
    scene.add_sprite(car_dealer.sprite)

    black_screen = Sprite('assets/black-screen.png')
    scene.add_sprite(black_screen)

    chapter_sprite = Sprite('assets/chapters-title/chapter-2.png')
    chapter_sprite.set_opacity_to(0)
    scene.add_sprite(chapter_sprite)

    def on_black_screen_is_disappearing(_):
        jey.sprite.set_scale_to(0.25)
        jey.sprite.set_position_to(jey.sprite.size[0] / 2, jey.sprite.size[1] / 2)

        car_dealer.sprite.set_scale_to(0.25)
        car_dealer.sprite.set_position_to(car_dealer.sprite.size[0] / 2, car_dealer.sprite.size[1] / 2)
        car_dealer.sprite.change_y_by(- car_dealer.sprite.size[1] / 4)

        map_sprite.set_position_to(map_sprite.size[0] / 2 - 112, map_sprite.size[1] / 2)

    scene.on('car_shop_black_screen_is_disappearing', on_black_screen_is_disappearing)

    def choice_node_3(on_yes_click: Callable, on_no_click: Callable):
        displayed_text = """Veux-tu retourner chez ta mère ?
 > [ref=yes]Oui[/ref]
 > [ref=no]Non[/ref]"""

        scene.display_text(displayed_text,
                           on_yes_click=on_yes_click,
                           on_no_click=on_no_click)

    def on_choice_node_3_yes_click(_):
        scene.clear_text()
        game.wait_then(0, lambda _: black_screen.set_opacity_to_in_seconds(1, 2), reset_timer=True)
        game.wait_then(2, lambda _: game.change_scene('moms_house', 'moms_house_from_car_shop'))

    def on_choice_node_3_no_click(_):
        scene.clear_text()
        choice_node_6(on_choice_node_6_steal_click, on_choice_node_6_hit_click)

    def choice_node_4(on_make_a_deal_click: Callable, on_get_angry_click: Callable):
        displayed_text = """\"Avec si peu vous ne pourrez rien vous permettre.\"
 > [ref=make_a_deal]\"On peut s'arranger\"[/ref]
 > [ref=get_angry]S'énerver[/ref]"""

        scene.display_text(displayed_text,
                           on_make_a_deal_click=on_make_a_deal_click,
                           on_get_angry_click=on_get_angry_click)

    def on_choice_4_make_a_deal_click(_):
        scene.clear_text()
        choice_node_5(on_choice_node_5_yes_click, on_choice_node_5_no_click)

    def on_choice_4_get_angry_click(_):
        scene.clear_text()
        choice_node_6(on_choice_node_6_steal_click, on_choice_node_6_hit_click)

    def choice_node_5(on_yes_click: Callable, on_no_click: Callable):
        displayed_text = """\"J'ai bien quelque chose à vous proposer, mais avez-vous le coeur pur ?\"
 > [ref=yes]Oui[/ref]
 > [ref=no]Non[/ref]"""

        scene.display_text(displayed_text,
                           on_yes_click=on_yes_click,
                           on_no_click=on_no_click)

    def on_choice_node_5_yes_click(_):
        scene.clear_text()
        jey.inventory.add_items(Car(), Knife())
        game.wait_then(0, lambda _: black_screen.set_opacity_to_in_seconds(1, 2), reset_timer=True)
        game.wait_then(2, lambda _: game.add_scene(nightclub(game), 'nightclub'))
        game.wait_then(0, lambda _: game.change_scene('nightclub', True))

    def on_choice_node_5_no_click(_):
        scene.clear_text()
        choice_node_6(on_choice_node_6_steal_click, on_choice_node_6_hit_click)

    def choice_node_6(on_steal_click: Callable, on_hit_click: Callable):
        displayed_text = """Que faire ?
 > [ref=steal]Voler la voiture[/ref]
 > [ref=hit]Courir et frapper le vendeur[/ref]"""

        scene.display_text(displayed_text,
                           on_steal_click=on_steal_click,
                           on_hit_click=on_hit_click)

    def on_choice_node_6_steal_click(_):
        scene.clear_text()

        jey.sprite.play_animation('walkingfromtheback')
        jey.sprite.change_y_by_in_seconds(100, 5)
        game.wait_then(5, lambda _: jey.sprite.stop_animation(), reset_timer=True)

        car_dealer.sprite.play_animation('walkingfromtheback')
        car_dealer.sprite.change_y_by_in_seconds(jey.sprite.pos[1] - car_dealer.sprite.pos[1] + 100, 5)
        game.wait_then(5, lambda _: car_dealer.sprite.stop_animation(), reset_timer=True)

        # TODO: gets picked up by the police

    def on_choice_node_6_hit_click(_):
        scene.clear_text()
        # TODO: hit the car dealer

    def on_black_screen_end(_):
        if not jey.inventory.has('money_envelope'):
            choice_node_3(on_choice_node_3_yes_click, on_choice_node_3_no_click)
        else:
            choice_node_4(on_choice_4_make_a_deal_click, on_choice_4_get_angry_click)

    scene.on('car_shop_black_screen_end', on_black_screen_end)

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
        game.wait_then(0, lambda _: scene.emit('car_shop_black_screen_is_disappearing'))
        game.wait_then(5, hide_chapter_title_and_black_screen)
        game.wait_then(2, lambda _: scene.emit('car_shop_black_screen_end'))

    scene.on('car_shop_start', on_scene_start)

    return scene
