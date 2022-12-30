# One Gotta Go API

This is the API layer for One Gotta Go.

## Installation

### Local Install

1. clone the `onegottago` repo
2. `cd {installdir}/onegottago_api`
3. create a python virtual env `python3 -m venv venv; source venv/bin/activate; pip install --upgrade pip`
4. install from requirements `pip install -r requirements.txt`

**To Run**
```bash
cd app
uvicorn main:app --reload
```

Verify that it worked (you should see Hello World):
http://127.0.0.1:8000/

```json
{
"message": "Hello World"
}
```

**Database Setup**

To really test this, you need to create a new Google Cloud Project and enable Cloud Datastore. 

Then go to "IAM & Admin" > "Service Accounts"; Click "Create Service Account"; Give it a useful name and description and for Role, choose `Cloud Datastore User`; Generate a key for this service account

Download your service account key and save it to "secret.json" in the same directory with "main.py"

TBD: Load sample data into your Datastore database

http://127.0.0.1:8000/cards



### Via Docker

**Prerequisitie** - Need to already have docker installed on your system.

1. clone the `onegottago` repo
2. `cd {installdir}/onegottago_api`
3. touch secret.json
   
```bash
docker build -t onegottago_api .

docker run -d -p 8080:8080 onegottago_api
```

Verify that it worked (you should see Hello World):
http://127.0.0.1:8080/

```json
{
"message": "Hello World"
}
```

## Deployment

