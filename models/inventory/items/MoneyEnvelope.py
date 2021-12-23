from models.inventory.items.Item import Item


class MoneyEnvelope(Item):
    def __init__(self):
        super().__init__('money_envelope')
