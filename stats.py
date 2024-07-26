import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load JSON data
with open("pokemon_data_updated.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    
plt.figure(figsize=(10, 6))
stats = ["HP", "Speed", 'Defense', "Attack", "Sp. Attack"]
values = {}
for stat in stats:
    
    # Extract values
    values[stat] = [pokemon['base'][stat] for pokemon in data[:151]]

# Create a DataFrame
df = pd.DataFrame(values)
df["HPAttack"] = df.HP + df.Attack + df["Sp. Attack"]

stat = "HPAttack"
# Create the plot

sns.histplot(data=df, x=stat, kde=True)
plt.title(f'Distribution of Pokemon {stat} Values')
plt.xlabel(stat)
plt.ylabel('Count')
plt.legend()
# Show the plot
plt.show()
    