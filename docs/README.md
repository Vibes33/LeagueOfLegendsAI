# League of Legends Expert Build System

## 🎮 Description

Système expert pour générer des builds optimaux basés sur des données réelles de parties Challenger/Grandmaster via l'API officielle Riot Games.

## ✨ Fonctionnalités

- 📋 **Liste complète des champions** avec détails des sorts (cooldowns, coûts mana, dégâts)
- 🔍 **Recherche de champions** par nom
- 🎒 **Base de données d'items** avec recherche et filtres
- 🛡️ **Générateur de builds** utilisant l'API Riot officielle
- 🤖 **Analyse de gameplay** avec recommandations personnalisées

## 🚀 Installation

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Installer les dépendances (déjà fait)
pip install -r requirements.txt
```

## 🔑 Configuration de l'API Riot (pour builds réels)

### Étape 1 : Obtenir une clé API gratuite

1. Va sur https://developer.riotgames.com/
2. Connecte-toi avec ton compte Riot Games
3. Clique sur **"REGISTER PRODUCT"** ou **"Generate API Key"**
4. Copie ta **Development API Key** (commence par `RGAPI-`)

### Étape 2 : Créer le fichier de configuration

Dans le dossier du projet, crée un fichier `riot_api_key.txt` :

```bash
echo "RGAPI-votre-clé-ici" > riot_api_key.txt
```

**⚠️ IMPORTANT :**
- La clé de développement expire après **24 heures**
- Tu peux en générer une nouvelle gratuitement chaque jour
- **Limites gratuites :** 20 requêtes/seconde, 100 requêtes/2 minutes
- Ne partage **jamais** ta clé API publiquement

### Étape 3 : Utiliser le système

```bash
python lol_manager.py
```

Quand tu choisis **[4] 🛡️ Generate Build**, le système :
1. Détecte automatiquement si tu as une clé API
2. Te demande si tu veux analyser de vraies parties Challenger
3. Analyse 50+ games récentes pour générer le build optimal
4. Affiche le build avec le winrate réel

## 📊 Comment ça marche ?

### Sans clé API (fallback)
Utilise un système expert basé sur les statistiques des champions :
- Détection automatique AP/AD
- Items optimaux selon les tags du champion
- Runes adaptées au style de jeu

### Avec clé API (recommandé)
Analyse de **vraies parties Challenger/Grandmaster** :
1. Récupère la liste des 50 meilleurs joueurs Challenger
2. Analyse leurs 10 dernières parties chacun
3. Filtre par champion et rôle
4. Calcule les items/runes/summoners les plus joués
5. Affiche le **winrate réel** sur les parties analysées

**Données collectées :**
- ✨ Items les plus construits (top 6 par fréquence)
- 🎯 Items de départ les plus populaires
- 🔮 Pages de runes optimales
- ⚡ Sorts d'invocateur meta
- 📈 Winrate réel du build

## 📁 Structure du projet

```
.
├── lol_manager.py           # Interface principale (menu)
├── build_generator.py       # Générateur de builds
├── riot_api_client.py       # Client API Riot (analyse matches)
├── data_dragon_client.py    # Client Data Dragon (champions/items)
├── gameplay_analyzer.py     # Analyse de performance
├── riot_api_key.txt        # ⚠️ Ta clé API (à créer)
└── requirements.txt         # Dépendances Python
```

## 🎯 Exemples d'utilisation

### Générer un build Yasuo Mid avec API

```
[4] 🛡️  Generate Build
Champion name: Yasuo
Role: [3] Mid
Use Riot API? [Y/n]: Y

⚡ Analyzing 50+ Challenger/Grandmaster games...
✓ Analyzed 67 games | 58.2% winrate

🛡️  BUILD - YASUO
Type: AD | Role: Mid
Source: riot_api (58.2% WR, 67 games)

✨ SUMMONER SPELLS: Flash + Ignite
🔮 RUNES: Conqueror (Precision)
🎯 STARTING: Doran's Blade, Health Potion
⚔️  CORE: 
  [1] Berserker's Greaves
  [2] Immortal Shieldbow
  [3] Infinity Edge
  [4] Phantom Dancer
  [5] Bloodthirster
  [6] Mortal Reminder
```

## 🔧 Dépannage

### "API key not found"
- Vérifie que `riot_api_key.txt` existe dans le dossier
- Vérifie que la clé commence par `RGAPI-`

### "Rate limit exceeded"
- Normal : attends 2 minutes et réessaie
- Le système a un délai de 0.05s entre chaque requête
- Cache activé pour éviter les requêtes répétées

### "403 Forbidden"
- Ta clé a peut-être expiré (24h)
- Génère une nouvelle clé sur developer.riotgames.com

### Clé expirée chaque jour
- C'est normal pour les clés Development
- Pour une clé permanente, demande un **Personal API Key** (nécessite projet approuvé)

## 📈 Statistiques

- **172 champions** disponibles
- **169 items** (Summoner's Rift uniquement)
- **Patch actuel :** 15.23.1
- **Mise à jour :** Automatique via Data Dragon

## 💡 Conseils

1. **Première utilisation :** Teste sans API key pour voir le système expert
2. **Avec API :** Prévois 1-2 minutes par build (rate limits)
3. **Cache :** Les résultats sont mis en cache 1 heure
4. **Multi-régions :** Change `region='euw1'` dans `riot_api_client.py` pour NA/KR

## 🌍 Régions supportées

- **EUW1** - Europe West (par défaut)
- **NA1** - North America
- **KR** - Korea
- **EUN1** - Europe Nordic & East
- **BR1** - Brazil
- **LA1/LA2** - Latin America
- **OC1** - Oceania
- **TR1** - Turkey
- **RU** - Russia
- **JP1** - Japan

## 🤝 Contribution

Données fournies par :
- **Riot Data Dragon API** - Champions, items, runes
- **Riot Games Official API** - Match data, rankings

## 📝 License

Projet éducatif - Données © Riot Games

---

**Made by Ryan**
