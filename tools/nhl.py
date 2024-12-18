"""This tool retrieves current NHL scores"""

from tools import BaseTool
import requests
import json


class NHLGamesTool(BaseTool):
    def tool_schema():
        return {
            "type": "function",
            "function": {
                "name": "NHLGamesTool",
                "description": "Gets the current NHL game scores",
                "parameters": {},
            },
        }

    def run_tool(**kwargs):
        current_game_data = []
        response = requests.get("https://api-web.nhle.com/v1/score/now")

        if not response.ok:
            return json.dumps({"error": "Unable to contact the NHL API"})

        payload = response.json()

        rawGameData = payload["games"]

        for game in rawGameData:
            home_goals = 0
            away_goals = 0

            for goal in game["goals"]:
                if goal["teamAbbrev"] == game["homeTeam"]["abbrev"]:
                    home_goals += 1
                else:
                    away_goals += 1

            current_game_data.append(
                {
                    "home": game["homeTeam"]["name"]["default"],
                    "away": game["awayTeam"]["name"]["default"],
                    "period": game["period"],
                    "timeRemaining": game["clock"]["timeRemaining"],
                    "running": game["clock"]["running"],
                    "homeGoals": home_goals,
                    "awayGoals": away_goals,
                }
            )

        return json.dumps({"result": json.dumps(current_game_data)})
