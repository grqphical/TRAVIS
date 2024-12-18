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
                "description": "Gets the current NHL game scores. If a game has ended (isGameRunning is equal to false) tell the user the result and the fact that it has ended",
                "parameters": {
                    "team": {
                        "type": "string",
                        "description": "The team the user wants to get the scores for. Don't include the city, just the team name",
                    }
                },
                "required": ["team"],
            },
        }

    def run_tool(**kwargs):
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

            if (
                game["homeTeam"]["name"]["default"] == kwargs["team"]
                or game["awayTeam"]["name"]["default"] == kwargs["team"]
            ):

                if game["clock"]["running"]:
                    return json.dumps(
                        {
                            "result": json.dumps(
                                {
                                    "home": game["homeTeam"]["name"]["default"],
                                    "away": game["awayTeam"]["name"]["default"],
                                    "period": game["period"],
                                    "isGameRunning": True,
                                    "timeRemaining": game["clock"]["timeRemaining"],
                                    "homeGoals": home_goals,
                                    "awayGoals": away_goals,
                                }
                            )
                        }
                    )
                else:
                    return json.dumps(
                        {
                            "result": json.dumps(
                                {
                                    "home": game["homeTeam"]["name"]["default"],
                                    "away": game["awayTeam"]["name"]["default"],
                                    "isGameRunning": False,
                                    "homeGoals": home_goals,
                                    "awayGoals": away_goals,
                                }
                            )
                        }
                    )

        return json.dumps({"result": "The team is not playing tonight"})
