import sqlite3
import requests
import json

# === Configuration ===
URL = "https://ddragon.leagueoflegends.com/cdn/15.10.1/data/en_US/runesReforged.json"
DB_PATH = "../SQL/lol_ai.db"

# === Connexion à la base ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === Récupération des runes ===
print("🔎 Téléchargement des runes...")
response = requests.get(URL)
if response.status_code != 200:
    print("❌ Erreur de récupération des runes.")
    exit()

runes = response.json()
inserts = 0

for tree in runes:
    path = tree.get("name", "Unknown")
    for slot in tree.get("slots", []):
        for rune in slot.get("runes", []):
            try:
                rune_id = rune["id"]
                name = rune["name"]
                short_desc = rune.get("shortDesc", "")

                cursor.execute("""
                    INSERT OR REPLACE INTO runes (id, name, path, stats)
                    VALUES (?, ?, ?, ?)
                """, (rune_id, name, path, json.dumps({"desc": short_desc})))
                inserts += 1
            except Exception as e:
                print(f"❌ Erreur sur la rune {rune.get('name', '?')} : {e}")

conn.commit()
conn.close()
print("✅ {inserts} runes insérées dans la base de données.")
