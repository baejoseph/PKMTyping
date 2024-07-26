import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

def get_korean_pokemon_names():
    url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Korean_Pokémon_names"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table", class_="roundy")

    # List to hold all the Pokemon names
    pokemon_names = []

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) > 3:  # Ensure there are enough columns
                english_name = columns[2].text.strip()
                korean_name = columns[3].text.strip()
                pokemon_names.append((english_name, korean_name))

    # Convert to DataFrame
    df = pd.DataFrame(pokemon_names, columns=["English", "Korean"])
    return df




if __name__=="__main__":

    pokemon_names_df = get_korean_pokemon_names()
    
    # Load your JSON file
    with open("pokedex.json", "r", encoding="utf-8") as file:
        pokemon_data = json.load(file)
    
    # Update the JSON data with Korean names
    for pokemon in pokemon_data:
        english_name = pokemon["name"]["english"]
        korean_name = pokemon_names_df[pokemon_names_df["English"] == english_name]["Korean"].values
        if len(korean_name) > 0:
            pokemon["name"]["korean"] = korean_name[0]    
    
    # Save the updated JSON file
    with open("pokemon_data_updated.json", "w", encoding="utf-8") as file:
        json.dump(pokemon_data, file, ensure_ascii=False, indent=2)

    print("Updated JSON file with Korean names.")

    
    