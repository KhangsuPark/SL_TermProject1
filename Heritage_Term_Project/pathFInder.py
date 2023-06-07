import requests

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

api_key = "AIzaSyBB47PEev4ghi50AZ3j3Xf-VcMGxgX67fc"  # 여기에 발급받은 Google Maps Geocoding API 키를 입력하세요.
address = '경기도 시흥시 산기대학로 237 한국공학대학교'  # 여기에 주소를 입력하세요.
latitude, longitude = get_geocode(address, api_key)
if latitude and longitude:
    print("위도:", latitude)
    print("경도:", longitude)
else:
    print("위도와 경도를 가져올 수 없습니다.")