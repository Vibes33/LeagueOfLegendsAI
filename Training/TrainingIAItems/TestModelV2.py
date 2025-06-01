import os
import sys
import json
import joblib

# === Ajout du chemin racine du projet ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
sys.path.append(ROOT_DIR)

# === Chargement du modèle ===
model_path = os.path.join(ROOT_DIR, "Models/itemization/item_model_v2.pkl")
model = joblib.load(model_path)
print("📥 Modèle chargé.")

# === Charger les tags des champions depuis le fichier ===
with open(os.path.join(ROOT_DIR, "Data/champion_tags.json"), "r") as f:
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
champion = input("Votre champion : ").strip()
role = input("Votre poste (ex: Mid) : ").strip()  # Pas utilisé mais conservé
print("🔹 Entrez les 5 champions alliés (séparés par des virgules) :")
allies = input("Alliés : ").split(",")

print("🔹 Entrez les 5 champions ennemis (séparés par des virgules) :")
enemies = input("Ennemis : ").split(",")

# === Récupération des tags ===
ally_tags = collect_tags(allies)
enemy_tags = collect_tags(enemies)

# === Vectorisation (identique à TrainModel.py) ===
all_champions = model["champions"]
all_tags = model["tags"]

def vectorize_input(entry):
    vector = []
    for champ in all_champions:
        vector.append(1 if champ == entry["champion"] else 0)
    for tag in all_tags:
        vector.append(1 if tag in entry["ally_tags"] else 0)
    for tag in all_tags:
        vector.append(1 if tag in entry["enemy_tags"] else 0)
    return vector

entry = {
    "champion": champion,
    "ally_tags": ally_tags,
    "enemy_tags": enemy_tags
}

X = [vectorize_input(entry)]

# === Prédiction ===
rune = model["rune_model"].predict(X)[0]
items = model["item_model"].predict(X)[0]

# === Filtrage des doublons ===
seen = set()
filtered_items = []
for item in items:
    if item not in seen and item != "None":
        seen.add(item)
        filtered_items.append(item)
while len(filtered_items) < 6:
    filtered_items.append("None")

# === Affichage ===
print("\n🔮 Recommandation IA pour ce contexte :")
print(f"🏹 Rune optimale : {rune}\n")
print("🛒 Build recommandé dans l'ordre d'achat :")
for i, item in enumerate(filtered_items, 1):
    print(f"  {i}. {item}")
