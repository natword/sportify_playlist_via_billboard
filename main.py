from pprint import pprint
from unidecode import unidecode

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Identifiants Spotify (à personnaliser selon ton application)
sportify_client_id = "VOTRE_CLIENT_ID"
sportify_client_key = "VOTRE_CLIENT_SECRET"
sportify_redirection_link = "VOTRE_REDIRECT_URI"

# ------------------- Recherche des meilleures chansons sur Billboard -------------------
# Demande à l'utilisateur une date au format YYYY-MM-DD pour voyager dans le temps
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Définition des en-têtes pour la requête HTTP (simule un navigateur pour éviter le blocage)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
}

# URL de la page Billboard pour la date donnée
billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

# Récupération et analyse du HTML de la page
billboard_html = requests.get(billboard_url, headers=header).text
soup = BeautifulSoup(billboard_html, "html.parser")

# Extraction des titres des chansons
songs = []
for song in soup.select(".o-chart-results-list-row-container ul li ul li #title-of-a-story"):
    songs.append(song.getText().replace('\n', '').replace('\t', ''))

# Extraction des artistes associés
best_artists = []
for artist in soup.select(".o-chart-results-list-row-container ul li ul li span.a-no-trucate"):
    best_artists.append(artist.getText().replace('\n', '').replace('\t', ''))

# Association des chansons et des artistes dans une liste de dictionnaires
best_songs = []
for i in range(len(songs)):
    song = {"song": songs[i], "artist": best_artists[i]}
    best_songs.append(song)

# --------------------- Authentification via Spotify API --------------------------------
# Création de l'objet Spotipy pour gérer l'authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=sportify_client_id,
    client_secret=sportify_client_key,
    redirect_uri=sportify_redirection_link,
    scope="playlist-modify-public playlist-modify-private"
))

# Récupération de l'ID utilisateur Spotify
user_id = sp.current_user()["id"]

# ---------------------------- Recherche de chansons -------------------------------------
# Liste pour stocker les URIs des chansons trouvées sur Spotify
song_sportify_uri = []
year = date[:4]  # Extraction de l'année pour affiner les recherches

# Fonction pour comparer les artistes avec une normalisation Unicode
def match_artist(spotify_artist, target_artist):
    return unidecode(spotify_artist.lower()) in unidecode(target_artist.lower())

# Recherche chaque chanson sur Spotify et tente de trouver une correspondance
for song in best_songs:
    track = unidecode(song['song'].strip())
    artist = unidecode(song['artist'].strip())

    print(f"\n🔍 Recherche : {track} - {artist}")
    result = sp.search(q=f"track:{track} year:{year}", type="track", limit=10)

    found = False
    for item in result["tracks"]["items"]:
        item_artist = item["artists"][0]["name"]
        if match_artist(item_artist, artist):
            uri = item["uri"]
            song_sportify_uri.append(uri)
            print(f"✅ Match : {track} by {item_artist} → {uri}")
            found = True
            break

    if not found:
        print(f"❌ Aucun match exact trouvé pour : {track} - {artist}")

# ---------------------- Création de la playlist ----------------------------------------
# Récupération du jeton d'accès pour effectuer des requêtes à l'API Spotify
access_token = sp.auth_manager.get_access_token(as_dict=False)

# Configuration des en-têtes pour l'authentification
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Paramètres pour la création de la playlist
create_playlist_enpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
create_parameters = {
    "name": f"Billboard {date} Top 100 Songs",
    "public": "true",
}

# Envoi de la requête pour créer une playlist
create_response = requests.post(url=create_playlist_enpoint, headers=headers, json=create_parameters)
playlist = create_response.json()

# Récupération de l'ID et du lien de la playlist
playlist_id = playlist["id"]
playlist_link = playlist["external_urls"]["spotify"]

# ------------------------------ Gestion de la playlist ---------------------------------
# Ajout des chansons trouvées à la playlist créée
sp.playlist_add_items(playlist_id, song_sportify_uri)

# Affichage du lien vers la playlist
print(f"Here is the link: {playlist_link}")
