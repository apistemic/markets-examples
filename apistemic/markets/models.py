from typing import List, Optional

from pydantic import BaseModel
import pandas as pd


class Organization(BaseModel):
    id: int
    name: str
    description: str
    website_url: Optional[str] = None
    linkedin_url: str
    employee_count: int
    founded_year: Optional[int] = None


class CompetitorItem(BaseModel):
    organization: Organization
    score: float


class CompetitorsResponse(BaseModel):
    organization: Organization
    competitors: List[CompetitorItem]


class LookalikesResponse(BaseModel):
    organization: Organization
    lookalikes: List[CompetitorItem]


def competitors_response_to_df(response: CompetitorsResponse) -> pd.DataFrame:
    competitors = [comp.model_dump() for comp in response.competitors]
    return pd.json_normalize(competitors)
