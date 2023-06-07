import requests
import sys


def get_geocode(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?key={api_key}&address={address}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        return None

