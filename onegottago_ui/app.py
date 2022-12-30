from flask import Flask, render_template
import random
import requests


app = Flask(__name__)
app.config.from_pyfile("settings.py")

@app.route('/')
def index():

    api_url = app.config.get("API_URL")
    ids = app.config.get("DATASTORE_IDS").split(",")

    id = random.choice(ids)

    response = requests.get(f"{api_url}/cards/{id}")
    json_response = response.json()
    category = json_response["category"]
    options = json_response["options"]

    return render_template('index.html', category=category, options=options)


if __name__ == '__main__':
    app.run(debug=True, port='8080', host='0.0.0.0') 