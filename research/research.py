import base64
import json
import random
import requests
import sys

CLIENT_ID = "764025cb6d2d4e829cea0cb06179e956"
CLIENT_SECRET = "4bd9ec038c554ceb8b637018f068a040"

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

def get_token():
    client_token = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('UTF-8')).decode('ascii')
    headers = {"Authorization": "Basic {}".format(client_token)}
    payload = {"grant_type": "client_credentials"}
    token_request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(token_request.text)["access_token"]
    return access_token


def request_valid_song(access_token, genre=None):

    # Wildcards for random search
    random_wildcards = ['%25a%25', 'a%25', '%25a',
                        '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i',
                        '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']
    wildcard = random.choice(random_wildcards)
    
    # Make a request for the Search API with pattern and random index
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    
    # Cap the max number of requests until getting RICK ASTLEYED
    song = None
    for i in range(51):
        try:
            song_request = requests.get(
                '{}/search?q={}&type=track&offset={}'.format(
                    SPOTIFY_API_URL,
                    wildcard,
                    random.randint(0, 100)
                ),
                headers = authorization_header
            )
            song_info = random.choice(json.loads(song_request.text)['tracks']['items'])
            song_uri = 'https://scannables.scdn.co/uri/plain/jpeg/000000/white/640/'+song_info['uri']
            artist = song_info['artists'][0]['name']
            song = song_info['name']
            break
        except IndexError:
            continue
        
    if song is None:
        print('Song Is None')
        artist = "Rick Astley"
        song = "Never Gonna Give You Up"
        
    return "{} - {} \n{}".format(artist, song, song_uri)


def main():
    args = sys.argv[1:]
    n_args = len(args)

    # Get a Spotify API token
    access_token = get_token()
    
    # Call the API for a song that matches the criteria
    result = request_valid_song(access_token)
    print(result)


if __name__ == '__main__':
    main()

# https://scannables.scdn.co/uri/plain/jpeg/000000/white/640/
