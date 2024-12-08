from fastapi import APIRouter
from web import calendar

web_router = APIRouter()

web_router.include_router(
    calendar.router,
    prefix='/calendar',
    tags=['calendar'],
)
