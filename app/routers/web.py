from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.config import settings
from app.db import get_db
from app.models import Agent, Report
from app.security import check_admin_login, require_login

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["web"])


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = ""):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error, "title": settings.app_title},
    )


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if not check_admin_login(username, password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Login yoki parol noto'g'ri", "title": settings.app_title},
            status_code=400,
        )

    request.session["admin_logged_in"] = True
    return RedirectResponse("/", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


@router.get("/", response_class=HTMLResponse)
@require_login
async def dashboard(request: Request, db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    total_reports = db.scalar(select(func.count(Report.id))) or 0
    today_reports = db.scalar(
        select(func.count(Report.id)).where(Report.created_at >= today, Report.created_at < tomorrow)
    ) or 0
    total_agents = db.scalar(select(func.count(Agent.id))) or 0

    latest_reports = db.execute(
        select(Report)
        .options(selectinload(Report.agent), selectinload(Report.photos))
        .order_by(Report.id.desc())
        .limit(10)
    ).scalars().all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "title": settings.app_title,
            "total_reports": total_reports,
            "today_reports": today_reports,
            "total_agents": total_agents,
            "latest_reports": latest_reports,
        },
    )


@router.get("/reports", response_class=HTMLResponse)
@require_login
async def reports_page(
    request: Request,
    db: Session = Depends(get_db),
    q: str = "",
    agent: str = "",
):
    stmt = (
        select(Report)
        .options(selectinload(Report.agent), selectinload(Report.photos))
        .order_by(Report.id.desc())
    )

    if q:
        stmt = stmt.where(
            or_(
                Report.address.ilike(f"%{q}%"),
                Report.landmark.ilike(f"%{q}%"),
                Report.client_code.ilike(f"%{q}%"),
                Report.client_comment.ilike(f"%{q}%"),
                Report.conclusion.ilike(f"%{q}%"),
                Report.rm_info.ilike(f"%{q}%"),
            )
        )

    if agent:
        stmt = stmt.join(Agent).where(Agent.full_name.ilike(f"%{agent}%"))

    reports = db.execute(stmt).scalars().all()

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "title": settings.app_title,
            "reports": reports,
            "q": q,
            "agent": agent,
        },
    )


@router.get("/reports/{report_id}", response_class=HTMLResponse)
@require_login
async def report_detail(request: Request, report_id: int, db: Session = Depends(get_db)):
    report = db.execute(
        select(Report)
        .where(Report.id == report_id)
        .options(selectinload(Report.agent), selectinload(Report.photos))
    ).scalar_one_or_none()

    if not report:
        return RedirectResponse("/reports", status_code=303)

    return templates.TemplateResponse(
        "report_detail.html",
        {
            "request": request,
            "title": settings.app_title,
            "report": report,
        },
    )


@router.post("/reports/{report_id}/update")
@require_login
async def update_report_manual_fields(
    request: Request,
    report_id: int,
    rm_info: str = Form(""),
    resolution_date: str = Form(""),
    db: Session = Depends(get_db),
):
    report = db.execute(select(Report).where(Report.id == report_id)).scalar_one_or_none()
    if not report:
        return RedirectResponse("/reports", status_code=303)

    report.rm_info = rm_info.strip()
    report.resolution_date = resolution_date.strip()
    db.add(report)
    db.commit()

    return RedirectResponse(f"/reports/{report_id}", status_code=303)