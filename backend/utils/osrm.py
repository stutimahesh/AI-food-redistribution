import requests

from config import Config


BASE_URL = Config.OSRM_BASE_URL


def get_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon
):
    """
    Get shortest driving route using OSRM.
    """

    coordinates = (
        f"{start_lon},{start_lat};"
        f"{end_lon},{end_lat}"
    )

    url = (
        f"{BASE_URL}"
        f"/route/v1/driving/"
        f"{coordinates}"
        f"?overview=false"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:

            return None

        data = response.json()

        route = data["routes"][0]

        return {

            "distance_km":
            round(route["distance"] / 1000, 2),

            "duration_minutes":
            round(route["duration"] / 60),

        }

    except Exception:

        return None


def get_eta(
    donor_lat,
    donor_lon,
    ngo_lat,
    ngo_lon
):

    route = get_route(

        donor_lat,
        donor_lon,

        ngo_lat,
        ngo_lon

    )

    if route:

        return route["duration_minutes"]

    return None