import math


EARTH_RADIUS_KM = 6371.0


def haversine(lat1, lon1, lat2, lon2):
    """
    Returns distance between two GPS coordinates in kilometers.
    """

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return EARTH_RADIUS_KM * c


def estimate_eta(distance_km, average_speed=40):
    """
    Estimate travel time in minutes.
    """

    if average_speed <= 0:
        return 0

    return round((distance_km / average_speed) * 60)


def distance_score(distance):

    """
    Higher score for shorter distance.
    """

    return 1 / (1 + distance)