from datetime import date, datetime, time

from fastapi_users_db_sqlalchemy import UUID_ID
from pydantic import BaseModel, Field


class ShiftDayBase(BaseModel):
    date: date
    time_start: time
    time_end: time
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)


class ShiftDayCreate(ShiftDayBase):
    master_id: UUID_ID | None = None


class ShiftDayRead(ShiftDayCreate):
    id: int  # noqa: A003


class UserShiftRead(ShiftDayBase):
    id: int  # noqa: A003
