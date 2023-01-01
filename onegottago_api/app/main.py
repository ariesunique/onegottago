from fastapi import FastAPI
from google.cloud import datastore
from google.cloud.datastore.key import Key
from google.oauth2 import service_account
from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import List, Dict
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

project = os.environ.get("gcp_project")

@dataclass
class Card:
    id: str
    category: str
    options: List[str] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)


def getClient():
    cred = service_account.Credentials.from_service_account_file("secret.json")
    return datastore.Client(credentials=cred)


def convertEntityToCard(entity):
    card = Card(entity.key.id, entity["category"], entity["options"])
    if "stats" in entity:
        card.stats = convertEntityToStats(entity["stats"])
    return card


def convertEntityToStats(entity):
    stats = {}
    for key in entity:
        stats[key] = entity[key]
    return stats


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cards", response_model=List[Card])
async def list_cards():
    results = []
    datastore_client = getClient()
    query = datastore_client.query(kind='Card')
    query_results = list(query.fetch())

    for entity in query_results:
        card = convertEntityToCard(entity)
        results.append(card)

    return results


@app.get("/cards/{card_id}", response_model=Card)
async def get_card(card_id: int):
    datastore_client = getClient()
    entity = datastore_client.get(Key('Card', card_id, project=project))

    return convertEntityToCard(entity)


@app.put("/cards/{card_id}")
async def update_card(card_id: int, incoming_card: Card):
    # this is only for updating the stats
    datastore_client = getClient()
    entity = datastore_client.get(Key('Card', card_id, project=project))
    entity["stats"] = incoming_card.stats
    datastore_client.put(entity)


@app.put("/cards/{card_id}/options/{option_index}")
async def update_card_selected_option(card_id: int, option_index: str):
    # another method to update the stats; only requires client to send the selected option
    datastore_client = getClient()
    entity = datastore_client.get(Key('Card', card_id, project=project))
    stats_obj = {} if "stats" not in entity else entity["stats"]
    stats_obj[option_index] = stats_obj.get(option_index, 0) + 1
    stats_obj["total"] = stats_obj.get("total", 0) + 1
    entity["stats"] = stats_obj
    datastore_client.put(entity)

