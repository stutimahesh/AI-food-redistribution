from models.driver import Driver

from utils.geo import haversine


def assign_driver(

    donor_lat,

    donor_lon

):

    drivers = Driver.query.filter_by(

        available=True

    ).all()

    if len(drivers) == 0:

        return None

    nearest = None

    minimum = float("inf")

    for driver in drivers:

        distance = haversine(

            donor_lat,

            donor_lon,

            driver.current_latitude,

            driver.current_longitude

        )

        if distance < minimum:

            minimum = distance

            nearest = driver

    if nearest:

        nearest.available = False

    return nearest