import requests
import json
import time
import sqlite3

<<<<<<< HEAD
RIOT_API_KEY = "Ajouter une API ici"
=======
RIOT_API_KEY = ""
>>>>>>> a7eeff7 (Database Extension)
HEADERS = {"X-Riot-Token": RIOT_API_KEY}
REGION_ROUTING = "europe"
PLATFORM_ROUTING = "euw"

# === Connexion à la base de données locale pour les tags ===
conn = sqlite3.connect("../SQL/lol_ai.db")
cursor = conn.cursor()

# === Mapping des runes principales ID → nom lisible ===
rune_mapping = {
    8112: "Electrocute",
    8124: "Predator",
    8128: "Dark Harvest",
    9923: "Hail of Blades",
    8351: "Glacial Augment",
    8360: "Unsealed Spellbook",
    8369: "First Strike",
    8005: "Press the Attack",
    8008: "Lethal Tempo",
    8021: "Fleet Footwork",
    8010: "Conqueror",
    8437: "Grasp of the Undying",
    8439: "Aftershock",
    8465: "Guardian",
    8214: "Summon Aery",
    8229: "Arcane Comet",
    8230: "Phase Rush"
}

# === Récupération des noms d'objets depuis DDragon ===
versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
latest_version = requests.get(versions_url).json()[0]
items_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/item.json"
items_data = requests.get(items_url).json()["data"]
item_names = {int(k): v["name"] for k, v in items_data.items()}

def get_item_name(item_id):
    return item_names.get(item_id, f"Item {item_id}")

# === Fonctions ===
def get_puuid(game_name, tag_line):
    url = f"https://{REGION_ROUTING}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()['puuid']

def get_match_ids(puuid, start, count):
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start={start}&count={count}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_match_detail(match_id):
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_timeline(match_id):
    url = f"https://{REGION_ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_tags(champion_names):
    tags = set()
    for name in champion_names:
        cursor.execute("SELECT tags FROM champions WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            tags.update(result[0].split(", "))
    return sorted(tags)

def build_json_from_match(match, timeline, puuid):
    participants = match['info']['participants']
    player = next(p for p in participants if p['puuid'] == puuid)
    participant_id = player['participantId']

    if player['teamPosition'] != "MIDDLE":
        print("→ Partie ignorée : joueur en", player['teamPosition'])
        return None

    ally_team = [p['championName'] for p in participants if p['teamId'] == player['teamId'] and p['puuid'] != puuid]
    enemy_team = [p['championName'] for p in participants if p['teamId'] != player['teamId']]

    matchup = next(
        (p['championName'] for p in participants if p['teamId'] != player['teamId'] and p['teamPosition'] == "MIDDLE"),
        enemy_team[0]
    )

    perks = player['perks']['styles'][0]['selections']
    main_rune_id = perks[0]['perk']
    rune_name = rune_mapping.get(main_rune_id, str(main_rune_id))

    final_items = [player.get(f'item{i}', 0) for i in range(6) if player.get(f'item{i}', 0) != 0]
    purchase_order = []

    for frame in timeline["info"]["frames"]:
        for event in frame.get("events", []):
            if event.get("type") == "ITEM_PURCHASED" and event.get("participantId") == participant_id:
                item_id = event.get("itemId")
                if item_id in final_items and item_id not in purchase_order:
                    purchase_order.append(item_id)

    while len(purchase_order) < 6:
        purchase_order.append("None")

    named_items = [get_item_name(i) if isinstance(i, int) else "None" for i in purchase_order[:6]]

    return {
        "champion": player['championName'],
        "role": "Mid",
        "rune": rune_name,
        "matchup": matchup,
        "ally_tags": get_tags(ally_team),
        "enemy_tags": get_tags(enemy_team),
        "item1": named_items[0],
        "item2": named_items[1],
        "item3": named_items[2],
        "item4": named_items[3],
        "item5": named_items[4],
        "item6": named_items[5]
    }

# === Point d'entrée principal ===
def main():
    game_name = input("Nom d'invocateur : ")
    tag_line = input("Tag Riot : ")
    max_builds = 10
    builds_collected = 0

    try:
        puuid = get_puuid(game_name, tag_line)
    except Exception as e:
        print("Erreur lors de la récupération du PUUID :", e)
        return

    for page in range(0, 10):
        try:
            match_ids = get_match_ids(puuid, page * 10, 10)
        except Exception as e:
            print("Erreur lors de la récupération des matchs :", e)
            break

        if not match_ids:
            break

        for match_id in match_ids:
            try:
                match = get_match_detail(match_id)
                timeline = get_timeline(match_id)
                build = build_json_from_match(match, timeline, puuid)
                if build:
                    print("\n✅ Build extrait :")
                    print(json.dumps(build, indent=2))
                    builds_collected += 1

                time.sleep(1.2)

                if builds_collected >= max_builds:
                    return

            except Exception as e:
                print(f"Erreur avec {match_id} : {e}")
                continue

if __name__ == "__main__":
    main()
