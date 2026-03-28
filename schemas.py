from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class Norma(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    date: date
    edition: Optional[str] = None
    branch: Optional[str] = None
    ministry: Optional[str] = None
    organ: Optional[str] = None
    title: str
    pdf_url: Optional[str] = None
    cve: str
    created_at: Optional[datetime] = None


class NormasResponse(BaseModel):
    count: int
    data: list[Norma]
