from lib.game.Game import Sprite, Game
from utils.load_costumes import load_costumes


def load_sprite(game: Game, character_name: str):
    sprite_directory = f"assets/characters/{character_name}"

    sprite = Sprite(f'{sprite_directory}/{character_name}-default.png')

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
            sprite.create_animation(costume_by_type, costumes_by_type[costume_by_type], True,
                                    len(costumes_by_type[costume_by_type]) * 0.5)

    return sprite
