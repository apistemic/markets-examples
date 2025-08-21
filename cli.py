import io
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

import httpx
import lxml.html
import pandas as pd
import tldextract
import typer
from sklearn.feature_extraction.text import TfidfVectorizer

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


def fetch_text_nofail(url) -> str | None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    try:
        resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None


def clean_html_text(html: str | None) -> str | None:
    if not html:
        return None
    doc = lxml.html.fromstring(html)
    # Remove script and style elements
    for elem in doc.xpath(".//script | .//style"):
        elem.getparent().remove(elem)
    return doc.text_content().strip()


@app.command()
def keywords():
    items = _fetch_items("linkedin:startupradar", "competitors")
    df = items_to_df(items)
    df = df.sample(n=20)

    # Take top 10 + random sample from remaining for proper TF-IDF corpus
    df_top = df.head(10)
    df_full = df

    df_full["organization.domain"] = (
        df_full["organization.website_url"]
        .apply(tldextract.extract)
        .apply(lambda x: x.top_domain_under_public_suffix)
    )

    df_full["html"] = df_full["organization.domain"].apply(
        lambda domain: fetch_text_nofail(f"https://{domain}")
    )

    with ThreadPoolExecutor(8) as tpe:
        texts = list(
            tpe.map(
                fetch_text_nofail,
                df_full["organization.domain"].apply(lambda x: f"https://{x}"),
            )
        )
    df_full["text"] = texts

    # Filter out None texts
    df_full_valid = df_full[df_full["text"].notna()]

    if len(df_full_valid) == 0:
        print("No valid text content found")
        return

    # Apply TF-IDF on full corpus for proper IDF calculation
    vectorizer = TfidfVectorizer(
        max_features=10_000,
        ngram_range=(1, 2),
        min_df=0.1,
        max_df=0.5,
        stop_words="english",
    )

    all_texts = df_full_valid["text"].tolist()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    feature_names = vectorizer.get_feature_names_out()

    df_tfidf = pd.DataFrame(
        data=tfidf_matrix.toarray(), columns=feature_names, index=df_full_valid.index
    )
    print(df_tfidf)

    print(df_tfidf.loc[df_top.index].mean(axis=0).sort_values(ascending=False).head(20))

    exit()
    # Get overall top keywords from top 10 competitors only
    top_10_matrix = tfidf_matrix[df_top.index]
    overall_scores = top_10_matrix.sum(axis=0).A1
    top_indices = overall_scores.argsort()[-20:][::-1]

    print("\n=== Top 20 Keywords from Top Competitors ===")
    for idx in top_indices:
        print(f"{feature_names[idx]}: {overall_scores[idx]:.3f}")

    # Get top keywords per top 10 companies
    print("\n=== Top Keywords per Top Competitor ===")
    for df_idx in df_top.index:
        if df_idx in df_full_valid.index:
            row = df_full_valid.loc[df_idx]
            scores = tfidf_matrix[df_full_valid.index.get_loc(df_idx)].toarray()[0]
            top_company_indices = scores.argsort()[-5:][::-1]
            print(f"\n{row['organization.name']} ({row['organization.domain']}):")
            for j in top_company_indices:
                if scores[j] > 0:
                    print(f"  - {feature_names[j]}: {scores[j]:.3f}")


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


def items_to_df(items: list[CompetitorItem]) -> pd.DataFrame:
    # all other formats are list-based
    items_data = [item.model_dump() for item in items]
    df = pd.json_normalize(items_data)

    # Convert nullable int columns to Int64 dtype
    int_columns = [
        "organization.id",
        "organization.employee_count",
        "organization.founded_year",
    ]
    for col in int_columns:
        if col in df.columns:
            df[col] = df[col].astype("Int64")

    return df


def _display_items(items: list[CompetitorItem], format: OutputFormat):
    """Display the data in the requested format."""
    # early return for non-list formats
    if format == OutputFormat.json:
        typer.echo(json.dumps([item.model_dump() for item in items], indent=2))
        return

    df = items_to_df(items)
    if format == OutputFormat.csv:
        typer.echo(df.to_csv(index=False))
    elif format == OutputFormat.parquet:
        buffer = io.BytesIO()
        df.to_parquet(buffer)
        typer.echo(buffer.getvalue(), nl=False)
    elif format == OutputFormat.table:
        # Format the table with better display options
        typer.echo(
            df.to_string(
                index=False,
                max_colwidth=20,
                float_format=lambda x: f"{x:.3f}" if pd.notna(x) else "",
            )
        )
    else:
        formats = ", ".join(OutputFormat.__members__.keys())
        raise ValueError(
            f"Unsupported format: {format}. Supported formats are: {formats}"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()
