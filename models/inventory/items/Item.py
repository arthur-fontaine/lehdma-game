from abc import ABC


class Item(ABC):
    def __init__(self, name):
        self.name = name
