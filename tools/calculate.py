"""Calculator tool for TRAVIS"""

from tools import BaseTool
import json


class CalculateTool(BaseTool):
    def run_tool(**kwargs) -> dict[str]:
        """Evaluate a mathematical expression"""
        try:
            # Attempt to evaluate the math expression

            result = eval(kwargs.get("expression", "default"))

            return json.dumps({"result": result})

        except:

            # Return an error message if the math expression is invalid

            return json.dumps({"error": "Invalid expression"})
