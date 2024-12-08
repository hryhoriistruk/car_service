import enum
import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field
from schemas.shifts import UserShiftRead


class Role(str, enum.Enum):
    admin = "admin"
    master = "master"
    client = "client"


class CustomFields(BaseModel):
    username: str
    name: str | None = None
    surname: str | None = None
    phone: str | None = None
    tg_chat_id: int | None = None
    role: Role = Role.client
    email: EmailStr | None = None
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)


class UserRead(CustomFields, schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(CustomFields, schemas.BaseUserCreate):
    pass


class UserUpdate(CustomFields, schemas.BaseUserUpdate):
    pass


class UserWithShifts(UserRead):
    shifts: list[UserShiftRead] = []
