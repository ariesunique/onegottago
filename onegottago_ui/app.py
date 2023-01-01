from flask import Flask, render_template, request, redirect, url_for
import random
import requests
from dotenv import load_dotenv

load_dotenv('.env')
app = Flask(__name__)
app.config.from_pyfile("settings.py")

@app.route('/', methods=['GET', 'POST'])
def index():

    api_url = app.config.get("API_URL")
    ids = app.config.get("DATASTORE_IDS").split(",")

    if request.method == "POST":
        card_id = request.form["card_id"]
        option_index = request.form["option"]

        # update the stats and TODO add error handling
        requests.put(f"{api_url}/cards/{card_id}/options/{option_index}")

        return redirect(url_for("stats", card_id=card_id))

    id = random.choice(ids)

    response = requests.get(f"{api_url}/cards/{id}")
    json_response = response.json()
    category = json_response["category"]
    options = json_response["options"]

    return render_template('index.html', card_id=id, category=category, options=options)


@app.route('/stats/<card_id>', methods=['GET'])
def stats(card_id=None):
    api_url = app.config.get("API_URL")
    json_response = requests.get(f"{api_url}/cards/{card_id}").json()
    category = json_response["category"]
    options = json_response["options"]
    stats_obj = json_response["stats"]
    
    return render_template('stats.html', card_id=card_id, category=category, options=options, stats=stats_obj)

if __name__ == '__main__':
    app.run(debug=True, port='8080', host='0.0.0.0') 