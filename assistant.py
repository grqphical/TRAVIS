"""T.R.A.V.I.S (Trusty Robot Assistant for Virtual Ideas and Solutions)

A configurable virtual assistant
"""

from groq import Groq
from dotenv import load_dotenv
from tools import BaseTool
import json

MODEL = "llama-3.3-70b-versatile"

load_dotenv()

client = Groq()

prompt = input("What do you want to say?: ")

messages = [
    {
        "role": "system",
        "content": "you have a calculate function available. Use it if the user wants to calculate a math expression.",
    },
    {
        "role": "user",
        "content": prompt,
    },
]

tools = []

for tool in BaseTool.plugins.values():
    tools.append(tool.tool_schema())

response = client.chat.completions.create(
    messages=messages,
    model=MODEL,
    tools=tools,
    tool_choice="auto",
    max_tokens=4096,
    stream=False,
)

response_message = response.choices[0].message

tool_calls = response_message.tool_calls

if tool_calls:

    # Define the available tools that can be called by the LLM

    available_functions = BaseTool.plugins

    # Add the LLM's response to the conversation

    messages.append(response_message)

    # Process each tool call

    for tool_call in tool_calls:

        function_name = tool_call.function.name

        function_to_call = available_functions[function_name].run_tool

        function_args = json.loads(tool_call.function.arguments)

        # Call the tool and get the response

        function_response = function_to_call(expression=function_args.get("expression"))

        # Add the tool response to the conversation

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",  # Indicates this message is from tool use
                "name": function_name,
                "content": function_response,
            }
        )

    # Make a second API call with the updated conversation

    second_response = client.chat.completions.create(model=MODEL, messages=messages)

print(second_response.choices[0].message.content)
