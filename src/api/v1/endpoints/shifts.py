from api.dependencies import get_repository
from database.models import ShiftDay
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi_users_db_sqlalchemy import UUID_ID
from repositories.shifts import ShiftsRepository
from schemas.shifts import ShiftDayCreate, ShiftDayRead
from schemas.users import UserWithShifts

router = APIRouter()

get_shifts_repository = get_repository(ShiftDay, ShiftsRepository)


@router.get("/user/{user_id}", response_model=UserWithShifts)
async def get_user_with_shifts(
        user_id: UUID_ID = Path(..., title="User ID", description="The ID of the user to get shifts for"),
        shifts_repo: ShiftsRepository = Depends(get_shifts_repository),
        # user: User = Depends(current_active_user),
):
    user_with_shifts = await shifts_repo.get_master_with_shifts(user_id)
    if user_with_shifts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_with_shifts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShiftDayRead)
async def create_user_shift(
        data: ShiftDayCreate = Body(..., title="Shift data", description="The data of the shift to create"),
        shifts_repo: ShiftsRepository = Depends(get_shifts_repository),
        # user: User = Depends(current_active_user),
):
    shift = await shifts_repo.create_shift(data)
    if isinstance(shift, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=shift)
    return shift


@router.get("/{shift_id}", response_model=ShiftDayRead)
async def get_shift(
        shift_id: int,
        shifts_repo: ShiftsRepository = Depends(get_shifts_repository),
):
    shift = await shifts_repo.get(shift_id)
    if shift is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shift {shift_id} not found")
    return shift


@router.put("/{shift_id}", response_model=ShiftDayRead)
async def update_shift(
        shift_id: int,
        data: ShiftDayCreate = Body(..., title="Shift data", description="The data of the shift to update"),
        shifts_repo: ShiftsRepository = Depends(get_shifts_repository),
):
    shift = await shifts_repo.update(data, shift_id)
    if isinstance(shift, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=shift)
    return shift


@router.delete("/{shift_id}")
async def delete_shift(
        shift_id: int,
        shifts_repo: ShiftsRepository = Depends(get_shifts_repository),
):
    deleted = await shifts_repo.delete(shift_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shift {shift_id} not found")
    return {"message": f"Shift {shift_id} deleted"}
