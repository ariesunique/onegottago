from google.cloud import datastore
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import argparse
import json

load_dotenv()

project = os.environ.get("gcp_project")
secret_file = os.environ.get("secret_file")


def load(filename):
    cred = service_account.Credentials.from_service_account_file(secret_file)
    datastore_client = datastore.Client(credentials=cred)

    with open(filename) as f:
        data = json.load(f)
        for card in data["cards"]:
            card_entity_key = datastore_client.key("Card")
            card_entity = datastore.Entity(key=card_entity_key)
            card_entity.update(card)
            datastore_client.put(card_entity)

    print("Done. Loaded ")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load data into datastore")
    parser.add_argument('filename', help='name of the json file containing the data')
    args = parser.parse_args()
    load(args.filename)
