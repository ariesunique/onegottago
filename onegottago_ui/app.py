from flask import Flask, render_template, request, redirect, url_for, session
import random
import requests
import logging
from dotenv import load_dotenv
import json

load_dotenv('.env')
app = Flask(__name__)
app.config.from_pyfile("settings.py")




@app.before_request
def getCardIds():
    if "ids" not in session or len(session['ids']) == 0:
        logging.info("loading ids from datastore and saving to session")
        ids = None
        try:
            api_url = app.config.get("API_URL")
            response = requests.get(f"{api_url}/cards/ids")
            ids = json.loads(response.text)
        except Exception as e:
            logging.warn("Problem loading the card ids from datastore", e)

        if ids:
            session['ids'] = ids



@app.route('/', methods=['GET', 'POST'])
def index():
    SKIP_OPTION = "99"

    api_url = app.config.get("API_URL")

    if request.method == "POST":
        card_id = request.form.get("card_id")
        option_index = request.form.get("option", SKIP_OPTION)
        skip = request.form.get("skip")

        if not card_id:
            logging.warning("The card id is null (and that shouldn't be). Something might have gone wrong.")
            return redirect(url_for("index"))

        if not option_index and not skip:
            logging.warning("The user neither selected an option, nor clicked the skip button. That shouldn't happen")
            return redirect(url_for("index"))

        try:
            if not (option_index >= "0" and option_index < "4"):
                logging.warning(f"Invalid option selected; exepct int between 0 and 3, got {option_index}")
                option_index = SKIP_OPTION

            if skip:
                option_index = SKIP_OPTION
            # update the stats
            requests.put(f"{api_url}/cards/{card_id}/options/{option_index}")
        except Exception as e:
            logging.error("Unable to update the stats", e)

        return redirect(url_for("stats", card_id=card_id))

    id = random.choice(session.get("ids", []))

    if not id:
        return redirect(url_for("page_not_found"))

    # TODO error handling here
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500



if __name__ == '__main__':
    app.run(debug=True, port='8080', host='0.0.0.0') 