# 🧠 League of Legends AI Coach

Bienvenue dans **League of Legends AI Coach**, un projet open-source ambitieux visant à créer un assistant de coaching automatisé basé sur l’intelligence artificielle pour le jeu *League of Legends*.

---

## 🎯 Objectif du projet

L'objectif est de fournir aux joueurs un **coaching personnalisé** via une interface web ou CLI capable de :

- 📊 Analyser leurs parties jouées  
- 🧩 Détecter leurs erreurs stratégiques  
- 🔍 Identifier les optimisations possibles (builds, runes, macro, etc.)  
- 💡 Proposer des conseils contextualisés basés sur des données réelles de haut niveau  

Le but ultime : apprendre aux joueurs **le pourquoi** de leurs erreurs, pas seulement **le quoi**.

---

## 🚀 Fonctionnalités actuelles

✅ Modèle IA fonctionnel pour :
- 📦 Recommandation de builds (6 items) en fonction du champion, de l'équipe et des ennemis
- 🏹 Prédiction de la rune principale optimale
- 🧠 Prise en compte des tags stratégiques des champions (Assassin, Tank, Healing, etc.)

🛠 Base de données locale :
- Objets, champions, runes, compétences, et tags
- Matchups champions + builds liés à des contextes réels

📤 Possibilité de tester des contextes interactifs directement en terminal :
- Entrée du champion joué
- Composition alliée et ennemie
- Retour immédiat : rune + build complet

---

## 🔧 Technologies utilisées

| Composant             | Description                           |
|----------------------|---------------------------------------|
| `Python 3`           | Langage principal                     |
| `Scikit-learn`       | Entraînement du modèle IA             |
| `SQLite`             | Base de données locale                |
| `Joblib`             | Sauvegarde & chargement du modèle     |
| `Riot Games API`     | Récupération des données live         |
| `Data Dragon`        | Mapping des objets et champions       |
| `GitHub`             | Versioning et hébergement du projet   |

---

## 🧪 En cours de développement

- ⚔️ Reconnaissance de matchups spécifiques  
- 🎬 Lecture et découpage automatique de replays  
- 🗺️ Analyse de la vision et du positionnement  
- 🕹️ Coaching complet lane par lane  
- 🌐 Interface web (long terme)

---

## 🛠 Arborescence actuelle du projet

📁 Data/
├─ dataset_with_slots.json
├─ champion_tags.json
└─ itemsmap.py

📁 Models/
└─ itemization/
├─ ItemRecommenderV2.py
└─ item_model_v2.pkl

📁 Scripts/
├─ ItemResearch.py
├─ RunesResearch.py
├─ ChampionsRequest.py
└─ build_dataset.py

📁 Training/
└─ TrainingIAItems/
├─ TrainModel.py
├─ TestModel.py
└─ TestModelV2.py

---

## 👤 Auteur

**Ryan Delépine**  
Développeur passionné de League of Legends , et d'informatique , j'aime tester des choses et mettre en commun des passions dans des projets sympa !  
Projet conçu dans le cadre personnel , dans le seul but d'en apprendre plus sur l'intelligence artificielle.

---

## 🧠 Vision long terme

Créer un assistant aussi interactif et pédagogique que **l’IA de chess.com**, mais pour *League of Legends*, avec des explications précises, visuelles, et vocales si nécessaire.

---

## ⭐️ Contribuer

Ce projet est en pleine construction. Si vous souhaitez contribuer, tester ou suggérer des idées, vous êtes les bienvenus ! Clonez, testez, proposez ✨
