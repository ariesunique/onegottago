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

        # update the stats TODO error handling
        requests.put(f"{api_url}/cards/{card_id}/options/{option_index}")

        return redirect(url_for("index"))

    id = random.choice(ids)

    response = requests.get(f"{api_url}/cards/{id}")
    json_response = response.json()
    category = json_response["category"]
    options = json_response["options"]

    return render_template('index.html', card_id=id, category=category, options=options)


if __name__ == '__main__':
    app.run(debug=True, port='8080', host='0.0.0.0') 