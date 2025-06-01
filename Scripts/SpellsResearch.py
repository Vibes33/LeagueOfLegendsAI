import sqlite3
import requests
import json

# === Configuration ===
PATCH = "15.10.1"
CHAMP_LIST_URL = f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion.json"
CHAMP_DETAIL_URL = f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion/{{champion_name}}.json"
DB_PATH = "../SQL/lol_ai.db"

# === Connexion à la base ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === Récupération des champions ===
print("🔎 Récupération des sorts de chaque champion...")
res = requests.get(CHAMP_LIST_URL)
if res.status_code != 200:
    print("❌ Erreur lors de la récupération de la liste des champions.")
    exit()
champions = res.json()["data"]

inserts = 0
for champ_key, champ_data in champions.items():
    name = champ_data["id"]
    detail_url = CHAMP_DETAIL_URL.format(champion_name=name)
    r_detail = requests.get(detail_url)
    if r_detail.status_code != 200:
        print(f"❌ Erreur de récupération de {name}")
        continue

    detail = r_detail.json()["data"][name]

    # Récupérer l'id du champion dans la base
    cursor.execute("SELECT id FROM champions WHERE name = ?", (name,))
    champ_row = cursor.fetchone()
    if not champ_row:
        print(f"⚠️ Champion {name} non présent dans la base, ignoré.")
        continue
    champion_id = champ_row[0]

    # Spells actifs : Q, W, E, R
    spell_keys = ["Q", "W", "E", "R"]
    for i, spell in enumerate(detail.get("spells", [])):
        try:
            spell_key = spell_keys[i]
            cursor.execute("""
                INSERT INTO spells (champion_id, spell_key, name, description, cooldowns, costs)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                champion_id,
                spell_key,
                spell.get("name", ""),
                spell.get("description", ""),
                json.dumps(spell.get("cooldown", [])),
                json.dumps(spell.get("cost", []))
            ))
            inserts += 1
        except Exception as e:
            print(f"❌ Erreur sur sort {spell.get('name')} de {name} : {e}")

    # Passive
    passive = detail.get("passive", {})
    if passive:
        try:
            cursor.execute("""
                INSERT INTO spells (champion_id, spell_key, name, description, cooldowns, costs)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                champion_id,
                "Passive",
                passive.get("name", ""),
                passive.get("description", ""),
                json.dumps([]),
                json.dumps([])
            ))
            inserts += 1
        except Exception as e:
            print(f"❌ Erreur sur passive de {name} : {e}")

conn.commit()
conn.close()
print(f"✅ {inserts} sorts insérés dans la base de données.")

