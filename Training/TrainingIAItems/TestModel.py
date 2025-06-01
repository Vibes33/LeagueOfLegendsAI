import os
import sys

# === Ajoute le chemin racine du projet à sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
sys.path.append(ROOT_DIR)

# === Import du modèle ===
from Models.itemization.ItemRecommenderV2 import ItemRecommenderV2

# === Chargement du modèle entraîné ===
model = ItemRecommenderV2()
model.load_model(os.path.join(ROOT_DIR, "Models/itemization/item_model_v2.pkl"))

# === Exemple de test enrichi ===
test_example = {
    "champion": "Ahri",
    "role": "Mid",
    "ally_tags": ["Fighter", "Mage", "Support", "Tank"],
    "enemy_tags": ["Assasin", "Mage","Support","Healing"]
}

# === Prédiction ===
prediction = model.predict(test_example)
rune = prediction[0]
items = prediction[1:]

# === Affichage ===
print("\n🔮 Recommandation IA pour ce contexte :")
print(f"🏹 Rune optimale : {rune}\n")
print("🛒 Build recommandé dans l'ordre d'achat :")
for i, item in enumerate(items, 1):
    print(f"  {i}. {item}")
