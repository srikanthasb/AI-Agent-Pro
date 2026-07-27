import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def get_ai_response(username, message):

    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={"username": username, "message": message},
        timeout=130,
    )

    response.raise_for_status()

    return response.json()["response"]
