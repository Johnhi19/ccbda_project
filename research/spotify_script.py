import base64
import json
import random
import requests

CLIENT_ID = "764025cb6d2d4e829cea0cb06179e956"
CLIENT_SECRET = "4bd9ec038c554ceb8b637018f068a040"

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_CODE_BASE_URL = "https://scannables.scdn.co/uri/plain/jpeg/000000/white/640/"


def get_token():
    client_token = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode('UTF-8')).decode('ascii')
    headers = {"Authorization": f"Basic {client_token}"}
    payload = {"grant_type": "client_credentials"}
    token_request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(token_request.text)["access_token"]
    return access_token


def request_valid_song(access_token):
    random_wildcards = ['%25a%25', 'a%25', '%25a', '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i', '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']
    wildcard = random.choice(random_wildcards)
    authorization_header = {"Authorization": f"Bearer {access_token}"}

    song = None
    for _ in range(51):
        try:
            song_request = requests.get(
                f'{SPOTIFY_API_URL}/search?q={wildcard}&type=track&offset={random.randint(0, 100)}',
                headers=authorization_header
            )
            song_info = random.choice(json.loads(song_request.text)['tracks']['items'])
            song_uri =  SPOTIFY_CODE_BASE_URL + song_info['uri']
            artist = song_info['artists'][0]['name']
            song = song_info['name']
            return f"{artist} - {song} <img src='{song_uri}'/>"
        except IndexError:
            continue

    return "Rick Astley - Never Gonna Give You Up <img src='https://scannables.scdn.co/uri/plain/jpeg/000000/white/640/spotify:track:4uLU6hMCjMI75M1A2tKUQC'/>"