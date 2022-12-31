FROM python:3.10-alpine

ARG FLASK_DEBUG="false"
ENV FLASK_DEBUG="${FLASK_DEBUG}"
ENV api_url=${API_URL}
ENV ids=${DATASTORE_IDS}

WORKDIR /app

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .


# https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app