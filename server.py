from flask import Flask, request, abort
from assistant import send_message
from config import load_config

app = Flask(__name__)

config = load_config()

system_prompt = f"""
You are T.R.A.V.I.S (Trusty Robot Assistant for Virtual Ideas and Solutions). You are a virtual assistant whose job is to assist users
with any tasks they may have. You have a set of tools available to you to do things you cannot do on your own, use them when necessary.

Here is some information about your user:

{config.to_json()}
"""


@app.route("/")
def status():
    return "TRAVIS is online"


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.form.get("prompt", None)
    if prompt == None:
        abort(400, description="no prompt provided")

    response = send_message([{"role": "system", "content": system_prompt}], prompt)
    return response
