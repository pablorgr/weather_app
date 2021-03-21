from os import getenv
from sys import argv

from datetime import timedelta
from urllib.parse import unquote

from flask import Flask, jsonify, make_response, request
from flask_pymongo import PyMongo

from requests import get


app = Flask(__name__)

app.secret_key = bytes(getenv("SECRET"), encoding="utf-8")
app.permanent_session_lifetime = timedelta(days=365)

app.config["MONGO_URI"] = "mongodb://mongo:27017/api"
mongo = PyMongo(app)

RESTCOUNTRIES = "https://restcountries.eu/rest/v2/all"
OPENWEATHER = (
    f"http://api.openweathermap.org/data/2.5/weather?units=metric&APPID={getenv('API_KEY')}"
)


def populate():
    """Helper function to populate database with city and weather info.

    Get city names from restcountries.eu and populate database collection.
    Get weather information from each city and populate another collection.
    """
    print("Populating database. This could take a while...")
    weather_info = []
    response = get(RESTCOUNTRIES)
    if response.ok:
        for country in response.json():
            city = country["capital"]
            weather_response = get(f"{OPENWEATHER}&q={city}")
            if weather_response.ok:
                weather_info.append(
                    {"city": unquote(city).lower(), "info": weather_response.json()}
                )
    if weather_info:
        # bypass document validation in order to avoid errors with '.' in dict keys
        mongo.db.weather.insert_many(weather_info, bypass_document_validation=True)


@app.route("/", methods=["GET"])
def main():
    """Retrieve weather information

    Get weather information from database filtered by city name.
    If no weather info populate database first.

    :return response:
    """
    query = {}
    city = request.args.get("city")
    if city:
        query["city"] = unquote(city).lower()
    if getenv("FLASK_ENV") == "development":
        app.logger.info(f"query: {query}")
    result = [
        {"city": cursor["city"], "info": cursor["info"]}
        for cursor in mongo.db.weather.find(query)
    ]
    if len(result) == 1:
        result = result.pop()
    return make_response(jsonify(result))


if __name__ == "__main__":
    if argv[1] in ("-p", "--populate"):
        populate()