import re
import json
import urllib.parse
import requests

from cards.card import Card
from cards.creatures import Creature

def load_deck_from_txt(filepath):
    deck_list = []
    commander = None
    section = None

    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line == "Commander":
                section = "commander"
                continue
            elif line == "Deck":
                section = "deck"
                continue

            match = re.match(r"(\d+) (.*)", line)
            if match:
                count = int(match.group(1))
                card_name = match.group(2)
                if section == "commander":
                    commander = card_name
                elif section == "deck":
                    for _ in range(count):
                        deck_list.append(card_name)
    return commander, deck_list

def get_card_data_from_scryfall(card_name):
    """Pobiera wybrane dane karty z API Scryfall po jej nazwie."""

    encoded_card_name = urllib.parse.quote_plus(card_name)
    url = f"https://api.scryfall.com/cards/named?fuzzy={encoded_card_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        card_data = response.json()

        # Tworzymy nowy słownik tylko z potrzebnymi polami
        extracted_data = {
            "name": card_data.get("name"),
            "mana_cost": card_data.get("mana_cost"),
            "cmc": card_data.get("cmc"),
            "type_line": card_data.get("type_line"),
            "oracle_text": card_data.get("oracle_text"),
            "colors": card_data.get("colors"),
            "color_identity": card_data.get("color_identity"),
            "keywords": card_data.get("keywords"),
            "legalities": card_data.get("legalities", {}).get("commander"), # Bezpieczny dostęp do legalities
            "rarity": card_data.get("rarity"),
            "image_uris": card_data.get("image_uris", {}).get("normal") # Bezpieczny dostęp do image_uris
        }

        # Warunkowe dodawanie power i toughness
        if "Creature" in card_data.get("type_line", ""): # Sprawdzamy, czy type_line istnieje
            extracted_data["power"] = card_data.get("power")
            extracted_data["toughness"] = card_data.get("toughness")

        return extracted_data

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych z API Scryfall: {e}")
        if response is not None and response.status_code == 404: # Dodana obsługa braku response
            print("Prawdopodobnie nie znaleziono karty o podanej nazwie.")
        return None
    except json.JSONDecodeError as e:
        print(f"Błąd dekodowania JSON: {e}")
        return None
    except AttributeError as e: #Dodana obsługa braku danych w jsonie
        print(f"Brak danych w zwróconym JSON: {e}")
        return None

def fetch_card_data(card_name):
    """Pobiera dane karty ze Scryfall i zwraca SŁOWNIK z danymi.""" # Important change in Docstring
    card_data = get_card_data_from_scryfall(card_name)

    if card_data:
        type_line = card_data.get("type_line")
        subtypes = []
        if type_line:
            parts = type_line.split("—")
            if len(parts) > 1:
                subtypes = [s.strip() for s in parts[1].split()]
        card_type = type_line.split("—")[0] if type_line else None #Handle cards without type_line



            # Zwracamy słownik z danymi
        return {
            "name": card_data.get("name"),
            "mana_cost": card_data.get("mana_cost"),
            "cmc": card_data.get("cmc"),
            "type": card_type,
            "subtypes": subtypes,
            "text": card_data.get("oracle_text"),
            "power": card_data.get("power"),
            "toughness": card_data.get("toughness"),
            "colors": card_data.get("colors"),
            "color_identity": card_data.get("color_identity"),
            "keywords": card_data.get("keywords"),
            "rarity": card_data.get("rarity"),
            "image_uri": card_data.get("image_uris"),
            "legalities_commander": card_data.get("legalities")
        }
    else:
        return None

def create_card_from_data(card_data):
    """Creates a Card object from a dictionary of card data."""
    if card_data is None:
        return None
    try:
        return Card(
            name=card_data.get("name"),
            mana_cost=card_data.get("mana_cost"),
            cmc=card_data.get("cmc"),
            card_type=card_data.get("type"),
            subtypes=card_data.get("subtypes"),
            oracle_text=card_data.get("text"),
            power=card_data.get("power"),
            toughness=card_data.get("toughness"),
            colors=card_data.get("colors"),
            color_identity=card_data.get("color_identity"),
            keywords=card_data.get("keywords"),
            rarity=card_data.get("rarity"),
            image_uri=card_data.get("image_uri"),
            legalities_commander=card_data.get("legalities", {}).get("commander") #Safe Access
        )
    except Exception as e:
        print(f"Error creating card: {e}, Data: {card_data}")
        return None

def save_deck_to_json(deck, filepath):
    deck_data = []
    for card in deck.cards:
        deck_data.append(card.__dict__())
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(deck_data, file, indent=4, ensure_ascii=False)

def load_deck_from_json(filepath):
    deck = Deck()
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            card_data_list = json.load(file)
            for card_data in card_data_list:
                card_type = card_data.pop('card_type')
                if card_type == "Creature":
                    card = Creature(**card_data)
                else:
                    card = Card(card_data['name'], card_data['cost'], card_type, card_data.get('subtypes'), card_data.get('text'))
                deck.add_card(card)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {filepath}")
    except json.JSONDecodeError:
        print(f"Błąd dekodowania JSON w pliku: {filepath}")
    return deck