import sqlite3
import json
import os

DB_PATH = "../SQL/lol_ai.db"
OUTPUT_PATH = "../Data/dataset_with_slots.json"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === Listes de détection contextuelle ===
high_healing_champions = {
    "Warwick", "Briar", "Aatrox", "Dr. Mundo", "Vladimir", "Soraka", "Yuumi",
    "Sylas", "Nidalee", "Fiora", "Olaf", "Illaoi", "Maokai", "Zac"
}

hard_cc_champions = {
    "Amumu", "Morgana", "Sejuani", "Lissandra", "Malzahar", "Leona", "Nautilus",
    "Thresh", "Rakan", "Zac", "Maokai", "Skarner", "Alistar", "Braum", "Vi",
    "Neeko", "Janna", "Pantheon", "Galio", "Kennen", "Rell", "Blitzcrank"
}

# Enrichit une équipe avec les tags des champions
def enrich_team(champion_names):
    team = []
    for name in champion_names:
        cursor.execute("SELECT stats, tags FROM champions WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            tags = row[1].split(", ")
            team.append({"name": name, "tags": tags})
        else:
            team.append({"name": name, "tags": []})
    return team

# Récupère les builds depuis la BDD
cursor.execute("SELECT champion, role, rune, matchup, ally_team, enemy_team, final_build FROM builds")
rows = cursor.fetchall()

dataset = []

for row in rows:
    champion, role, rune, matchup, ally_json, enemy_json, build_json = row
    try:
        ally_team = json.loads(ally_json)
        enemy_team = json.loads(enemy_json)
        final_build = json.loads(build_json)
    except Exception as e:
        print(f"❌ Erreur JSON : {e}")
        continue

    enriched_ally = enrich_team(ally_team)
    enriched_enemy = enrich_team(enemy_team)

    ally_tags = list({tag for champ in enriched_ally for tag in champ['tags']})
    enemy_tags = list({tag for champ in enriched_enemy for tag in champ['tags']})

    # Tags contextuels dynamiques
    if any(champ in high_healing_champions for champ in enemy_team):
        enemy_tags.append("Healing")

    if any(champ in hard_cc_champions for champ in enemy_team):
        enemy_tags.append("HardCC")

    # Assure que le build fait bien 6 items (remplit avec "None" sinon)
    final_build += ["None"] * (6 - len(final_build))

    record = {
        "champion": champion,
        "role": role,
        "rune": rune,
        "matchup": matchup,
        "ally_tags": ally_tags,
        "enemy_tags": enemy_tags,
        "item1": final_build[0],
        "item2": final_build[1],
        "item3": final_build[2],
        "item4": final_build[3],
        "item5": final_build[4],
        "item6": final_build[5]
    }
    dataset.append(record)

# Sauvegarde
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w') as f:
    json.dump(dataset, f, indent=2)

print(f"✅ Dataset généré avec {len(dataset)} builds avec slots dans {OUTPUT_PATH}")

conn.close()
