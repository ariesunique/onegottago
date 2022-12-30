FROM python:3.10-alpine

ENV gcp-project=${GCP_PROJECT}

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./secret.json /code/secret.json

RUN pip install --no-cache-dir  --trusted-host pypi.python.org --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

