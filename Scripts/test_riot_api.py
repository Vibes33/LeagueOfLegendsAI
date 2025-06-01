import requests

# ✅ Ta clé API Riot Games (valide 24h)
RIOT_API_KEY = "RGAPI-b9e8abdf-d3ca-4bc2-9ad5-062b74a30f42"

# Configuration de l'en-tête d'authentification
HEADERS = {"X-Riot-Token": RIOT_API_KEY}

# Exemple de joueur sur le serveur EUW
summoner_name = "Caps"
region = "euw1"  # Pour les infos du joueur

# URL pour obtenir les infos du joueur
url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"

# ➤ Envoi de la requête
response = requests.get(url, headers=HEADERS)

# ➤ Traitement de la réponse
if response.status_code == 200:
    data = response.json()
    print("✅ Clé API valide ! Voici les infos du joueur :")
    print(f"Nom     : {data['name']}")
    print(f"PUUID   : {data['puuid']}")
    print(f"Niveau  : {data['summonerLevel']}")

elif response.status_code == 401:
    print("❌ Erreur 401 : Clé API invalide ou expirée.")
    print("→ Va sur https://developer.riotgames.com pour en générer une nouvelle.")

elif response.status_code == 403:
    print("❌ Erreur 403 : Accès interdit.")
    print("→ Vérifie que ta clé est active et que tu utilises le bon endpoint et la bonne région.")
    print("→ Si tu appelles match/v5, n'oublie pas de passer par 'europe', 'asia' ou 'americas' selon le serveur.")

elif response.status_code == 429:
    print("⚠️ Erreur 429 : Trop de requêtes.")
    print("→ Attends quelques secondes/minutes avant de réessayer.")

else:
    print(f"❌ Erreur {response.status_code} inconnue.")
    print(response.text)
