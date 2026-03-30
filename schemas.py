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


# --- Reglamentos ---

class Etapa(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    etapa: Optional[str] = None
    fecha: Optional[date] = None
    accion: Optional[str] = None
    sector: Optional[str] = None
    observaciones: Optional[str] = None
    documento: Optional[str] = None
    documento_url: Optional[str] = None
    gobierno_actual: bool = False


class Reglamento(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    numero: str
    anio: str
    ministerio: str
    subsecretaria: Optional[str] = None
    materia: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    estado: Optional[str] = None
    categoria: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ReglamentoDetail(Reglamento):
    etapas: list[Etapa] = []


class ReglamentosResponse(BaseModel):
    count: int
    data: list[Reglamento]


class ReglamentoStats(BaseModel):
    ministerio: str
    count: int


class ReglamentoTimeline(BaseModel):
    reglamento_id: int
    numero: str
    anio: str
    ministerio: str
    materia: Optional[str] = None
    categoria: str
    estado: Optional[str] = None
    ultima_etapa_fecha: Optional[date] = None
    ultima_etapa_accion: Optional[str] = None
    total_etapas: int


class NormaDestacada(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    date: date
    explanation: str
    norma: Norma
