import os

API_URL = os.environ.get("API_URL")
DATASTORE_IDS = os.environ.get("DATASTORE_IDS")
SECRET_KEY = os.environ.get("SECRET_KEY") or "my-secret"
