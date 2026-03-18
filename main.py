from datetime import date
from typing import Optional

from fastapi import FastAPI, Query, HTTPException

from db import supabase
from schemas import Norma, NormasResponse

app = FastAPI(
    title="Diario Oficial de Chile — Normas Generales API",
    description="Public API to query normas generales published in the Diario Oficial de Chile.",
    version="1.0.0",
)

DEFAULT_LIMIT = 50
MAX_LIMIT = 500


@app.get("/normas", response_model=NormasResponse)
def list_normas(
    date_from: Optional[date] = Query(None, description="Filter from this date (inclusive, YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Filter up to this date (inclusive, YYYY-MM-DD)"),
    ministry: Optional[str] = Query(None, description="Filter by ministry (case-insensitive partial match)"),
    branch: Optional[str] = Query(None, description="Filter by branch (e.g. PODER EJECUTIVO)"),
    search: Optional[str] = Query(None, description="Full-text search on the norm title"),
    offset: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
):
    """List normas generales with optional filters."""
    query = supabase.table("normas_generales").select("*", count="exact")

    if date_from:
        query = query.gte("date", date_from.isoformat())
    if date_to:
        query = query.lte("date", date_to.isoformat())
    if ministry:
        query = query.ilike("ministry", f"%{ministry}%")
    if branch:
        query = query.ilike("branch", f"%{branch}%")
    if search:
        query = query.ilike("title", f"%{search}%")

    query = query.order("date", desc=True).range(offset, offset + limit - 1)

    result = query.execute()

    return NormasResponse(
        count=result.count if result.count is not None else len(result.data),
        data=result.data,
    )


@app.get("/normas/{cve}", response_model=Norma)
def get_norma_by_cve(cve: str):
    """Get a single norma by its CVE code."""
    result = (
        supabase.table("normas_generales")
        .select("*")
        .eq("cve", cve)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Norma not found")

    return result.data[0]


@app.get("/normas/dates/available", response_model=list[str])
def list_available_dates(
    limit: int = Query(30, ge=1, le=365),
):
    """List distinct dates that have published normas, most recent first."""
    result = (
        supabase.table("normas_generales")
        .select("date")
        .order("date", desc=True)
        .limit(1000)
        .execute()
    )

    seen = []
    for row in result.data:
        d = row["date"]
        if d not in seen:
            seen.append(d)
        if len(seen) >= limit:
            break

    return seen


@app.get("/normas/stats/by-ministry", response_model=list[dict])
def stats_by_ministry(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
):
    """Get count of normas grouped by ministry for a date range."""
    query = supabase.table("normas_generales").select("ministry")

    if date_from:
        query = query.gte("date", date_from.isoformat())
    if date_to:
        query = query.lte("date", date_to.isoformat())

    result = query.limit(10000).execute()

    counts: dict[str, int] = {}
    for row in result.data:
        m = row["ministry"] or "Unknown"
        counts[m] = counts.get(m, 0) + 1

    return sorted(
        [{"ministry": k, "count": v} for k, v in counts.items()],
        key=lambda x: x["count"],
        reverse=True,
    )
