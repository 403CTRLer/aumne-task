from datetime import datetime
from enum import Enum

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class AppointmentStatus(str, Enum):
    """Track the lifecycle of an appointment."""

    CONFIRMED = "confirmed"
    CANCELED = "canceled"


class Appointment(SQLModel, table=True):
    """Persisted appointment record."""

    id: int | None = Field(default=None, primary_key=True)
    user_name: str
    phone_number: str
    reason: str
    appointment_time: datetime
    status: AppointmentStatus = Field(default=AppointmentStatus.CONFIRMED)
    reminder_sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AppointmentRead(SQLModel):
    """Response model exposed to API consumers."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    user_name: str
    phone_number: str
    reason: str
    appointment_time: datetime
    status: AppointmentStatus
    reminder_sent: bool
    created_at: datetime
    updated_at: datetime


class AppointmentCreate(SQLModel):
    """Payload required to create a new appointment."""

    model_config = ConfigDict(from_attributes=True)
    user_name: str
    phone_number: str
    reason: str
    appointment_time: datetime


class AppointmentUpdate(SQLModel):
    """Internal helper for partial updates."""

    status: AppointmentStatus | None = None
    reminder_sent: bool | None = None

