from decks.deck import Deck
from decks.io import load_deck_from_txt, fetch_card_data, create_card_from_data, load_deck_from_json
import cards.card

commander_name, deck_list = load_deck_from_txt("./rawDecks/Davros2.txt")

commander = fetch_card_data(commander_name)

print(commander["color_identity"])
print(commander["type"])
print(commander["subtypes"])

commander=create_card_from_data(commander)

deck= Deck(commander=commander)

for card in deck_list:
    cardToAdd=create_card_from_data(fetch_card_data(card))
    deck.add_card(cardToAdd)

deck3=deck.copy()
deck.shuffle()

print(deck.getNumOfCardsInLibrary())
var=deck.draw(7)


for card in var:
    print(card.getName())

print(deck.getNumOfCardsInLibrary())

deck2=deck.copy()

print("deck2: " +str(deck2.getNumOfCardsInLibrary()))
print("deck3: " +str(deck3.getNumOfCardsInLibrary()))