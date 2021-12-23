from typing import Optional

from models.inventory.items.Item import Item


class Inventory:
    def __init__(self, inventory: Optional[list[Item]] = None):
        if inventory is None:
            inventory = []

        self.inventory = inventory

    def add_items(self, *items: Item):
        for item in items:
            self.inventory.append(item)

    def get_item(self, name: str) -> Optional[Item]:
        for item in self.inventory:
            if item.name == name:
                return item
        return None

    def has(self, name: str) -> bool:
        for item in self.inventory:
            if item.name == name:
                return True
        return False
