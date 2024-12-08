from datetime import date

from api.dependencies import get_repository
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from repositories.shifts import ShiftsRepository

from src.database.models import ShiftDay

router = APIRouter()
templates = Jinja2Templates(directory="templates")

get_shifts_repository = get_repository(ShiftDay, ShiftsRepository)


@router.get("/", response_class=HTMLResponse)
async def render_calendar(
        request: Request,
        shifts_repo: ShiftsRepository = Depends(get_shifts_repository),
        start_date: date | None = date.today(),
        end_date: date | None = date.today(),
):
    try:
        result: list[ShiftDay] = await shifts_repo.get_shifts_between_dates(start_date, end_date)
        shifts = {}
        for shift in result:
            shifts.setdefault(shift.date, [])
            shifts[shift.date].append(
                {
                    'id': shift.id,
                    'time_start': shift.time_start,
                    'time_end': shift.time_end,
                    'master': shift.master.name,
                },
            )
        return templates.TemplateResponse(
            "shifts.html", {"request": request, "shifts": shifts},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
