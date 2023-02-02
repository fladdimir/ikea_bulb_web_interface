from flask import Flask, request, send_from_directory

import src.bulb_control as bc

bc.connect()
bc.client.loop_start()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return send_from_directory("static", "index.html")


@app.route("/state", methods=["GET", "POST"])
def state():
    if request.method == "GET":
        return bc.getState()
    if request.method == "POST":
        data: dict = request.get_json(force=True)
        bc.setState(data)
        return "", 200


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
