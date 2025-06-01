import json
import requests

# === Obtenir la dernière version de LoL ===
versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
response = requests.get(versions_url)
latest_version = response.json()[0]

# === Télécharger le fichier item.json pour cette version ===
item_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/item.json"
response = requests.get(item_url)
items_data = response.json()

# === Créer un dictionnaire ID → nom d'objet ===
item_id_to_name = {
    int(item_id): item_info['name']
    for item_id, item_info in items_data['data'].items()
}

# === Saisie interactive des 6 IDs d'objets ===
item_ids = []
for i in range(1, 7):
    val = input(f"ID de l'item{i} : ").strip()
    try:
        item_ids.append(int(val))
    except ValueError:
        item_ids.append(0)  # objet inconnu

# === Construction du dictionnaire formaté ===
result = {
    f"item{i+1}": item_id_to_name.get(item_ids[i], "None")
    for i in range(6)
}

# === Affichage du résultat final ===
print("\n🧾 Format JSON :")
print(json.dumps(result, indent=2))
