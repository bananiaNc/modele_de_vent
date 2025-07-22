import requests, json, csv, unicodedata, os
from io import StringIO

# token pour accéder aux services d'api : https://portail-api.meteofrance.fr/web/fr
token = "eyJ4NXQiOiJOelU0WTJJME9XRXhZVGt6WkdJM1kySTFaakZqWVRJeE4yUTNNalEyTkRRM09HRmtZalkzTURkbE9UZ3paakUxTURRNFltSTVPR1kyTURjMVkyWTBNdyIsImtpZCI6Ik56VTRZMkkwT1dFeFlUa3paR0kzWTJJMVpqRmpZVEl4TjJRM01qUTJORFEzT0dGa1lqWTNNRGRsT1RnelpqRTFNRFE0WW1JNU9HWTJNRGMxWTJZME13X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJkYWQzMzdhMC1lNjcyLTQ2ODQtOTRjMi05OTVhZGFiYzk0MjkiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IjFFaEt0RkZmb3loU2tJUWtPYU9hT2d3NG1hc2EiLCJuYmYiOjE3NTI2MzUxMzksImF6cCI6IjFFaEt0RkZmb3loU2tJUWtPYU9hT2d3NG1hc2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvcG9ydGFpbC1hcGkubWV0ZW9mcmFuY2UuZnJcL29hdXRoMlwvdG9rZW4iLCJleHAiOjE3NTI2Mzg3MzksImlhdCI6MTc1MjYzNTEzOSwianRpIjoiNThmNDJkYTMtODFjOC00OTFlLTllNTYtMTE4ZmIxMDRlZWIyIiwiY2xpZW50X2lkIjoiMUVoS3RGRmZveWhTa0lRa09hT2FPZ3c0bWFzYSJ9.OcDJje6IP7G4ldC1y6HoSFXUuW73WVzHhRwVIih-lf2f60k1n8sOVx7z-wzl-RrXBcdZQyBVn9QqaeuQijETapMPYqwr93RKVyCIpomn5xaxiTGTCqnUWdfbk8TKWwNsFwbCZBQT8eDfQkZGWfllwUxmTUUMQTJp-poijP4SkKaqdup3GuX7wFrI4A8UxJqCuaM-7e_YIkjm7GqiF-hmYHn58fQwHSjPXm0sVjXd5QGrvJluZ9Tz7wJUENQeqN50zmBbMBpTIkKRbdugzO9ln9_0lybsWgXBIvpXKrkvQFgbvH-ViIvdZSHV2im3hbaLT4wEadqlqMKKGKH0FMmU9A"

# header qui sera injecter dans la requête http
headers = {
    "accept" : "*/*",
    "Authorization" : f"Bearer {token}"
    }

# lien du serveur utilisé par l'api
url_server = "https://public-api.meteofrance.fr/public/DPClim/v1/"

# liste des fréquences à laquelle les stations enregistre les informations
liste_frequence = ["infrahoraire-6m", "horaire", "quotidienne"]

# liste des fréquences à laquelle les stations enregistre les informations (pour les commandes)
liste_frequence_com = liste_frequence + ["decadaire", "mensuelle"]

# liste des paramètres disponibles
list_parametre = ["Précipitations", "Température", "Humidité", "Vent", "Pression", "Rayonnement", "Insolation", "Etat de la mer", "ETP quotidienne"]

# numéro du département (Nouvelle-Calédonie)
num_dep = "988"


def enlever_accents(texte: str) -> str:
    """_Permt d'enlever les accents d'une chaîne de caractère_

    Args:
        texte (str): _chaine de caractère à traiter_

    Returns:
        str: _la chaîne sans aucun accent_
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte)
        if unicodedata.category(c) != 'Mn'
    )

def obtenir_liste_station(choix_frequence: int, numero_dep: str, parametre: str) -> dict:
    """_Permet d'obtenir la liste de toutes les stations ayant enregistré les données d'un paramètre sur une période donnée_

    Args:
        choix_frequence (int): _Indice de la fréquence choisi dans la liste des fréquences_
        numero_dep (str): _Numéro du département auquel appartient la station_
        parametre (str): _Paramètre sur lequel la recherche se fait_

    Returns:
        dict: _La liste des stations, de leur paramètres, et attributs au format json_
    """
    
    # len(liste_frequence) = 3. Vérifie que 0 < choix_fréquence < 3 pour éviter débordement de liste
    if not 0 < choix_frequence < 3:
        # Si choix_frequence not in < [0, 3[. Retourne un json avec message d'erreur
        return json.dumps({"response": "error"})
    # Prend la valeur de la chaine contenue à l'indice "choix_frequence" de liste_frequence
    frequence = liste_frequence[choix_frequence]
    # Concaténation de l'url du serveur et du reste de l'url pour avoir la route et récupérer les données
    url = url_server + f"liste-stations/{frequence}"
    # Envoie une requête à l'api avec l'url, les paramètres, et les headers
    response = requests.get(
        url, 
        params={
            "id-departement": numero_dep, 
            "parametre":parametre.lower()
            }, 
        headers=headers)
    # Retourne la réponse au format json
    return response.json()

def obtenir_commande_station(choix_frequence: int, id_station: str, date_deb: str, date_fin: str) -> dict:
    """_Permet d'obtenir un numéro de commande, délivré par l'api, pour une station spécifique, à une certaine fréquence, sur une période donnée.
    Si la période donnée est en dehors de la période d'enregistrement de la station alors l'attribut text de response contiendra un message d'erreur_

    Args:
        choix_frequence (int): _Indice de la fréquence choisi dans la liste des fréquences des commandes (liste_frequence_com_
        id_station (str): _Identifiant de la station (id unique)_
        date_deb (str): _Date de départ de la période_
        date_fin (str): _Date de fin de la période_

    Returns:
        dict: _Un json contenant le numéro de commande spécifique, si la commande est bien passé_
    """
    # len(liste_frequence) = 5. Vérifie que 0 < choix_fréquence < 4 pour éviter débordement de liste
    if not 0 < choix_frequence < 5:
        # Retourne un json avec message d'erreur si débordement de la liste
        return json.dumps({"response": "error"})
    # Prend la valeur de la chaine contenue à l'indice "choix_frequence" de liste_frequence_com
    frequence = liste_frequence_com[choix_frequence]
    # Concaténation de l'url du serveur et du reste de l'url pour avoir la route et récupérer les données
    url = url_server+ f"commande-station/{frequence}"
    # Envoie une requête à l'api avec l'url, les paramètres, et les headers
    response = requests.get(
        url, 
        params={
            "id-station":id_station, 
            "date-deb-periode":date_deb, 
            "date-fin-periode":date_fin}, 
        headers=headers)
    # Retourne la réponse au format json
    return response.json()

def commande_fichier(id_cmde: str) -> str:
    """_Permet d'obtenir les données de la commande passer grâce à la fonction obtenir_commande_station()_

    Args:
        id_cmde (str): _Identifiant de la commande passée_

    Returns:
        _str_: _Données au format text/csv_
    """
    # Concaténation de l'url du serveur et du reste de l'url pour avoir la route et récupérer les données
    url = url_server + "commande/fichier"
    # Envoie une requête http à l'api avec l'url, les paramètres, et les headers
    response = requests.get(
        url, 
        params={
            "id-cmde":id_cmde
        },
        headers=headers)
    # Retourne la réponse au format text/csv
    return response

def information_station(id_station: str):
    """_Permet d'obtenir les informations telles que les périodes d'actvités d'une station, et ses périodes d'enregistrement pour les différents paramètres avec différentes valeur_

    Args:
        id_station (str): _Identifiant de la station (unique)_
        date_deb (str): _Date de début de la période donnée_
        date_fin (str): _Date de fin de la période donnée_
        
    Returns:
        _str_: _Données concernant la station au format json_
    """
    # Concaténation de l'url du serveur et du reste de l'url pour avoir la route et récupérer les données
    url = url_server + "information-station"
    # Envoie une requête http à l'api avec l'url, les paramètres, et les headers
    response = requests.get(
        url,
        params={
            "id-station": id_station
        },
        headers=headers
    )
    # Retourne la réponse au format json
    return response.json()

print("Obtention de la liste des stations ayant enregistré des information à une certaine fréquence pour un certain paramètre.")

print("--- PARAMETRE ---", *list_parametre, sep="\n")
# Récupération/formatage du paramètre voulue (vent, precipitations etc.)
param = enlever_accents(input("Choix  :  ").lower())

print("--- FREQUENCE ---\n[1, 2, 3]", *liste_frequence, sep="\n")
# Récupération/cast de la fréquence d'enregistrement de la station
frequence = int(input("Choix  :  "))
# Récupération de la liste des stations disponibles avec les critères précédent
liste_station = obtenir_liste_station(frequence, num_dep, param)

print("\nObtention du numéro de commande pour une station donnée sur une période donnée.")

print(f"--- LISTE DES STATIONS DISPONIBLES DANS LE DEPARTEMENT {num_dep}")
# Affichage de la liste des stations disponibles (id, nom)
for elem in liste_station:
    print(elem["id"], elem["nom"])
# Récupération de l'identifiant de la station voulue
zone_station = input("Choisissez parmi les disponibles (id) : ")

print("--- FREQUENCE ---\n[1, 2, 3, 4, 5]", *liste_frequence_com, sep="\n")
# Récupération/cast de la fréquence pour la commande
commande_freq = int(input("Choix  :  "))

print("--- DATE DEBUT ---\n")
# Récupération de la date de début de période
annee_deb = input("Année (AAAA): ")
mois_deb = input("mois (MM) : ")
jour_deb = input("Jour (JJ) : ")
heure_deb = input("Heure (HH:HH:HH) : ")
# Concaténation des valeurs AAAA-MM-JJTHH:HH:HHZ
date_deb = f"{annee_deb}-{mois_deb}-{jour_deb}T{heure_deb}Z"

print("--- DATE FIN ---")
# Récupération de la date de fin de période
annee_fin = input("Année (AAAA): ")
mois_fin = input("mois (MM) : ")
jour_fin = input("Jour (JJ) : ")
heure_fin = input("Heure (HH:HH:HH) : ")
# Concaténation des valeurs AAAA-MM-JJTHH:HH:HHZ
date_fin = f"{annee_fin}-{mois_fin}-{jour_fin}T{heure_fin}Z"

# Récupération du numéro de la commande
commande = obtenir_commande_station(commande_freq, zone_station, date_deb, date_fin)["elaboreProduitAvecDemandeResponse"]["return"]

# Récupération du contenu de la commande
contenu_commande = commande_fichier(commande)

# Si attribut status_code de la commande = 200 (OK) alors
if contenu_commande.status_code == 200:
    # Formatage nom du fichier : dateDebut_dateFin_zoneStationFrequence.csv
    nom_fichier = f"{date_deb.replace(":", "")}_{date_fin.replace(":", "")}_{zone_station}{liste_frequence[frequence].upper()}.csv"

    chemin_dossier = os.path.join(os.path.dirname(__file__), "csv_data_registered")
    chemin_fichier = os.path.join(chemin_dossier, nom_fichier)

    csv_file = StringIO(contenu_commande)
    reader = csv.reader(csv_file, delimiter=";")

    if not os.path.exists(chemin_fichier):
        with open(chemin_fichier, "x", newline="", encoding="utf-8") as fichier:
            writer = csv.writer(fichier, delimiter=";")
            for row in reader:
                writer.writerow(row)
        print(f"Fichier {nom_fichier} crée dans {chemin_dossier} avec succès.")
    else:
        print(f"Fichier {nom_fichier} déjà existant dans {chemin_dossier}.")
else:
    print(contenu_commande.status_code)
    print(contenu_commande.text)
  

"""paire1 = ("2024-01-10T00:00:00Z", "2024-02-10T23:00:00Z")
paire2 = ("2024-04-01T00:00:00Z", "2024-05-31T23:00:00Z")
paire3 = ("2024-08-15T00:00:00Z", "2024-10-14T23:00:00Z")
print(obtenir_liste_station(2, "988", "vent"))
print(obtenir_commande_station(2, "98817104", paire1[0], paire1[1]))
print(commande_fichier("2025008800651"))"""







