from models.Character import Character
from models.Choice import ChoiceNode
from models.Map import Map


class Scene:
    def __init__(self, name: str, characters: list[Character], choices: list[ChoiceNode], scene_map: Map):
        self.name = name
        self.characters = characters
        self.choices = choices
        self.map = scene_map
