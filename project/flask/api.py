import requests
import json 

# API endpoint
url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"
urlAirports = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchAirport"

def get_airport(headers, location):
    querystring = {"query": location}
    response = requests.get(urlAirports, headers=headers, params=querystring)
    data = response.json()
    entityId = data["data"][0]["entityId"]
    skyId = data["data"][0]["skyId"]
    return entityId, skyId

def get_flights(headers, originSkyId, destinationSkyId, originEntityId, destinationEntityId, date):
    querystring = {
        "originSkyId": originSkyId,
        "destinationSkyId": destinationSkyId,
        "originEntityId": originEntityId,
        "destinationEntityId": destinationEntityId,
        "date": date
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

def extract_flight_info(data):
    final_data = {}
    # final_data["totalResults"] = data["data"]["context"]["totalResults"] 
    # final_data["status"] = data["data"]["context"]["status"]
    flights = []
    for flight in data["data"]["itineraries"]:
        flight_data = {}
        flight_data["id"] = flight["id"]
        flight_data["price"] = flight["price"]["formatted"]
        flight_data["origin"] = flight["legs"][0]["origin"]["name"] + " (" + flight["legs"][0]["origin"]["id"] + ")"
        flight_data["destination"] = flight["legs"][0]["destination"]["name"] + " (" + flight["legs"][0]["destination"]["id"] + ")"
        flight_data["departure"] = flight["legs"][0]["departure"]
        flight_data["arrival"] = flight["legs"][0]["arrival"]
        flight_data["duration"] = flight["legs"][0]["durationInMinutes"]
        flight_data["stops"] = flight["legs"][0]["stopCount"]
        flight_data["airline"] = flight["legs"][0]["carriers"]["marketing"][0]["name"]
        flight_data["logoUrl"] = flight["legs"][0]["carriers"]["marketing"][0]["logoUrl"]
        flight_data["flightNumber"] = flight["legs"][0]["segments"][0]["flightNumber"]
        flights.append(flight_data)
    
    final_data["flights"] = flights

    return final_data
    # with open('final_data.json', 'w') as f:
    #     json.dump(final_data, f, indent=4) 


def flights(origin, destination, date):
    headers = {
    "X-RapidAPI-Key": "f27b563b20mshe084557d3a4279ep191acfjsn242aae6fe20b",
    "X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
    }
    
    originEntityId, originSkyId = get_airport(headers, origin)
    destinationEntityId, destinationSkyId = get_airport(headers, destination)
    data = get_flights(headers, originSkyId, destinationSkyId, originEntityId, destinationEntityId, date)
    final_data = extract_flight_info(data)
    return final_data



#flights("London", "New York", "2024-07-04")
