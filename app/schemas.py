from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ReportPhotoIn(BaseModel):
    photo_type: str = Field(..., examples=["stand", "product", "outside"])
    photo_link: str = ""


class ReportCreate(BaseModel):
    agent_name: str
    agent_phone: str
    address: str
    landmark: str = ""
    client_code: str = ""
    last_trade_agent_visit: str = ""
    stand_code: str = ""
    client_comment: str = ""
    conclusion: str = ""
    created_at: Optional[datetime] = None
    photos: List[ReportPhotoIn] = []


class ReportCreateResponse(BaseModel):
    ok: bool
    report_id: int
