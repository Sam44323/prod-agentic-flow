import requests


def get_weather(latitude: float, longitude: float) -> str:
    """
    Fetch the current weather from Open-Meteo.
    """

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,wind_speed_10m"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return (
        f"Temperature: {current['temperature_2m']}°C, "
        f"Wind Speed: {current['wind_speed_10m']} km/h"
    )
