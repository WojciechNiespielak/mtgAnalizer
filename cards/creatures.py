from cards.card import Card

class Creature(Card):
    def __init__(self, name, cost, power, toughness, subtypes=None, text=None):
        super().__init__(name, cost, "Creature", subtypes, text)
        self.power = power
        self.toughness = toughness

    def __repr__(self):
        return f"{super().__repr__()} - {self.power}/{self.toughness}"

    def __dict__(self):
        base_dict = super().__dict__()
        base_dict.update({
            'power': self.power,
            'toughness': self.toughness
        })
        return base_dict