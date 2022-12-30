FROM python:3.10-alpine

ENV api_url=${API_URL}
ENV ids=${DATASTORE_IDS}

WORKDIR /app

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

ENTRYPOINT ["python", "app.py"]