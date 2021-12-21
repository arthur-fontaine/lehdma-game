from typing import Callable

from kivy.clock import Clock

from lib.game.Game import Sprite, Game
from utils.load_costumes import load_costumes


def load_sprite(game: Game, character_name: str):
    sprite_directory = f"assets/characters/{character_name}"

    sprite = Sprite(f'{sprite_directory}/{character_name}.png')

    costumes = load_costumes(sprite_directory)
    costumes_by_type = {}

    for costume_name, costume_path in costumes.items():
        sprite.add_costume(costume_name, costume_path)
        if costume_name.split('-')[0] in costumes_by_type:
            costumes_by_type[costume_name.split('-')[0]].append(costume_name)
        else:
            costumes_by_type[costume_name.split('-')[0]] = [costume_name]

    for costume_by_type in costumes_by_type:
        if len(costumes_by_type[costume_by_type]) > 1:
            def animate_sprite(cbt):
                for costume in costumes_by_type[cbt]:
                    current_costume = sprite.costume_name

                    if cbt not in current_costume:
                        current_costume = costumes_by_type[cbt][0]

                    if costume == current_costume:
                        try:
                            next_costume = costumes_by_type[cbt][
                                costumes_by_type[cbt].index(current_costume) + 1]
                        except IndexError:
                            next_costume = costumes_by_type[cbt][0]
                        sprite.switch_costume(next_costume)
                        break

            def build_callback(cbt):
                def cb(_): animate_sprite(cbt)
                return cb

            def schedule_interval(cb: Callable, interval: float):
                def cbi(_): Clock.schedule_interval(cb, interval)
                return cbi

            def unschedule_interval(cb: Callable):
                def uncbi(_): Clock.unschedule(cb)
                return uncbi

            animation_duration = 0.5
            callback = build_callback(costume_by_type)
            schedule_interval_callback = schedule_interval(callback, animation_duration)
            unschedule_interval_callback = unschedule_interval(callback)

            if 'left' in costume_by_type:
                sprite.on('keydown_a', schedule_interval_callback, animation_duration)
                sprite.on('keyup_a', unschedule_interval_callback, animation_duration)
            if 'right' in costume_by_type:
                sprite.on('keydown_d', schedule_interval_callback, animation_duration)
                sprite.on('keyup_d', unschedule_interval_callback, animation_duration)
            if 'fromtheback' in costume_by_type:
                sprite.on('keydown_w', schedule_interval_callback, animation_duration)
                sprite.on('keyup_w', unschedule_interval_callback, animation_duration)
            if 'forward' in costume_by_type:
                sprite.on('keydown_s', schedule_interval_callback, animation_duration)
                sprite.on('keyup_s', unschedule_interval_callback, animation_duration)

    return sprite
