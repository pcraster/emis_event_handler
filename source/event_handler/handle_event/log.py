import requests


def log(
        uri,
        timestamp,
        priority,
        severity,
        message):

    payload = {
        "timestamp": timestamp,
        "priority": priority,
        "severity": severity,
        "message": message
    }

    response = requests.post(uri, json={"log": payload})

    if response.status_code != 201:
        raise RuntimeError(response.json()["message"])
