from datetime import date

from database.repository import DatabaseRepository
from fastapi_users_db_sqlalchemy import UUID_ID
from schemas.shifts import ShiftDayCreate
from sqlalchemy import and_, exists, select
from sqlalchemy.orm import joinedload, selectinload

from src.database.models import ShiftDay, User


class ShiftsRepository(DatabaseRepository[ShiftDay]):

    async def get_master_with_shifts(self, user_id: UUID_ID) -> User:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.shifts))
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def check_shift_already_exists(self, user_id: UUID_ID, today: date) -> bool:
        stmt = (
            select(
                exists().where(
                    and_(
                        ShiftDay.date == today,
                        ShiftDay.master_id == user_id,
                    ),
                ),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create_shift(self, data: ShiftDayCreate) -> ShiftDay | str:
        master_shift_exists = await self.check_shift_already_exists(data.master_id, data.date)
        if master_shift_exists:
            return "Shift already exists or the user is not a master"
        shift = ShiftDay(**data.model_dump())
        self.session.add(shift)
        await self.session.commit()
        await self.session.refresh(shift)
        return shift

    async def get_shifts_between_dates(
            self, start_date: date = date.today(), end_date: date = date.today(),
    ) -> list[ShiftDay]:
        stmt = (
            select(ShiftDay)
            .options(joinedload(ShiftDay.master).load_only(User.name))
            .where(ShiftDay.date.between(start_date, end_date))
            .order_by(ShiftDay.date)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, data: ShiftDayCreate, pk: int) -> ShiftDay | str:
        shift: ShiftDay = await super().get(pk)
        # Check if shift already exists on this day
        if shift.master_id != data.master_id or shift.date != data.date:
            master_exists = await self.check_shift_already_exists(data.master_id, data.date)
            if master_exists:
                return "This master already has a shift on this day"
        return await super().update(data, pk)
