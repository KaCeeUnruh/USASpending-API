from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch_data")
def fetch_data():
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)
    return jsonify(response.json()['results'])

    if __name__ == '__main__':
        app.run()
