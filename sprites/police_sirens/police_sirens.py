import math

from lib.game.Game import Game, Scene, Sprite


def show_police_sirens(game: Game, blue_police_siren: Sprite, red_police_siren: Sprite, duration: float = 5,
                       siren_duration: float = 1):
    blue_police_siren.set_position_to(218, blue_police_siren.size[1] / 2)
    red_police_siren.set_position_to(618, red_police_siren.size[1] / 2)

    sirens_number = math.floor(duration / siren_duration)

    for i in range(sirens_number):
        game.wait_then(0, lambda _: blue_police_siren.set_opacity_to_in_seconds(1, siren_duration / 2))
        game.wait_then(siren_duration / 4, lambda _: red_police_siren.set_opacity_to_in_seconds(1, siren_duration / 2))
        game.wait_then(0, lambda _: blue_police_siren.set_opacity_to_in_seconds(0, siren_duration / 2))
        game.wait_then(siren_duration / 4, lambda _: red_police_siren.set_opacity_to_in_seconds(0, siren_duration / 2))
