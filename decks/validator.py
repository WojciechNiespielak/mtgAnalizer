def validate_deck(commander, deck):
    if not commander:
        return "Brak Commandera w pliku."

    if len(deck) != 99:
        return "Talia musi zawierać 99 kart (bez Commandera)."

    card_counts = {}
    for card in deck:
        card_counts[card["name"]] = card_counts.get(card["name"], 0) + 1

    for name, count in card_counts.items():
        is_basic_land = False
        for card in deck:
            if card["name"] == name and "Basic Land" in card.get("type_line", ""):
                is_basic_land = True
                break
        if count > 1 and not is_basic_land:
            return f"Karta {name} występuje więcej niż raz (z wyjątkiem Basic Lands)."

    return None