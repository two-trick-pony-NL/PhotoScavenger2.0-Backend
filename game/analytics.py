


import requests
import base64
import json


MIXPANEL_API_URL = "https://api-eu.mixpanel.com/track"  # EU endpoint if your project is EU


def track_event(username: str, event_name: str, properties: dict = None):
    properties = properties or {}

    # Base payload
    payload = {
        "event": event_name,
        "properties": {
            "token": "325989db6648780254d7b0be51d01777",
            "distinct_id": str(username),
            **properties
        }
    }

    # Mixpanel expects base64-encoded JSON in 'data' parameter
    data = base64.b64encode(json.dumps(payload).encode("utf-8"))
    requests.post(MIXPANEL_API_URL, data={"data": data})
