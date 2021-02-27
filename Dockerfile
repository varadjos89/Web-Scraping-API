FROM python:3.7-slim AS base

ENV DB_HOST db
EXPOSE 8080

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY household_api.py .

COPY web_scrapper.py .

RUN python3 web_scrapper.py

CMD [ "python", "household_api.py" ]
