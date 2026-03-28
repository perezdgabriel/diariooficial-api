from datetime import date
from typing import Optional

from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from db import get_db, NormaGeneralDB
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
    db: Session = Depends(get_db),
):
    """List normas generales with optional filters."""
    query = db.query(NormaGeneralDB)
    count_query = db.query(func.count(NormaGeneralDB.id))

    if date_from:
        query = query.filter(NormaGeneralDB.date >= date_from)
        count_query = count_query.filter(NormaGeneralDB.date >= date_from)
    if date_to:
        query = query.filter(NormaGeneralDB.date <= date_to)
        count_query = count_query.filter(NormaGeneralDB.date <= date_to)
    if ministry:
        query = query.filter(NormaGeneralDB.ministry.ilike(f"%{ministry}%"))
        count_query = count_query.filter(NormaGeneralDB.ministry.ilike(f"%{ministry}%"))
    if branch:
        query = query.filter(NormaGeneralDB.branch.ilike(f"%{branch}%"))
        count_query = count_query.filter(NormaGeneralDB.branch.ilike(f"%{branch}%"))
    if search:
        query = query.filter(NormaGeneralDB.title.ilike(f"%{search}%"))
        count_query = count_query.filter(NormaGeneralDB.title.ilike(f"%{search}%"))

    total = count_query.scalar()
    rows = query.order_by(NormaGeneralDB.date.desc()).offset(offset).limit(limit).all()

    print('rows:', rows)

    return NormasResponse(count=total, data=rows)


@app.get("/normas/{cve}", response_model=Norma)
def get_norma_by_cve(cve: str, db: Session = Depends(get_db)):
    """Get a single norma by its CVE code."""
    row = db.query(NormaGeneralDB).filter(NormaGeneralDB.cve == cve).first()
    if not row:
        raise HTTPException(status_code=404, detail="Norma not found")
    return row


@app.get("/normas/dates/available", response_model=list[str])
def list_available_dates(
    limit: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    """List distinct dates that have published normas, most recent first."""
    rows = (
        db.query(NormaGeneralDB.date)
        .distinct()
        .order_by(NormaGeneralDB.date.desc())
        .limit(limit)
        .all()
    )
    return [row.date.isoformat() for row in rows]


@app.get("/normas/stats/by-ministry", response_model=list[dict])
def stats_by_ministry(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Get count of normas grouped by ministry for a date range."""
    query = db.query(
        NormaGeneralDB.ministry,
        func.count(NormaGeneralDB.id).label("count"),
    )

    if date_from:
        query = query.filter(NormaGeneralDB.date >= date_from)
    if date_to:
        query = query.filter(NormaGeneralDB.date <= date_to)

    rows = query.group_by(NormaGeneralDB.ministry).order_by(func.count(NormaGeneralDB.id).desc()).all()

    return [{"ministry": row.ministry or "Unknown", "count": row.count} for row in rows]
