import requests
import argparse
import json  # Import json for file operations

# Set up the argument parser
parser = argparse.ArgumentParser(description='Search for flights using the Sky Scrapper API.')
parser.add_argument('--originSkyId', default='LOND', type=str, required=False, help='Sky ID for the origin location.')
parser.add_argument('--destinationSkyId', default='NYCA', type=str, required=False, help='Sky ID for the destination location.')
parser.add_argument('--originEntityId', default='27544008', type=str, required=False, help='Entity ID for the origin location.')
parser.add_argument('--destinationEntityId', default='27537542', type=str, required=False, help='Entity ID for the destination location.')
parser.add_argument('--date', type=str, required=True, help='Date for the flight search (YYYY-MM-DD).')
parser.add_argument('--adults', type=str, default='1', help='Number of adults.')
parser.add_argument('--currency', type=str, default='USD', help='Currency to display prices in.')
parser.add_argument('--market', type=str, default='en-US', help='Market language for results.')
parser.add_argument('--countryCode', type=str, default='US', help='Country code.')

# Parse the arguments
args = parser.parse_args()

# API endpoint
url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"

# Prepare the querystring using the parsed arguments
querystring = {
    "originSkyId": args.originSkyId,
    "destinationSkyId": args.destinationSkyId,
    "originEntityId": args.originEntityId,
    "destinationEntityId": args.destinationEntityId,
    "date": args.date,
    "adults": args.adults,
    "currency": args.currency,
    "market": args.market,
    "countryCode": args.countryCode
}

# Headers for the request
headers = {
    "X-RapidAPI-Key": "f27b563b20mshe084557d3a4279ep191acfjsn242aae6fe20b",
    "X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
}

# Send the GET request
response = requests.get(url, headers=headers, params=querystring)

# Get the JSON response data
data = response.json()

# Save the JSON data to a file
with open('flight_results.json', 'w') as f:
    json.dump(data, f, indent=4)  # Indent for pretty printing

# Optionally, print the JSON data to the console
print(data)
