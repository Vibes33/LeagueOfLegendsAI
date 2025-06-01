import sqlite3
import requests
import json

# === Configuration ===
PATCH = "15.10.1"  # Doit correspondre à une version valide de Data Dragon
CHAMP_LIST_URL = f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion.json"
CHAMP_DETAIL_URL = f"https://ddragon.leagueoflegends.com/cdn/{PATCH}/data/en_US/champion/{{champion_name}}.json"
DB_PATH = "../SQL/lol_ai.db"

# === Connexion à la base ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === Récupérer la liste des champions ===
print(f"🔎 Récupération des champions pour le patch {PATCH}...")
res = requests.get(CHAMP_LIST_URL)
if res.status_code != 200:
    print("❌ Erreur lors de la récupération de la liste des champions.")
    exit()
champions = res.json()["data"]

# === Traitement et insertion ===
inserts = 0
for champ_key, champ_data in champions.items():
    name = champ_data["id"]
    print(f"→ Traitement de {name}...")

    # Détails du champion
    detail_url = CHAMP_DETAIL_URL.format(champion_name=name)
    r_detail = requests.get(detail_url)
    if r_detail.status_code != 200:
        print(f"❌ Erreur de récupération de {name}")
        continue

    detail = r_detail.json()["data"][name]
    stats = detail.get("stats", {})
    tags = ", ".join(detail.get("tags", []))
    resource_type = detail.get("partype", "Unknown")

    # Insertion
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO champions (name, stats, tags, resource_type)
            VALUES (?, ?, ?, ?)
        """, (name, json.dumps(stats), tags, resource_type))
        inserts += 1
    except Exception as e:
        print(f"❌ Erreur insertion {name} : {e}")

conn.commit()
conn.close()
print(f"✅ {inserts} champions insérés avec leurs stats.")
