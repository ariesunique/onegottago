from fastapi import FastAPI
from google.cloud import datastore
from google.cloud.datastore.key import Key
from google.oauth2 import service_account
from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import List
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


def getClient():
    cred = service_account.Credentials.from_service_account_file("secret.json")
    return datastore.Client(credentials=cred)


def convertEntityToCard(entity):
    return Card(entity.key.id, entity["category"], entity["options"])


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