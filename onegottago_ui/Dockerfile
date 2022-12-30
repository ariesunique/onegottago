FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

ENTRYPOINT ["python", "app.py"]