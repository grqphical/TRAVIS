"""T.R.A.V.I.S (Trusty Robot Assistant for Virtual Ideas and Solutions)

A configurable virtual assistant
"""

from groq import Groq
from dotenv import load_dotenv

MODEL = "llama-3.3-70b-versatile"

load_dotenv()

client = Groq()

prompt = input("What do you want to say?: ")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model=MODEL,
)
print(chat_completion.choices[0].message.content)
