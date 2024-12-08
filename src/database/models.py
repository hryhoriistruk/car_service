from datetime import date, datetime, time
from typing import Annotated

from fastapi_users_db_sqlalchemy import UUID_ID, SQLAlchemyBaseUserTableUUID
from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text, Time, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config import db_settings

DATABASE_URL = db_settings.url


class Base(DeclarativeBase):
    pass


created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', NOW())"))]
updated_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', NOW())"), onupdate=datetime.utcnow),
]


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    surname: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(length=20), nullable=True)
    tg_chat_id: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    role: Mapped[str] = mapped_column(
        Enum("admin", "master", "client", name="user_role"),
        nullable=False, default="client",
    )
    email: Mapped[str | None] = mapped_column(
        String(length=320), unique=True, nullable=True,
    )
    created: Mapped[created_at]
    updated: Mapped[updated_at]

    shifts: Mapped[list['ShiftDay']] = relationship(back_populates='master')
    vehicles: Mapped[list['Vehicle']] = relationship(back_populates='vehicle_owner')

    def __repr__(self):
        return f"<User (id={self.id}, username={self.username})>"


class ShiftDay(Base):
    __tablename__ = 'shift'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003
    date: Mapped[date] = mapped_column(Date(), nullable=False)
    time_start: Mapped[time] = mapped_column(Time(), nullable=False)
    time_end: Mapped[time] = mapped_column(Time(), nullable=False)
    created: Mapped[created_at]
    updated: Mapped[updated_at]

    master_id: Mapped[UUID_ID] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    master: Mapped[User] = relationship(back_populates='shifts', innerjoin=True)

    def __repr__(self):
        return f"<ShiftDay (id={self.id}, date={self.date})>"


class Vehicle(Base):
    __tablename__ = 'vehicle'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    license_plate: Mapped[str] = mapped_column(String(length=10), nullable=True)
    category: Mapped[str] = mapped_column(
        Enum("car", "truck", "bus", "motorcycle", "other", name="vehicle_category"),
        nullable=False, default="car",
    )
    VIN: Mapped[str] = mapped_column(String(length=17), nullable=True, unique=True)
    created: Mapped[created_at]
    updated: Mapped[updated_at]

    client_id: Mapped[UUID_ID] = mapped_column(ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
    vehicle_owner: Mapped[User] = relationship(back_populates='vehicles')

    orders: Mapped[list['Order']] = relationship(back_populates='vehicle')

    def __repr__(self):
        return f"<Vehicle (id={self.id}, license_plate={self.license_plate})>"


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003
    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    price: Mapped[int] = mapped_column(Integer(), nullable=True)
    date: Mapped[date] = mapped_column(Date(), nullable=False)
    time_start: Mapped[time] = mapped_column(Time(), nullable=False)
    time_end: Mapped[time] = mapped_column(Time(), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("open", "done", "canceled", name="order_status"),
        nullable=False, default="open",
    )
    created: Mapped[created_at]
    updated: Mapped[updated_at]

    master_id: Mapped[UUID_ID] = mapped_column(ForeignKey('user.id', ondelete="SET NULL"), nullable=True)

    vehicle_id: Mapped[UUID_ID] = mapped_column(ForeignKey('vehicle.id', ondelete="CASCADE"))
    vehicle: Mapped[Vehicle] = relationship(back_populates='orders')

    client_id: Mapped[UUID_ID] = mapped_column(ForeignKey('user.id', ondelete="SET NULL"), nullable=True)

    def __repr__(self):
        return f"<Order (id={self.id}, title={self.title}, status={self.status})>"
