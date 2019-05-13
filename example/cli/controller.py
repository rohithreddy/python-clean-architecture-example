from decimal import getcontext
from typing import TextIO

import click

from .adapter import from_domain, create_customer_coordinates
from example.config import DEFAULTS
from example.core import use_cases
from example.core.entities.exceptions import BaseError
from example.core.entities.geo import Point, Distance

getcontext().prec = 7


@click.command()
@click.argument("file_stream", type=click.File("r"))
@click.option(
    "--max-distance",
    default=DEFAULTS["distance_in_km"],
    type=float,
    help="max distance from office in kilometers",
)
@click.option(
    "--office-latitude",
    default=DEFAULTS["office_latitude"],
    type=float,
    help="office decimal latitude",
)
@click.option(
    "--office-longitude",
    default=DEFAULTS["office_longitude"],
    type=float,
    help="office decimal longitude",
)
def run(
    file_stream: TextIO,
    max_distance: float,
    office_latitude: float,
    office_longitude: float,
) -> None:
    """Finds the nearest customers from the office."""
    try:
        sorted_customers_nearby = use_cases.find_nearest_customer(
            office_coordinate=Point.of(
                latitude=office_latitude, longitude=office_longitude
            ),
            max_distance_from_office=Distance.of(max_distance),
            customer_coordinates=create_customer_coordinates(file_stream.readlines()),
        )

    except BaseError as error:
        click.echo(error)
    else:
        click.echo(from_domain(sorted_customers_nearby))