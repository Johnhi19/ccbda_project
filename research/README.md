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
1. After creating your app go to the settings. Save your Client ID and your Client secret (available when you click on ```View client secret```) 

2. Go to the directory of the research project and open a terminal. Copy and paste the following command

```
curl -X POST "https://accounts.spotify.com/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=YOUR-CLIENT-ID&client_secret=YOUR-CLIENT-SECRET"
     > credentials.txt
```

This will create an access token valid for 1 hour. The access token will look something like this