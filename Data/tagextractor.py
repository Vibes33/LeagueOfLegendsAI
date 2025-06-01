import json

# === Charger les tags des champions depuis le fichier ===
with open("../Data/champion_tags.json", "r") as f:
    champion_tags = json.load(f)

# === Fonction pour collecter les tags depuis une équipe ===
def collect_tags(champion_list):
    tags = set()
    for champ in champion_list:
        champ = champ.strip()
        if champ in champion_tags:
            tags.update(champion_tags[champ])
        else:
            print(f"⚠️ Champion inconnu ou mal orthographié : {champ}")
    return sorted(tags)

# === Saisie manuelle ===
print("🔹 Entrez les 5 champions alliés (séparés par des virgules) :")
allies = input("Alliés : ").split(",")

print("🔹 Entrez les 5 champions ennemis (séparés par des virgules) :")
enemies = input("Ennemis : ").split(",")

# === Récupération des tags ===
ally_tags = collect_tags(allies)
enemy_tags = collect_tags(enemies)

# === Affichage formaté ===
print("\n✅ Résultat :")
print(json.dumps({
    "ally_tags": ally_tags,
    "enemy_tags": enemy_tags
}, indent=2))
