from typing import Callable

from lib.game.Game import Game, Scene, Sprite
from models.inventory.items.MoneyEnvelope import MoneyEnvelope
from scenes.car_shop.car_shop import car_shop
from sprites.jey.jey import jey
from sprites.mom.mom import mom
from utils.load_map import load_map


def moms_house(game: Game):
    scene = Scene()

    map_sprite = load_map(game, 'assets/map/buildings/jey-house/jey-house.png', 1)
    scene.add_sprite(map_sprite)

    jey.build_jey(game)
    scene.add_sprite(jey.sprite)

    mom.build_mom(game)
    scene.add_sprite(mom.sprite)

    black_screen = Sprite('assets/black-screen.png')
    scene.add_sprite(black_screen)

    chapter_sprite = Sprite('assets/chapters-title/chapter-1.png')
    chapter_sprite.set_opacity_to(0)
    scene.add_sprite(chapter_sprite)

    def on_black_screen_is_disappearing(_):
        jey.sprite.set_scale_to(0.25)
        jey.sprite.set_position_to(jey.sprite.size[0] / 2, jey.sprite.size[1] / 2)

        mom.sprite.set_scale_to(0.25)
        mom.sprite.set_position_to(mom.sprite.size[0] / 2, mom.sprite.size[1] / 2)
        mom.sprite.change_y_by(- mom.sprite.size[1] / 4)

        map_sprite.set_position_to(map_sprite.size[0] / 2 - 112, map_sprite.size[1] / 2)

    scene.on('black_screen_is_disappearing', on_black_screen_is_disappearing)

    def on_black_screen_end(_):
        dialog_duration = 5

        game.wait_then(0, lambda _: scene.display_text("""\"T'as vu l'heure ?\"""", mom.name), reset_timer=True)
        game.wait_then(dialog_duration, lambda _: scene.display_text("""\"Ouais, ouais, j'ai vu, ouais\"""", jey.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text("""\"Allez, lève toi, fais quelque chose, j'sais pas, pfff..\"""",
                                                    mom.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text(
            """\"Mais il fait froid dehors là, j'sais pas, j'suis pas chaud j'crois\"""", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("""\"Froid ? Mais nous, à l'époque, on marchait des kilomètres pour aller à l'école.
        On avait envie d'faire des choses. On avait envie d's'instruire,
        de rendre fiers nos parents\"""", mom.name))
        game.wait_then(dialog_duration,
                       lambda _: scene.display_text("""\"Ouais, tu dis tout l'temps la même, ouais...\"""", jey.name))
        game.wait_then(dialog_duration, lambda _: scene.display_text("""\" Ouais, bon, alors tu vas pas m'dire que c'est un p'tit vent de rien du tout qui
        va t'clouer au lit, hein. Roh, allez, bouge-toi, là !\"""", mom.name))
        game.wait_then(dialog_duration, lambda _: scene.clear_text())
        game.wait_then(0, lambda _: choice_node_1(on_choice_node_1_move_click, on_choice_node_1_dont_move_click))

    scene.on('black_screen_end', on_black_screen_end)

    def choice_node_1(on_move_click: Callable, on_dont_move_click: Callable):
        displayed_text = """Que faire?
> [ref=move]Bouger[/ref]
> [ref=dont_move]Rester[/ref]"""

        scene.display_text(displayed_text,
                           None,
                           on_move_click=on_move_click,
                           on_dont_move_click=on_dont_move_click)

    def on_choice_node_1_move_click(_):
        scene.clear_text()
        choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                      on_choice_node_2_mom_bedroom_click)

    def on_choice_node_1_dont_move_click(_):
        scene.clear_text()
        choice_node_7(on_choice_node_7_throw_book_click, on_choice_node_7_shout_click)

    def choice_node_2(on_car_shop_click: Callable, on_friends_click: Callable, on_mom_bedroom_click: Callable):
        displayed_text = """Où voulez-vous aller?
> [ref=car_shop]Concessionaire[/ref]
> [ref=friends]Amis[/ref]"""

        print(jey.inventory.has('money_envelope'))
        print(jey.inventory)

        if not jey.inventory.has('money_envelope'):
            displayed_text += """
> [ref=mom_bedroom]Chambre de maman[/ref]"""

        scene.display_text(displayed_text,
                           on_car_shop_click=on_car_shop_click,
                           on_friends_click=on_friends_click,
                           on_mom_bedroom_click=on_mom_bedroom_click)

    def on_choice_node_2_car_shop_click(_):
        scene.clear_text()
        game.change_scene(car_shop(game))

    def on_choice_node_2_friends_click(_):
        scene.clear_text()
        # TODO: friend's scene

    def on_choice_node_2_mom_bedroom_click(_):
        scene.clear_text()
        displayed_text = """Vous récupérez une enveloppe pleine d'argent !"""
        game.wait_then(0, lambda _: scene.display_text(displayed_text), reset_timer=True)
        game.wait_then(5, lambda _: choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                                                  on_choice_node_2_mom_bedroom_click))

    def choice_node_7(on_throw_book_click: Callable, on_shout_click: Callable):
        displayed_text = """Que faire ?
>[ref=throw_book]Lancer un livre[/ref]
>[ref=shout]Crier en retour[/ref]"""

        scene.display_text(displayed_text,
                           on_throw_book_click=on_throw_book_click,
                           on_shout_click=on_shout_click)

    def on_choice_node_7_throw_book_click(_):
        scene.clear_text()
        displayed_text = """Elle sursaute et se met à crier plus fort."""
        game.wait_then(0, lambda _: scene.display_text(displayed_text), reset_timer=True)
        game.wait_then(5, lambda _: choice_node_8(on_choice_node_8_stay_click, on_choice_node_8_leave_click))
        # TODO: book throw

    def on_choice_node_7_shout_click(_):
        scene.clear_text()
        displayed_text = """Vous criez en retour et vous faites gifler. Vous sortez énervé."""
        game.wait_then(0, lambda _: scene.display_text(displayed_text), reset_timer=True)
        game.wait_then(5, lambda _: choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                                                  on_choice_node_2_mom_bedroom_click))

    def choice_node_8(on_stay_click: Callable, on_leave_click: Callable):
        displayed_text = """Partir ?
>[ref=stay]Rester[/ref]
>[ref=leave]Partir[/ref]"""

        scene.display_text(displayed_text,
                           on_stay_click=on_stay_click,
                           on_leave_click=on_leave_click)

    def on_choice_node_8_stay_click(_):
        scene.clear_text()
        displayed_text = """Vous prenez une gifle et décidez de sortir."""
        game.wait_then(0, lambda _: scene.display_text(displayed_text), reset_timer=True)
        game.wait_then(5, lambda _: choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                                                  on_choice_node_2_mom_bedroom_click))

    def on_choice_node_8_leave_click(_):
        scene.clear_text()
        displayed_text = """Vous sortez de la maison et récupérez une enveloppe pleine d'argent."""
        jey.inventory.add_items(MoneyEnvelope())
        game.wait_then(0, lambda _: scene.display_text(displayed_text), reset_timer=True)
        game.wait_then(5, lambda _: choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                                                  on_choice_node_2_mom_bedroom_click))

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
