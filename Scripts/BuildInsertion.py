import sqlite3
import json
from datetime import datetime

# === Configuration ===
DB_PATH = "../SQL/lol_ai.db"

# === Exemple de build complet ===
build = {
    "champion": "Viktor",
    "role": "Mid",
    "rune": "Summon Aery",
    "matchup": "Lucian",
    "ally_team": ["Gwen", "XinZhao", "Neeko", "Senna"],
    "enemy_team": ["Lucian", "Jayce", "Nidalee", "Ezreal", "Leona"],
    "final_build": [
        "Rod of Ages",
        "Ionian Boots of Lucidity",
        "Lich Bane",
        "Rabadon's Deathcap",
        "Zhonya's Hourglass",
        "Void Staff"
    ]
}

# === Insertion dans la base ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO builds (
        champion, role, rune, matchup, ally_team, enemy_team, final_build, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    build["champion"],
    build["role"],
    build["rune"],
    build["matchup"],
    json.dumps(build["ally_team"]),
    json.dumps(build["enemy_team"]),
    json.dumps(build["final_build"]),
    datetime.now().isoformat()
))

conn.commit()
conn.close()

print("✅ Build inséré avec succès dans la base de données.")
