import random
import copy

class Deck:
    def __init__(self, commander=None, cards=None):
        self.commander = commander
        self.cards = cards or []
        if self.commander:
            self.add_card(self.commander) # Dodajemy dowódcę automatycznie do kart

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        try:
            self.cards.remove(card)
        except ValueError:
            print(f"Karta {card.name} nie znajduje się w talii.")

    def is_legal_commander_deck(self):
        if not self.commander:
            print("Błąd: Brak dowódcy w talii.")
            return False

        if "Legendary" not in self.commander.getType() or "Creature" not in self.commander.getType():
            print("Błąd: Dowódca musi być legendarną istotą (Legendary Creature).")
            return False
        else:
            print("Dowódca jest poprawny.")

        num_cards = len(self.cards) - 1  # bez commandera
        if num_cards != 99:
            print(f"Błąd: Talia powinna zawierać 99 kart (bez dowódcy). Obecnie zawiera {num_cards} kart.")
            return False
        else:
            print("Ilość kart jest poprawna.")

        card_names = [card.getName() for card in self.cards[1:]]  # bez commandera
        duplicates = []
        seen = set()

        for card in self.cards[1:]:  # Iterujemy po obiektach Card zamiast po nazwach
            if not (
                    "Land" in card.getType() and "Basic" in card.getType()):  # Sprawdzamy czy karta NIE jest basic landem
                if card.getName() in seen:
                    duplicates.append(card.getName())
                else:
                    seen.add(card.getName())

        if duplicates:
            print(f"Błąd: Talia zawiera duplikaty kart (poza basic landami): {duplicates}")
            return False
        else:
            print("Karty są unikalne.")

        commander_colors = self.commander.getColorIdentity()
        for card in self.cards[1:]:  # bez commandera
            card_colors = card.getColorIdentity()
            card_type = card.getType()
            if not set(card_colors).issubset(set(commander_colors)):
                if not ("Land" in card_type and "Basic" in card_type):  # Wyjątek dla bazowych lądów
                    print(f"Błąd: Karta '{card.getName()}' ma tożsamość kolorów niezgodną z dowódcą. Tożsamość dowódcy: {commander_colors}, tożsamość karty: {card_colors}")
                    return False
        print("Tożsamość kolorów kart jest zgodna z dowódcą.")
        return True

    def __repr__(self):
        if self.commander:
            return f"Dowódca: {self.commander.getName()}\nKarty:\n" + "\n".join(map(str, self.cards[1:]))
        else:
            return "Talia bez dowódcy.\nKarty:\n" + "\n".join(map(str, self.cards))

    def shuffle(self):
        if any(card.getState() != "Library" for card in self.cards[1:] if self.commander):
            print("Brak kart.")
            return

        cards_without_commander = self.cards[1:] if self.commander else self.cards
        random.shuffle(cards_without_commander)
        if self.commander:
            self.cards = [self.commander] + cards_without_commander
        else:
            self.cards = cards_without_commander

    def draw(self, num_cards):

        available_cards = [card for card in self.cards[1:] if card.state == "Library"] if self.commander else [card for
                                                                                                               card in
                                                                                                               self.cards
                                                                                                               if
                                                                                                               card.state == "Library"]
        num_cards_to_draw = min(num_cards, len(available_cards))  # Limit draw to available cards

        if not num_cards_to_draw:
            print(f"Talia nie zawiera wystarczającej liczby kart do dobrania {num_cards} kart.")
            return []

        drawn_cards = [card for card in available_cards[:num_cards_to_draw]]  # Efficiently slice available cards
        for card in drawn_cards:
            card.setState("Hand")  # Set state of each drawn card

        del self.cards[1:1 + num_cards_to_draw]  # Efficiently remove drawn cards from deck

        return drawn_cards

    def getNumOfCardsInLibrary(self):
        available_cards = len([card for card in self.cards[1:] if card.state == "Library"])

        return available_cards

    def copy(self):
        """Creates a deep copy of the Deck object."""
        new_deck = Deck(self.commander)
        new_deck.cards = [copy.deepcopy(card) for card in self.cards]
        return new_deck