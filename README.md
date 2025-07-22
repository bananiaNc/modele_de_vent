# **Récupération des Données Climatique - via API MétéoFrance**

Ce scrpit Python permet d'interroger l'API publique de MétéoFrance pour:

* Obtenir la liste des stations météoroligiques enregistrant des données pour un paramètre donné à intervalle régulier.
* Générer une commande pour télécharger des données météorologiques sur une période définie.
* Récupérer les données au format CSV et les enregistrer localement.

## **Prérequis**

* Python 3.7 ou plus
* Bibliothèque Python : requests, json, cs, unicodedata, os
* Un compte utilisateur pour l'API publique de Météofrance : [Création d'un compte utilisateur API publique météofrance](https://portail-api.meteofrance.fr/authenticationendpoint/login.do?client_id=q86Efxg3AWJQ2KJQ25EZsJw1cfAa&code_challenge=j9od4ajyCtjSmGsRqSOOlxEW_Ib-Y3kL6d5FZTCI5BY&code_challenge_method=S256&commonAuthCallerPath=%2Foauth2%2Fauthorize&forceAuth=false&passiveAuth=false&redirect_uri=https%3A%2F%2Fportail-api.meteofrance.fr%2Fweb%2Ffr&response_mode=query&response_type=code&scope=openid+profile+apim%3Asubscribe&state=request_0&tenantDomain=carbon.super&sessionDataKey=609dafe8-2c6b-4879-a99e-68b33b7c9594&relyingParty=q86Efxg3AWJQ2KJQ25EZsJw1cfAa&type=oidc&sp=apim_portail&isSaaSApp=true&authenticators=BasicAuthenticator%3ALOCAL)
* Un token d'accès valide à l'API publique de Météofrance : [Portail Api MétéoFrance](https://portail-api.meteofrance.fr/web/fr/)

## Installation

Aucune installation particulière n'est nécessaire. Clonez ce dépôt et éxecutez le fichier Python :

```bash
git clone https://
```

## Utilisation

Le script se lance via la ligne de commande et vous guide étape par étape:

1. Choisissez un paramètre climatique (ex: Températture, Vent, Précipitations, etc.).
2. Séléctionnez la fréquence d'enregistrement (6 minutes, horaire, quotidienne, etc.).
3. Choisissez une station météo parmi celles disponibles dans le département.
4. Indiquez la période souhaitée (date de début, date de fin).
5. Les données sont téléchargées au format CSV dans le dossier csv_data_registered.

### Exemple de fichier généré

```bash
csv_data_registered/
└── 2024-01-01T00-00-00Z_2024-01-31T23-00-00Z_98817104QUOTIDIENNE.csv
```

## Fonctionnalités

* **Recherche de stations** : basé sur le département et le paramètre choisi.
* **Commande de données**: séléction de la fr"quence et de la période de temps
* **Export CSV**: automatique si les données sont disponibles.

## Paramètres disponibles

* Précipitations
* Température
* Humidité
* Vent
* Pression
* Rayonnement
* Insolation
* Etat de la mer
* ETP quotidienne

## Fréquence supportées

* infrahoraire-6m
* horaire
* quotidienne
* decadaire
* mensuelle

## Remarques

* Le **token API** est actuellement codé en dur dans le script. Ne pas exposer en public. La durée d'un token est d'une heure, lorsque le délai est dépassé il est obligatoire de générer un nouveau token via la session ouverte et ensuite de remplacer l'ancien token, par sa nouvelle valeur généré.
* Le script est configuré pour interroger les stations en **Nouvelle-Calédonie** (num_dep="988).
* Le dossier csv_data_registered sera automatiquement crée s'il n'existe pas.

## Structure des fonctions

* obtenir_liste_stations(...) : liste les stations par paramètre/fréquence/département.
* obtenir_commande_station(...) : génère une commande d'extraction de données
* commande_fichier(...) : télécharge les données de la commande au format CSV.
* information_station(...) : affiche les métadonnées d'une station
* enlever_accents(...) : nettoie les accents dans les chaînes des caractères.

## Exemple d'utilisation

```python
obtenir_liste_station(2, "988", "vent")
obtenir_commande_station(2, "98817104", "2024-01-01T00:00:00Z", "2024-01-31T23:00:00Z")
commande_fichier("2025008800651")
```
