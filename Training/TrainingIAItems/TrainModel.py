import json
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

# === Détection du dossier racine ===
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# === Chargement du dataset avec slots ===
data_path = os.path.join(ROOT_DIR, "Data/dataset_with_slots.json")
with open(data_path, "r") as f:
    raw_dataset = json.load(f)

# === Filtres et vérifications ===
required_fields = ["champion", "rune"] + [f"item{i+1}" for i in range(6)]
dataset = []
for entry in raw_dataset:
    if all(field in entry for field in required_fields):
        dataset.append(entry)
    else:
        print("⚠️ Entrée ignorée (incomplète) :", entry)

# === Préparation ===
all_tags = ["Assassin", "Fighter", "Mage", "Marksman", "Support", "Tank", "Healing", "HardCC"]
all_champions = sorted({entry["champion"] for entry in dataset})

# === Vectorisation ===
def vectorize_input(entry):
    vector = []
    for champ in all_champions:
        vector.append(1 if champ == entry["champion"] else 0)
    for tag in all_tags:
        vector.append(1 if tag in entry["ally_tags"] else 0)
    for tag in all_tags:
        vector.append(1 if tag in entry["enemy_tags"] else 0)
    return vector

X = [vectorize_input(entry) for entry in dataset]
y_runes = [entry["rune"] for entry in dataset]
y_items = [[entry[f"item{i+1}"] for i in range(6)] for entry in dataset]

# === Entraînement ===
rune_clf = RandomForestClassifier(n_estimators=100, random_state=42)
items_clf = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))

model = {
    "rune_model": rune_clf.fit(X, y_runes),
    "item_model": items_clf.fit(X, y_items),
    "champions": all_champions,
    "tags": all_tags
}

# === Sauvegarde ===
model_path = os.path.join(ROOT_DIR, "Models/itemization/item_model_v2.pkl")
joblib.dump(model, model_path)

print("✅ Modèle entraîné avec précision moyenne (rune) : {:.2f}".format(model["rune_model"].score(X, y_runes)))
print("📦 Modèle sauvegardé dans:", model_path)
