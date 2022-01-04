from typing import Callable

from lib.game.Game import Game, Scene, Sprite
from models.inventory.items.MoneyEnvelope import MoneyEnvelope
from scenes.car_shop.car_shop import car_shop
from scenes.nightclub.nightclub import nightclub
from sprites.jey.jey import jey
from sprites.mom.mom import mom
from utils.load_map import load_map


def moms_house(game: Game):
    scene = Scene()

    map_sprite = load_map(game, 'assets/map/buildings/jey-house/jey-house.png', 1)
    scene.add_sprite(map_sprite)

    pillow = Sprite('assets/objects/pillow.png')
    scene.add_sprite(pillow)

    jey.build_jey(game)
    scene.add_sprite(jey.sprite)

    mom.build_mom(game)
    scene.add_sprite(mom.sprite)

    black_screen = Sprite('assets/black-screen.png')
    scene.add_sprite(black_screen)

    chapter_sprite = Sprite('assets/chapters-title/chapter-1.png')
    chapter_sprite.set_opacity_to(0)
    scene.add_sprite(chapter_sprite)

    on_choice_node_2_mom_bedroom_click_animation_go_to_the_door = True

    def on_black_screen_is_disappearing(_):
        pillow.set_opacity_to(0)
        pillow.set_scale_to(0.125)

        jey.sprite.set_scale_to(0.25)
        jey.sprite.set_position_to(jey.sprite.size[0] / 2, jey.sprite.size[1] / 2)
        jey.sprite.change_x_by(233)

        mom.sprite.set_scale_to(0.25)
        mom.sprite.set_position_to(mom.sprite.size[0] / 2, mom.sprite.size[1] / 2)
        mom.sprite.change_x_by(-100)
        mom.sprite.switch_costume('right')

        map_sprite.set_position_to(map_sprite.size[0] / 2, map_sprite.size[1] / 2)

    scene.on('moms_house_black_screen_is_disappearing', on_black_screen_is_disappearing)

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

    scene.on('moms_house_black_screen_end', on_black_screen_end)

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
        jey_get_up()
        choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                      on_choice_node_2_mom_bedroom_click)

    def on_choice_node_1_dont_move_click(_):
        scene.clear_text()
        choice_node_7(on_choice_node_7_throw_pillow_click, on_choice_node_7_shout_click)

    def jey_get_up():
        jey.sprite.change_x_by(-155)

    def jey_go_to_the_door(reset_timer=True):
        jey.sprite.set_x_to(478)
        jey.sprite.play_animation('walkingfromtheback')
        game.wait_then(0, lambda _: jey.sprite.change_y_by_in_seconds(100, 1.5), reset_timer=reset_timer)
        game.wait_then(1.5, lambda _: jey.sprite.set_opacity_to(0))
        game.wait_then(0, lambda _: jey.sprite.stop_animation())

    def choice_node_2(on_car_shop_click: Callable, on_friends_click: Callable, on_mom_bedroom_click: Callable):
        displayed_text = """Où voulez-vous aller?
> [ref=car_shop]Concessionaire[/ref]
> [ref=friends]Amis[/ref]"""

        if not jey.inventory.has('money_envelope'):
            displayed_text += """
> [ref=mom_bedroom]Chambre de maman[/ref]"""

        scene.display_text(displayed_text,
                           on_car_shop_click=on_car_shop_click,
                           on_friends_click=on_friends_click,
                           on_mom_bedroom_click=on_mom_bedroom_click)

    def on_choice_node_2_car_shop_click(_):
        scene.clear_text()
        jey_go_to_the_door()
        game.wait_then(0, lambda _: game.add_scene(car_shop(game), 'car_shop'))
        game.wait_then(0, lambda _: game.change_scene('car_shop', True))

    def on_choice_node_2_friends_click(_):
        scene.clear_text()
        game.wait_then(0, lambda _: jey_go_to_the_door())
        game.wait_then(0, lambda _: black_screen.set_opacity_to_in_seconds(1, 2))
        game.wait_then(2, lambda _: game.add_scene(nightclub(game), 'nightclub'))
        game.wait_then(0, lambda _: game.change_scene('nightclub', True))

    def on_choice_node_2_mom_bedroom_click(_):
        scene.clear_text()

        jey_go_to_the_door()

        displayed_text = """Vous récupérez une enveloppe pleine d'argent !"""
        jey.inventory.add_items(MoneyEnvelope())
        game.wait_then(3, lambda _: scene.display_text(displayed_text))

        game.wait_then(0, lambda _: jey.sprite.set_opacity_to(1))
        game.wait_then(0, lambda _: jey.sprite.play_animation('walkforward'))
        game.wait_then(0, lambda _: jey.sprite.change_y_by_in_seconds(-100, 1.5))
        game.wait_then(1.5, lambda _: jey.sprite.stop_animation())

        game.wait_then(5, lambda _: choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                                                  on_choice_node_2_mom_bedroom_click))

    def choice_node_7(on_throw_pillow_click: Callable, on_shout_click: Callable):
        game.wait_then(0, lambda _: scene.display_text("""\"Tu vas sortir oui ?!\""""), reset_timer=True)

        displayed_text = """Que faire ?
>[ref=throw_pillow]Lancer un coussin[/ref]
>[ref=shout]Crier en retour[/ref]"""

        game.wait_then(5, lambda _: scene.display_text(displayed_text,
                                                       on_throw_pillow_click=on_throw_pillow_click,
                                                       on_shout_click=on_shout_click))

    def on_choice_node_7_throw_pillow_click(_):
        scene.clear_text()

        pillow.set_opacity_to(1)
        pillow.set_position_to(jey.sprite.x + jey.sprite.size[0] / 2, jey.sprite.y + jey.sprite.size[1])
        game.wait_then(0, lambda _: pillow.go_to_in_seconds(mom.sprite.x + pillow.size[0] * 2, mom.sprite.y, 0.25),
                       reset_timer=True)

        displayed_text = """Elle sursaute et se met à crier plus fort."""
        game.wait_then(1, lambda _: scene.display_text(displayed_text))
        game.wait_then(5, lambda _: choice_node_8(on_choice_node_8_stay_click, on_choice_node_8_leave_click))

    def on_choice_node_7_shout_click(_):
        scene.clear_text()

        displayed_text = """Vous criez en retour. Vous êtes énervé et vous voulez sortir."""
        game.wait_then(0, lambda _: scene.display_text(displayed_text), reset_timer=True)
        game.wait_then(0, lambda _: jey.sprite.set_x_to(478))
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
        displayed_text = """Vous prenez une gifle. Vous êtes énervé et vous voulez sortir."""
        game.wait_then(0, lambda _: scene.display_text(displayed_text), reset_timer=True)
        game.wait_then(5, lambda _: choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                                                  on_choice_node_2_mom_bedroom_click))

    def on_choice_node_8_leave_click(_):
        scene.clear_text()
        displayed_text = """Vous sortez de la maison. Au passage, vous récupérez une enveloppe pleine d'argent dans la 
chambre de votre mère."""
        jey.inventory.add_items(MoneyEnvelope())
        game.wait_then(0, lambda _: jey_get_up(), reset_timer=True)
        game.wait_then(0, lambda _: jey_go_to_the_door())
        game.wait_then(0, lambda _: scene.display_text(displayed_text))
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

        game.wait_then(2, show_chapter_title, reset_timer=True)
        game.wait_then(0, lambda _: scene.emit('moms_house_black_screen_is_disappearing'))
        game.wait_then(5, hide_chapter_title_and_black_screen)
        game.wait_then(2, lambda _: scene.emit('moms_house_black_screen_end'))

    def on_from_car_shop(_):
        # FIXME: jey does not appear

        jey.sprite.set_position_to(478, 300)
        mom.sprite.set_position_to(300, 300)
        jey.sprite.set_opacity_to(1)

        black_screen.set_position_to(black_screen.size[0] / 2, black_screen.size[1] / 2)
        black_screen.set_scale_to(5)
        black_screen.set_opacity_to(1)

        game.wait_then(2, lambda _: black_screen.set_opacity_to_in_seconds(0, 2), reset_timer=True)
        game.wait_then(2, lambda _: choice_node_2(on_choice_node_2_car_shop_click, on_choice_node_2_friends_click,
                                                  on_choice_node_2_mom_bedroom_click))

    scene.on('moms_house_start', on_scene_start)
    scene.on('moms_house_from_car_shop', on_from_car_shop)

    return scene
