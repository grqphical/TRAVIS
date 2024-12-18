"""Tool to get current weather conditions for your city"""

from tools import BaseTool
import requests
import json
import urllib.parse

weather_codes = {
    0: "Clear sky",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Freezing fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    56: "Light freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


class WeatherTool(BaseTool):
    def tool_schema():
        return {
            "type": "function",
            "function": {
                "name": "WeatherTool",
                "description": "Get the current weather conditions for the user's city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city to get the weather from",
                        }
                    },
                    "required": ["city"],
                },
            },
        }

    def run_tool(**kwargs):
        # get the coordinates for the user's city
        city_url_safe = urllib.parse.quote(kwargs["city"])
        response = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city_url_safe}&count=10&language=en&format=json"
        )

        if not response.ok:
            print("ERROR: Request Failed To Geocoding API:", response.text)
            return json.dumps({"error": "Failed to access the API"})

        response_json = response.json()["results"][0]
        latitude, longitude = response_json["latitude"], response_json["longitude"]

        weather_response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation,weather_code,wind_speed_10m"
        )

        if not weather_response.ok:
            print("ERROR: Request Failed To Weather API:", response.text)
            return json.dumps({"error": "Failed to access the API"})

        currentData = weather_response.json()["current"]
        units = weather_response.json()["current_units"]

        currentData["weather_conditions"] = weather_codes[currentData["weather_code"]]
        currentData.pop("weather_code")

        for key, value in currentData.items():
            if key == "weather_conditions":
                continue
            currentData[key] = f"{value}{units[key]}"

        print(currentData)

        return json.dumps({"result": json.dumps(currentData)})
