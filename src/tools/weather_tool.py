import requests

import os

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city: str):
    """Get the current weather of a city."""
    url = "http://api.weatherapi.com/v1/current.json"

    params = {"key": API_KEY, "q": city, "aqi": "no"}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"Error: {response.text}"

    data = response.json()

    return (
        f"Weather in {data['location']['name']}\n"
        f"Temperature : {data['current']['temp_c']}°C\n"
        f"Condition   : {data['current']['condition']['text']}\n"
        f"Humidity    : {data['current']['humidity']}%\n"
        f"Wind Speed  : {data['current']['wind_kph']} km/h"
    )
