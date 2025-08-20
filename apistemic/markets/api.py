import logging
import os
from abc import ABC
from urllib.parse import urljoin

import httpx

from apistemic.markets.models import CompetitorItem
from apistemic.markets.models import CompetitorsResponse
from apistemic.markets.models import LookalikesResponse

LOGGER = logging.getLogger(__name__)


class ApiBackend(ABC):
    def get(self, endpoint) -> httpx.Response: ...


class MarketsApi(ABC):
    api_backend: ApiBackend

    def __init__(self, api_backend: ApiBackend):
        self.api_backend = api_backend

    def get_competitors(self, slug: str) -> CompetitorsResponse:
        response = self.api_backend.get(f"/{slug}/competitors")
        response.raise_for_status()
        return CompetitorsResponse.model_validate(response.json())

    def get_competitors_with_original(self, slug: str) -> list[CompetitorItem]:
        response = self.get_competitors(slug)
        return [
            CompetitorItem(organization=response.organization, score=1.0)
        ] + response.competitors

    def get_lookalikes(self, slug: str) -> LookalikesResponse:
        response = self.api_backend.get(f"/{slug}/lookalikes")
        # Note: The API returns the same structure but with 'competitors' key
        # We need to map it to 'lookalikes' for the response model
        data = response.json()
        if "competitors" in data:
            data["lookalikes"] = data.pop("competitors")
        return LookalikesResponse.model_validate(data)

    def get_lookalikes_with_original(self, slug: str) -> list[CompetitorItem]:
        response = self.get_lookalikes(slug)
        return [
            CompetitorItem(organization=response.organization, score=1.0)
        ] + response.lookalikes


class RapidApiBackend(ApiBackend):
    RAPIDAPI_HOST = "market-intelligence-competitors-lookalikes-and-more.p.rapidapi.com"
    rapidapi_key: str

    def __init__(self, rapidapi_key: str):
        self.rapidapi_key = rapidapi_key

    def get(self, endpoint: str) -> httpx.Response:
        base_url = f"https://{self.RAPIDAPI_HOST}"
        url = urljoin(base_url, endpoint)
        resp = httpx.get(
            url,
            headers={
                "x-rapidapi-key": self.rapidapi_key,
                "x-rapidapi-host": self.RAPIDAPI_HOST,
            },
            # slugs currently redirect to actual organization ID
            follow_redirects=True,
        )
        resp.raise_for_status()
        return resp


class RegularApiBackend(ApiBackend):
    def get(self, endpoint: str) -> httpx.Response:
        base_url = "https://competitor-api.apistemic.com"
        url = urljoin(base_url, endpoint)
        resp = httpx.get(url, follow_redirects=True)
        resp.raise_for_status()
        return resp


def create_markets_api_from_environment() -> MarketsApi:
    """Creates a MarketsAPI depending on the found environment variables"""
    backend: ApiBackend
    if os.environ.get("RAPIDAPI_API_KEY"):
        LOGGER.info("using RapidAPI backend")
        backend = RapidApiBackend(os.environ["RAPIDAPI_API_KEY"])
    else:
        LOGGER.warning("using un-authenticated API, rate limits apply")
        backend = RegularApiBackend()

    return MarketsApi(backend)
