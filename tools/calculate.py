"""Calculator tool for TRAVIS"""

from tools import BaseTool
import json


class CalculateTool(BaseTool):
    def tool_schema():
        return {
            "type": "function",
            "function": {
                "name": "CalculateTool",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }

    def run_tool(**kwargs) -> dict[str]:
        """Evaluate a mathematical expression"""
        try:
            # Attempt to evaluate the math expression

            result = eval(kwargs.get("expression", "default"))

            return json.dumps({"result": result})

        except:

            # Return an error message if the math expression is invalid

            return json.dumps({"error": "Invalid expression"})
