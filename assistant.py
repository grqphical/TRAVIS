"""T.R.A.V.I.S (Trusty Robot Assistant for Virtual Ideas and Solutions)

A configurable virtual assistant
"""

from groq import Groq
from dotenv import load_dotenv
from tools import BaseTool
import typing
import json

MODEL = "llama-3.3-70b-versatile"

load_dotenv()

client = Groq()
tools = []

for tool in BaseTool.plugins.values():
    tools.append(tool.tool_schema())


def send_message(
    message_history: typing.List[typing.Dict[str, str]], prompt: str
) -> str:
    """Sends a message to TRAVIS and returns the response"""
    message_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    response = client.chat.completions.create(
        messages=message_history,
        model=MODEL,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096,
        stream=False,
    )

    response_message = response.choices[0].message
    message_history.append(response_message)

    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = BaseTool.plugins

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name].run_tool
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(
                expression=function_args.get("expression")
            )

            message_history.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        second_response = client.chat.completions.create(
            model=MODEL, messages=message_history
        )
        return second_response.choices[0].message.content
    else:
        return response_message.content
