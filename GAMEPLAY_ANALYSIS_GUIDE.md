# 📊 Guide d'Analyse IA Gameplay

## 🎯 Nouvelles Métriques Ajoutées

### 1. **Participation aux Objectifs** 
Mesure votre implication dans les prises d'objectifs majeurs :
- Dragons auxquels vous avez participé
- Barons auxquels vous avez participé
- Tours détruites où vous avez contribué

**Calcul** : (Objectifs participés / Total objectifs équipe) × 100

**Benchmark** :
- ✅ 70%+ : Excellente participation
- ⚠️ 50-70% : Bonne participation
- 🚨 <30% : Trop peu impliqué

### 2. **KDA Moyen de l'Équipe**
Compare votre performance à celle de vos alliés pour détecter :
- 🌟 Si vous **portez** votre équipe (KDA > 130% de l'équipe)
- 📉 Si vous **sous-performez** (KDA < 70% de l'équipe)
- ⚖️ Si vous jouez au **niveau de l'équipe**

**Impact** :
- KDA supérieur → Vous êtes un carry potentiel
- KDA inférieur → Besoin d'adapter votre style de jeu

### 3. **Champion Nemesis**
Identifie le champion ennemi qui vous cause le plus de problèmes :
- Champion qui vous a tué le plus souvent
- Permet des recommandations ciblées (build, stratégie, demander de l'aide)

**Recommandations générées** :
- 📚 Étudier le matchup
- 🛡️ Build défensif adapté
- 🤝 Demander l'aide du jungler

### 4. **Détails Tours Détruites**
Compte précis des tours où vous avez participé :
- Pression en side lane
- Participation aux sieges
- Objectifs structurels

**Benchmark par rôle** :
- Top/ADC : 3+ tours attendues
- Mid/Jungle : 2+ tours
- Support : 1+ tour

---

## 🎮 Comment Utiliser l'Analyse Manuelle

### Étape 1 : Lancer le Programme
```bash
python lol_manager.py
```

### Étape 2 : Sélectionner "Analyse IA Gameplay"
Menu principal → **[6] 🤖 Analyse IA Gameplay**

### Étape 3 : Choisir "Analyse Manuelle"
**[1] 📊 Analyser une Partie (Données Manuelles)**

### Étape 4 : Entrer vos Statistiques

#### Informations de Base
```
Champion: Yasuo
Rôle: Mid
Durée: 32
Kills: 8
Deaths: 5
Assists: 12
CS: 224
Vision score: 28
Control wards: 5
Dégâts infligés: 38400
```

#### 🆕 Nouvelles Informations Objectifs
```
Dragons auxquels vous avez participé: 2
Total de dragons pris par votre équipe: 3
Barons auxquels vous avez participé: 1
Tours détruites où vous avez participé: 4
```

#### 🆕 Contexte d'Équipe
```
KDA moyen de vos alliés: 2.8
Champion ennemi qui vous a le plus tué: Syndra
```

---

## 📁 Format JSON

Pour l'analyse depuis fichier JSON, utilisez ce format :

```json
{
  "champion": "Yasuo",
  "role": "Mid",
  "duration": 32,
  "kills": 8,
  "deaths": 5,
  "assists": 12,
  "cs": 224,
  "damage": 38400,
  "vision": 28,
  "control_wards": 5,
  "turrets": 4,
  "dragons": 2,
  "barons": 1,
  "objective_participation": 75.0,
  "team_average_kda": 2.8,
  "nemesis_champion": "Syndra"
}
```

**Fichier exemple** : `example_game.json`

---

## 📊 Résultats de l'Analyse

L'analyse affiche maintenant :

### Section Contexte (🆕)
```
Contexte:
  Participation objectifs: 75%
  Tours détruites: 4
  KDA moyen alliés: 2.80
  Comparaison KDA: Meilleur que l'équipe (2.80)
  Champion problématique: Syndra
```

### Recommandations Améliorées
Exemples de nouvelles recommandations générées :

🎯 **Basées sur la participation** :
- "PRIORITÉ: Rotate vers les objectifs avec ton équipe"
- "Sois plus présent lors des prises de dragons et barons"
- "Ward autour des objectifs et spam-ping pour que ton équipe rotate"

🎯 **Basées sur le contexte équipe** :
- "Tu portes ton équipe! KDA: 4.00 vs équipe: 2.80"
- "Ton équipe joue mieux que toi - adapte ton style de jeu"

🎯 **Basées sur le champion nemesis** :
- "Étudie le matchup contre Syndra"
- "Build défensif contre Syndra (Zhonya's, Banshee's, etc.)"
- "Demande de l'aide à ton jungler pour gérer Syndra"

---

## 💡 Conseils d'Utilisation

### Pour les Objectifs
1. **Dragons** : Note tous les dragons où tu étais présent (même sans assist)
2. **Barons** : Compte uniquement ceux où tu as participé activement
3. **Tours** : Inclut les tours où tu as fait des dégâts significatifs

### Pour le KDA Équipe
- Moyenne des KDA de tes 4 alliés
- Calcul : (KDA ally1 + KDA ally2 + KDA ally3 + KDA ally4) / 4
- Ou utilise la moyenne affichée dans le post-game

### Pour le Champion Nemesis
- Champion ennemi qui t'a tué le plus (check death recap)
- Si égalité, choisis celui qui t'a le plus impacté
- Si aucun champion ne t'a tué souvent, mets "Aucun"

---

## 🔮 Utilisation Avancée

### Analyser l'Évolution
Compare plusieurs parties pour voir ta progression :

```bash
# Partie 1
python lol_manager.py → [6] → [1] → Entrer stats

# Partie 2
python lol_manager.py → [6] → [1] → Entrer stats

# Compare manuellement les scores
```

### Identifier les Patterns
- Si même champion nemesis sur plusieurs games → **Urgence de travailler ce matchup**
- Si participation objectifs constamment basse → **Focus macro game**
- Si KDA vs équipe toujours négatif → **Revoir fundamentals**

---

## 🎓 Exemple Complet

**Scénario** : Partie Mid lane en ranked

```
Champion: Ahri
Rôle: Mid
Durée: 28 minutes
KDA: 6/4/10 (KDA: 4.00)
CS: 196 (7.0 CS/min)
Vision: 32
Control wards: 4

Objectifs:
- Dragons participés: 2 / Total équipe: 3
- Barons participés: 0
- Tours détruites: 3

Contexte:
- KDA moyen alliés: 2.5
- Champion nemesis: Zed
```

**Résultats Attendus** :
- ✅ Bon CS (7.0/min pour Mid)
- ✅ KDA supérieur à l'équipe (carry potentiel)
- ⚠️ Participation objectifs moyenne (67%)
- 🚨 Problème avec Zed → Build Zhonya's prioritaire
- **Recommandations** : Focus objectifs, counter-build Zed, maintenir CS

---

## 📈 Améliorations Continues

Ces nouvelles métriques permettent une analyse plus **contextualisée** et **personnalisée** :

1. **Contextuelle** : Prend en compte la performance de l'équipe
2. **Ciblée** : Identifie les champions problématiques
3. **Actionnable** : Recommandations concrètes et spécifiques
4. **Complète** : Vision macro (objectifs) + micro (matchups)

---

**Bon climb ! 🚀**
