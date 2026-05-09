from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Agent, Report, ReportPhoto
from app.schemas import ReportCreate, ReportCreateResponse

router = APIRouter(prefix="/api/reports", tags=["api-reports"])


@router.post("", response_model=ReportCreateResponse)
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    agent = db.execute(select(Agent).where(Agent.phone == payload.agent_phone)).scalar_one_or_none()
    if not agent:
        agent = Agent(full_name=payload.agent_name, phone=payload.agent_phone)
        db.add(agent)
        db.flush()

    report = Report(
        agent_id=agent.id,
        address=payload.address,
        landmark=payload.landmark,
        client_code=payload.client_code,
        last_trade_agent_visit=payload.last_trade_agent_visit,
        stand_code=payload.stand_code,
        client_comment=payload.client_comment,
        conclusion=payload.conclusion,
        created_at=payload.created_at or datetime.utcnow(),
    )
    db.add(report)
    db.flush()

    for photo in payload.photos:
        db.add(
            ReportPhoto(
                report_id=report.id,
                photo_type=photo.photo_type,
                photo_link=photo.photo_link,
            )
        )

    db.commit()
    return ReportCreateResponse(ok=True, report_id=report.id)
