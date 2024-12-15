from flask import Flask, request, abort
from assistant import send_message

app = Flask(__name__)


@app.route("/")
def status():
    return "TRAVIS is online"


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.form.get("prompt", None)
    if prompt == None:
        abort(400, description="no prompt provided")

    response = send_message([], prompt)
    return response
