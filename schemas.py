from datetime import date
from typing import Optional

from pydantic import BaseModel


class Norma(BaseModel):
    id: int
    date: date
    edition: Optional[str] = None
    branch: Optional[str] = None
    ministry: Optional[str] = None
    organ: Optional[str] = None
    title: str
    pdf_url: Optional[str] = None
    cve: str
    created_at: Optional[str] = None


class NormasResponse(BaseModel):
    count: int
    data: list[Norma]
