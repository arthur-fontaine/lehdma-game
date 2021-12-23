from models.inventory.items.Item import Item


class Car(Item):
    def __init__(self):
        super().__init__('car')
