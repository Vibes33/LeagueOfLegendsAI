import sqlite3
import requests
import json

# === Configuration ===
PATCH = "15.10.1"
URL = f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/item.json"
DB_PATH = "../SQL/lol_ai.db"

# === Connexion à la base de données ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === Requête à Riot Data Dragon ===
print(f"🔎 Téléchargement des items du patch {PATCH}...")
response = requests.get(URL)
if response.status_code != 200:
    print("❌ Erreur lors de la récupération des items.")
    exit()

data = response.json()
items_data = data["data"]

# === Insertion dans la base ===
inserted = 0
for item_id, item_info in items_data.items():
    try:
        id_int = int(item_id)
        name = item_info.get("name", "Unknown")
        description = item_info.get("description", "")
        stats = item_info.get("stats", {})

        cursor.execute("""
            INSERT OR REPLACE INTO items (id, name, stats, description)
            VALUES (?, ?, ?, ?)
        """, (id_int, name, json.dumps(stats), description))

        inserted += 1
    except Exception as e:
        print(f"❌ Erreur sur l'item {item_id} : {e}")

conn.commit()
conn.close()
print(f"✅ {inserted} objets insérés dans la base de données.")
