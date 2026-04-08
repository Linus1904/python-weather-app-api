import requests

def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name,
              "count": 1,
              "language": "de",
              "format": "json",
              }
    response = requests.get(url, params=params)
    if  response.status_code == 200:
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            city_data = data["results"][0]
            latitude = city_data["latitude"]
            longitude = city_data["longitude"]
            city = city_data["name"]
            return latitude, longitude, city

        else:
            print("Stadt nicht gefunden.")
            return None

    else:
        print(f"Fehler beim Abrufen der Koordinaten: {response.status_code}")
        return None

def get_weather_info(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude,
              "longitude": longitude,
              "current_weather": True,
              "daily": ["temperature_2m_max", "temperature_2m_min"],
              "timezone": "auto",
              "forecast_days": 5
              }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler beim abrufen der Wetterdaten: {response.status_code}")
        return None

city_name = input("Stadt eingeben:").strip()
coordinates = get_coordinates(city_name)

if coordinates:
    latitude, longitude, city = coordinates
    weather_info = get_weather_info(latitude, longitude)

    if weather_info:
        if "current_weather" not in weather_info or "daily" not in weather_info:
            print("Unvollständige Wetterdaten erhalten")
        current_weather = weather_info["current_weather"]
        daily = weather_info["daily"]
        weather_codes = {
        0: "Klar",
        1: "Überwiegend klar",
        2: "Teilweise bewölkt",
        3: "Bewölkt",
        45: "Neblig",
        48: "Reifnebel",
        51: "Leichter Nieselregen",
        53: "Mäßiger Nieselregen",
        55: "Starker Nieselregen",
        61: "Leichter Regen",
        63: "Mäßiger Regen",
        65: "Starker Regen",
        71: "Leichter Schneefall",
        73: "Mäßiger Schneefall",
        75: "Starker Schneefall",
        80: "Leichte Regenschauer",
        81: "Mäßige Regenschauer",
        82: "Starke Regenschauer",
        95: "Gewitter"
        }

        print(f"\nStadt: {city}")
        print(f"Aktuelle Temperatur: {current_weather['temperature']} Grad Celsius")
        print(f"Windgeschwindigkeit: {current_weather['windspeed']} km/h")
        print(f"Wetterbeschreibung: {weather_codes.get(current_weather["weathercode"],'unbekannt')}")
        print(f"Zeitpunkt: {current_weather['time']}")

        print("\nHeute:")
        print(f"Höchste Temperatur: {daily['temperature_2m_max'][0]} Grad Celsius")
        print(f"Niedrigste Temperatur: {daily['temperature_2m_min'][0]} Grad Celsius")

        print("\nHöchsttemperaturen der nächsten Tage:")
        for i in range(1,len(daily['time'])):
            print(f"{daily['time'][i]}: {daily['temperature_2m_max'][i]} Grad Celsius")