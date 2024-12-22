import re

class Card:
    __slots__ = ["name", "mana_cost", "cmc", "card_type", "subtypes", "oracle_text", "power", "toughness", "colors", "color_identity", "keywords", "rarity", "image_uri", "legalities_commander","state","type","isEnteredTaped", "isManaGain", "manaGained","hasSummoningSicness"]
    def __init__(self, name, mana_cost, cmc, card_type, subtypes=None, oracle_text=None, power=None, toughness=None,
                 colors=None, color_identity=None, keywords=None, rarity=None, image_uri=None, legalities_commander=None ):
        """
        Initializes a Card object with all relevant fields.

        Args:
            name (str): The name of the card.
            mana_cost (str): The mana cost of the card, using MTG notation (e.g., "{1}{B}").
            cmc (int): The converted mana cost of the card.
            card_type (str): The main type of the card (e.g., "Creature", "Instant").
            subtypes (list, optional): A list of card subtypes (e.g., ["Goblin", "Warrior"]). Defaults to None.
            oracle_text (str, optional): The complete Oracle text of the card. Defaults to None.
            power (int, optional): The power of the card (applicable to creatures only). Defaults to None.
            toughness (int, optional): The toughness of the card (applicable to creatures only). Defaults to None.
            colors (list, optional): A list of colors the card belongs to (e.g., ["Red", "Black"]). Defaults to None.
            color_identity (list, optional): A list of colors the card's mana cost can produce. Defaults to None.
            keywords (list, optional): A list of keywords the card has (e.g., ["Flying", "Haste"]). Defaults to None.
            rarity (str, optional): The rarity of the card (e.g., "Common", "Rare", "Mythic Rare"). Defaults to None.
            image_uri (str, optional): The URL of the card's image. Defaults to None.
            legalities_commander (dict, optional): A dictionary containing Commander legality information. Defaults to None.
        """
        self.state = "Library"
        self.name = name
        self.mana_cost = mana_cost
        self.cmc = cmc
        self.type = card_type  # Use "type" instead of "card_type" for consistency with MTG terminology
        self.subtypes = subtypes or []
        self.oracle_text = oracle_text
        self.power = power
        self.toughness = toughness
        self.colors = colors or []
        self.color_identity = color_identity or []
        self.keywords = keywords or []
        self.rarity = rarity
        self.image_uri = image_uri
        self.legalities_commander = legalities_commander
        self.isManaGain = False

        self.manaGained = {"isSingleOption": True, "manaType": []}
        if oracle_text:
            oracle_text_lower = oracle_text.lower()  # Sprowadzamy tekst do małych liter
        else:
            oracle_text_lower=""

        if "add" in oracle_text_lower:
            matches = re.findall(r"\{([0-9WUBRGC]+)\}", oracle_text)
            if matches:
                self.isManaGain = True
                self.manaGained["manaType"] = matches
                if any("or" in match for match in matches):  # Sprawdzamy, czy w którymś z dopasowań jest "or"
                    self.manaGained["isSingleOption"] = False

        if "enters tapped" in oracle_text_lower:  # Poprawione "taped" na "tapped"
            self.isEnteredTaped = True
        else:
            self.isEnteredTaped = False

        self.hasSummoningSicness = True

        if self.keywords: # Sprawdzamy, czy lista keywords nie jest pusta
            if any("haste" in keyword.lower() for keyword in self.keywords):
                self.hasSummoningSicness = False
        if "creature" not in card_type.lower():
            self.hasSummoningSicness = False

    def __repr__(self):
        return f"{self.name} ({self.mana_cost}) - {self.type}"

    def __dict__(self):
        return {
            'name': self.name,
            'mana_cost': self.mana_cost,
            'card_type': self.type,
            'subtypes': self.subtypes,
            'text': self.oracle_text
        }

    def getName(self):
        return self.name

    def getColorIdentity(self):
        return self.color_identity

    def getType(self):
        return self.type

    def getState(self):
        return self.state

    def setState(self, state):
        self.state=state

    def getCmc(self):
        return self.cmc

    def getCost(self):
        return self.mana_cost

    def getManaGain(self):
        return self.isManaGain

    def getManaGained(self):
        return self.manaGained

    def getEnterTapped(self):
        return self.isEnteredTaped

    def getHasSickness(self):
        return self.hasSummoningSicness