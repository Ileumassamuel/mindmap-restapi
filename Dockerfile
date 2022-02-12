FROM python:3.10-alpine

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENV FLASK_ENV=production

RUN pip install waitress

EXPOSE 3000
ENTRYPOINT [ "waitress-serve", "--call", "0.0.0.0:3000", "index:app" ]
