import io
import json
import logging
from enum import Enum

import pandas as pd
import typer

from apistemic.markets.api import create_markets_api_from_environment
from apistemic.markets.models import CompetitorItem

app = typer.Typer()


class OutputFormat(str, Enum):
    table = "table"
    json = "json"
    csv = "csv"
    parquet = "parquet"


class Endpoint(str, Enum):
    competitors = "competitors"
    lookalikes = "lookalikes"


@app.command()
def leadgen():
    pass


@app.command()
def fetch(
    endpoint: Endpoint = typer.Argument(..., help="Type of data to fetch"),
    slug: str = typer.Argument(
        ...,
        help=(
            "company identifier, can be company ID, Linkedin slug or domain name."
            " For example, to get Uber"
            " both `linkedin:uber-com` and `domain:uber.com` work"
        ),
    ),
    format: OutputFormat = typer.Option(OutputFormat.table, help="Output format"),
):
    """
    Fetch competitors or lookalikes for a given company.
    """
    # Step 1: Fetch data
    items = _fetch_items(slug, endpoint.value)

    # Step 2: Display data
    _display_items(items, format)


def _fetch_items(
    slug: str,
    endpoint: str,
) -> list[CompetitorItem]:
    """Fetch data from the API and apply limit if specified."""
    api = create_markets_api_from_environment()

    if endpoint == "competitors":
        items = api.get_competitors_with_original(slug)
    else:  # lookalikes
        items = api.get_lookalikes_with_original(slug)

    return items


def _display_items(items: list[CompetitorItem], format: OutputFormat):
    """Display the data in the requested format."""
    # early return for non-list formats
    if format == OutputFormat.json:
        typer.echo(json.dumps([item.model_dump() for item in items], indent=2))
        return

    # all other formats are list-based
    items_data = [item.model_dump() for item in items]
    df = pd.json_normalize(items_data)

    if format == OutputFormat.csv:
        typer.echo(df.to_csv(index=False))
    elif format == OutputFormat.parquet:
        buffer = io.BytesIO()
        df.to_parquet(buffer)
        typer.echo(buffer.getvalue(), nl=False)
    elif format == OutputFormat.table:
        typer.echo(df)
    else:
        formats = ", ".join(OutputFormat.__members__.keys())
        raise ValueError(
            f"Unsupported format: {format}. Supported formats are: {formats}"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()
