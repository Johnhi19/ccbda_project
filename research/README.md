# Research topic

## Prerequesites
1. You need to have a spotify account (either free or premium). If you don't have an account, you have to register here https://www.spotify.com/es/signup

2. You need to have the curl command installed in your machine. If you don't have that you can follow the instructions provided here https://help.ubidots.com/en/articles/2165289-learn-how-to-install-run-curl-on-windows-macosx-linux

## Setting up the access to the Spotify API
### Create an App
1. Go to https://developer.spotify.com/ and log yourself in with your spotify account.

2. Go to your dashboard and create a new app. With the following properties:
    - ```App name = ccbda_research```
    - ```App description = Research topic for CCBDA```
    - ```Redirect URIs = http://localhost:3000``` (you don't need that but it is mandatory to specify)

3. Leave the rest blank and click the Developer Terms of Service checkbox and tap on the Create button

### Get the access token
1. After creating your app go to the settings of the app. Save your Client ID and your Client secret (available when you click on ```View client secret```) 

2. Create a new python file named ```research.py``` and copy the following code inside
```python
import base64
import json
import requests

CLIENT_ID = "YOUR-CLIENT-ID"
CLIENT_SECRET = "YOUR-CLIENT-SECRET"

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

def get_token():
    client_token = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('UTF-8')).decode('ascii')
    headers = {"Authorization": "Basic {}".format(client_token)}
    payload = {"grant_type": "client_credentials"}
    token_request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(token_request.text)["access_token"]
    return access_token
```

Replace ```YOUR-CLIENT-ID``` and ```YOUR-CLIENT-SECRET``` with the Client ID and the Client secret of your app. This function creates an access token valid for one hour. When you execute the code, the output looks something like this. 
```
BQDBKJ5eo5jxbtpWjVOj7ryS84khybFpP_lTqzV7uV-T_m0cTfwvdn5BnBSKPxKgEb11
```
### Get a random song
1. Add the following code to your python file
```python
import json
import random
import requests
import sys

def request_valid_song(access_token, genre=None):

    random_wildcards = ['%25a%25', 'a%25', '%25a',
                        '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i',
                        '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']
    wildcard = random.choice(random_wildcards)
    
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    
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
            artist = song_info['artists'][0]['name']
            song = song_info['name']
            break
        except IndexError:
            continue
        
    if song is None:
        print('Song Is None')
        artist = "Rick Astley"
        song = "Never Gonna Give You Up"
        
    return "{} - {}".format(artist, song)
```
2. And finally add the main function.
```python
def main():
    args = sys.argv[1:]
    n_args = len(args)

    access_token = get_token()
    
    result = request_valid_song(access_token)
    print(result)


if __name__ == '__main__':
    main()
```
When executing this code you should get a random song name with the artist.