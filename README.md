# 🧠 League of Legends AI Coach

Bienvenue dans **League of Legends AI Coach**, un projet open-source perso visant à créer un assistant de coaching automatisé basé sur l’intelligence artificielle pour le jeu *League of Legends*.

---

## 🎯 Objectif du projet final

L'objectif est de fournir aux joueurs un **coaching personnalisé** via une interface web ou CLI capable de :

- 📊 Analyser leurs parties jouées  
- 🧩 Détecter leurs erreurs stratégiques  
- 🔍 Identifier les optimisations possibles (builds, runes, macro, etc.)  
- 💡 Proposer des conseils contextualisés basés sur des données réelles de haut niveau  

Le but ultime : Développer une IA stratégique de très haut niveau capable d’analyser des phases de lane en vidéo, comprendre les logiques de jeu comme un coach professionnel (LCK-level), et détecter automatiquement les bons ou mauvais comportements.

---

## ✨ Fonctionnalités actuelles

✅ **Modèle IA fonctionnel pour :**
- 📦 Recommandation de builds complets (6 items) en fonction du champion, de l’équipe et des ennemis  
- 🏹 Prédiction de la rune principale optimale  
- 🧠 Prise en compte des *tags stratégiques* des champions (Assassin, Tank, Healing, Hard CC, etc.)  
- ⚔️ Gestion des matchups midlane pour enrichir les contextes d’entraînement  

🛠 **Base de données locale :**
- Objets, champions, runes, compétences, et tags  
- Matchups champions + builds liés à des parties réelles  
- Équipes alliées et ennemies enrichies avec leurs profils (tags + sorts)  

📤 **Interface interactive en terminal :**
- Entrée du champion joué, rôle, et compositions alliée/ennemie  
- Retour immédiat : rune optimale + build complet ordonné  
- Feedback visuel clair (affichage structuré en terminal)  

👁 **Module de vision (YOLOv8) :**
- Extraction et annotation automatique d’images depuis des clips  
- Détection en temps réel d’éléments clés : champions, sbires, tours, barres de HP/mana, minimap  
- Pipeline d’entraînement et de prédiction opérationnel  
- Tests possibles sur images, vidéos et webcam pour valider la détection  

Il manque encore enorément de DATA mais les models fonctionnent !! 


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
| `PyTorch`            | Entraînement profond (deep learning)  |
| `OpenCV`             | Traitement vidéo                      |
| `JSon`               | Format d'annotation / de fichiers bdd |
| `YOLO`               | Model d'ia à entrainer                |

---

## 🧪 En cours de développement

- ⚔️ Reconnaissance de matchups spécifiques  
- 🎬 Analyse de replays et reconnaissances de paterns de jeu 
- 🗺️ Analyse de la phase de lane
- 🕹️ Coaching complet lane par lane ( actuellement uniquement Midlane )


---

## 🧠 Prochain module : IA de stratégie via Deep Learning

**Objectif**

Créer une IA capable d’apprendre à analyser une phase de lane à partir de clips vidéo annotés.

📋 Étapes prévues (Théorie) :
    1.    Collecte & découpage de clips vidéo centrés sur la phase de lane (≈14min)
    2.    Annotation manuelle : commencer avec 30 clips sur la notion de CSing (good_cs / bad_cs).
    3.    Conception d’un dataset compatible PyTorch : intégration progressive des annotations.
    4.    Modèle initial : entraînement sur une première tâche simple (ex : prédire si une phase est bonne ou mauvaise selon les cs).
    5.    Itération : ajout progressif de nouvelles notions dans les annotations :
    •    trades gagnants / perdants
    •    wave management
    •    vision / jungle tracking
    •    recall timings
    •    roaming / impact map
    6.    Entraînement plus poussé avec clips plus longs, puis matchs complets.
    7.    Émergence de compréhension stratégique par apprentissage supervisé et guidé par des scores/pénalités (reward shaping).
    
🧩 Approche stratégique
    •    L’IA n’a pas besoin de mécaniques, uniquement de comprendre les situations de jeu.
    •    On commence avec plusieurs champions, mais à terme l'idée est de spécialiser l’IA par rôle ou champion (ex : 10 000 games de Yone mid).
    •    À mesure que les concepts s’empilent, l’IA développera une compréhension profonde
    •    Les annotations servent à guider l’apprentissage, mais une fois suffisantes, l’IA saura généraliser.

 ## 🔮 Prochaines étapes

🎯 **Renforcer la précision du module d’itemisation**  
- Enrichir la base de données avec davantage de parties (pro + haut elo)  
- Intégrer des règles contextuelles avancées (anti-heal vs régénération, bottes spécifiques vs CC lourd, etc.)  
- Optimiser le modèle pour prendre en compte plus de rôles que la midlane  

👁 **Améliorer le module de vision (YOLOv8)**  
- Annoter et entraîner sur davantage d’images pour stabiliser la détection  
- Étendre les classes détectées : objectifs neutres (Drake, Baron, camps de jungle), sorts utilisés, vision (wards)  
- Développer une interface temps réel qui superpose les détections sur le replay et suit la timeline  

🧩 **Analyse de phase de lane (Deep Learning + annotations)**  
- Création d’un dataset de clips annotés (ex. : `good_cs`, `bad_trade`, `good_recall`)  
- Entraîner l’IA à reconnaître les fondamentaux : CS/min, gestion de wave, recalls, trades gagnants/perdants  
- Développer un système de scoring par phase de lane (comme un coach qui attribue des notes)  

⚔️ **Vers une IA stratégique complète**  
- Fusionner les modules existants (itemisation, vision, phase de lane) dans un seul pipeline d’analyse  
- Ajouter un module d’**analyse de draft** basé sur la méta et les synergies/contre-synergies entre champions  
- Générer des rapports détaillés **minute par minute** avec conseils pratiques (itemisation, mouvements, vision, objectifs)  

🌐 **Expérience utilisateur finale**  
- Site web ou app permettant d’**uploader un replay Riot** (`.rofl`)  
- Coaching interactif où l’IA commente la partie comme un head coach (à la manière d’un grand maître d’échecs sur chess.com)  
- Mode interactif avec feedback utilisateur (✅ compris / ❌ pas compris → l’IA développe son explication)  

---

## 🚀 Vision long terme

- 🔄 Fusion de modules : build + stratégie + draft.
- 🧠 IA multi-niveaux connectée par LLM ou un gestionnaire central ( ou les deux )
- 💬 Interface de coaching automatisée capable d’expliquer, justifier, conseiller.
- 📈 Potentiel économique : outils de coaching pour particuliers, équipes e-sport, académies.
    
---

## 👤 Auteur

**Ryan Delépine**  

Je suis un developeur de 21 ans,  passionné de League of Legends , et d'informatique , j'aime tester des choses et mettre en commun des passions dans des projets sympa !
  
Projet conçu dans le cadre personnel , dans le seul but d'en apprendre plus sur l'intelligence artificielle ( et sur League Of Legends bien entendu ).

---

## ⭐️ Contribuer

Ce projet est en pleine construction. Si vous souhaitez contribuer, tester ou suggérer des idées, vous êtes les bienvenus ! Clonez, testez, proposez ✨
