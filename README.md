# 🎵 Billboard 100 Spotify Playlist Generator

Ce projet vous permet de **créer automatiquement une playlist Spotify** à partir du classement **Billboard Hot 100** d'une date donnée. Il combine du web scraping avec `BeautifulSoup` et l'API Spotify via `Spotipy`.

---

## 📌 Fonctionnalités

- 🔍 Scraping du site [Billboard](https://www.billboard.com/charts/hot-100/) pour récupérer les 100 meilleures chansons d'une date choisie
- 🎧 Recherche des titres sur Spotify avec l'API officielle
- ✅ Filtrage intelligent pour associer les bons artistes aux chansons
- 📂 Création automatique d’une playlist Spotify avec les titres trouvés

---

## 🛠️ Technologies utilisées

- [Python 3](https://www.python.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/en/master/)
- [Spotipy (Spotify API Wrapper)](https://spotipy.readthedocs.io/en/2.22.1/)

---

## ⚙️ Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/ton_nom_utilisateur/billboard-spotify-playlist.git
   cd billboard-spotify-playlist

## 🔐 Configuration de l'accès Spotify
Aller sur le Dashboard Spotify Developer

Créer une application pour obtenir :

client_id

client_secret

redirect_uri (ex: https://example.org/callback)

Modifier les variables dans le script :

python
Copier
Modifier
sportify_client_id = "VOTRE_CLIENT_ID"
sportify_client_key = "VOTRE_CLIENT_SECRET"
sportify_redirection_link = "VOTRE_REDIRECT_URI"

## ▶️ Utilisation
Lancer le script :

bash
Copier
Modifier
python main.py
Saisir la date souhaitée au format :

css
Copier
Modifier
YYYY-MM-DD
Le script :

Scrape les chansons Billboard

Les recherche sur Spotify

Crée une playlist dans ton compte

## 📄 Licence
Ce projet est sous licence MIT. 

## 🙌 Remerciements
Billboard.com pour les classements hebdomadaires

Spotify pour l’API musicale

La communauté Python 🐍

## ✍️ Auteur
Riantseheno Miandry Nathan Mandatiana

LinkedIn | GitHub


