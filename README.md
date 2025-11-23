# ⚔️ League of Legends Expert Build System

Système expert pour générer des builds optimaux basés sur des données réelles de parties Challenger/Grandmaster via l'API officielle Riot Games.

## 🚀 Quick Start

```bash
# 1. Lancer le programme
python lol_manager.py

# 2. (Optionnel) Avec clé API Riot pour des builds réels
# Voir: docs/riot_api_key.txt.example
echo "RGAPI-your-key-here" > riot_api_key.txt
```

## 📚 Documentation

- **[Guide complet](docs/GUIDE.txt)** - Guide visuel avec exemples
- **[README détaillé](docs/README.md)** - Documentation complète
- **[Changelog](docs/CHANGELOG.md)** - Historique des modifications
- **[Configuration API](docs/riot_api_key.txt.example)** - Instructions pour la clé API

## ✨ Fonctionnalités

- 📋 Liste des 172 champions avec détails des sorts
- 🎒 Base de données de 169 items
- 🛡️ Générateur de builds avec données réelles Challenger
- 🤖 Analyse de gameplay

## 🔑 API Riot (Optionnel)

Pour des builds basés sur de vraies parties Challenger :
1. Obtiens une clé sur https://developer.riotgames.com/
2. Crée le fichier `riot_api_key.txt`
3. Teste avec `python test_api_key.py`

Sans clé API, le système utilise un système expert fonctionnel.

## 📖 Aide

```bash
# Tester la clé API
python test_api_key.py

# Menu interactif
./quick_menu.sh
```

---

**Version 2.0** | Made with ⚡ by Ryan
