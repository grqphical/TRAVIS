"""Tool to get current weather conditions for your city"""

from tools import BaseTool
import requests
import json
import urllib.parse


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

        for key, value in currentData.items():
            currentData[key] = f"{value}{units[key]}"

        print(currentData)

        return json.dumps({"result": json.dumps(currentData)})
