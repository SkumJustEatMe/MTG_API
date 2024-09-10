import requests
import json
from datetime import datetime

def fetch_all_cards_in_set(url):
    all_cards = []
    
    while url:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            all_cards.extend(data['data'])  # Add the current page of cards to the list
            
            # Check if there is another page
            url = data.get('next_page')
        else:
            print(f"Error: {response.status_code}")
            break
    
    return all_cards

def store_price_history(card_data):
    price_entries = []
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    for card in card_data:
        if 'prices' in card:
            prices = card['prices']
            price_entry = {
                "date": date_str,
                "name": card['name'],
                "prices": {
                    "eur": prices.get('eur'),
                    "eur_foil": prices.get('eur_foil')
                }
            }
            price_entries.append(price_entry)
    
    # Append price entries to a file (or store in a database)
    with open("price_history.json", "a") as file:
        for entry in price_entries:
            json.dump(entry, file)
            file.write("\n")

# URL to fetch all cards in the DMU set
set_code = "dmu"
url = f"https://api.scryfall.com/cards/search?order=set&q=e%3A{set_code}&unique=prints"

# Fetch all cards in the DMU set
cards = fetch_all_cards_in_set(url)

# Print out the name and EUR prices of each card
for card in cards:
    if 'prices' in card:
        prices = card['prices']
        print(f"{card['name']}: EUR Price: {prices['eur']}")
        print(f"{card['name']}: EUR Foil Price: {prices['eur_foil']}")
    else:
        print(f"{card['name']}: No price data available.")

# Store the current prices in a file
store_price_history(cards)
