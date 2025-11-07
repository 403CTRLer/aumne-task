from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import select, Session

from .models import (
    Appointment,
    AppointmentCreate,
    AppointmentRead,
    AppointmentStatus,
)


def _raise_conflict() -> None:
    """Raise a HTTP 409 error when two appointments collide."""

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Another confirmed appointment exists at the requested time.",
    )


def create_appointment(session: Session, payload: AppointmentCreate) -> Appointment:
    """Persist a new appointment after validating business rules."""

    appointment_time = payload.appointment_time
    if appointment_time < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment time must be in the future.",
        )

    statement = select(Appointment).where(
        Appointment.appointment_time == appointment_time,
        Appointment.status == AppointmentStatus.CONFIRMED,
    )
    if session.exec(statement).first():
        _raise_conflict()

    db_obj = Appointment(**payload.model_dump())
    session.add(db_obj)
    session.flush()
    session.refresh(db_obj)
    return db_obj


def list_appointments(session: Session) -> Sequence[Appointment]:
    """Return upcoming appointments sorted by their scheduled time."""

    statement = select(Appointment).where(
        Appointment.appointment_time >= datetime.utcnow()
    ).order_by(Appointment.appointment_time)
    return session.exec(statement).all()


def get_appointment(session: Session, appointment_id: int) -> Appointment:
    """Fetch a single appointment or raise a 404 if it is missing."""

    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment


def cancel_appointment(session: Session, appointment_id: int) -> Appointment:
    """Cancel a booked appointment and prevent double cancellations."""

    appointment = get_appointment(session, appointment_id)
    if appointment.status == AppointmentStatus.CANCELED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Appointment is already canceled.",
        )

    appointment.status = AppointmentStatus.CANCELED
    appointment.updated_at = datetime.utcnow()
    session.add(appointment)
    session.flush()
    session.refresh(appointment)
    return appointment


def mark_reminder_sent(session: Session, appointment: Appointment) -> Appointment:
    """Flag an appointment as reminded after a successful WhatsApp push."""

    appointment.reminder_sent = True
    appointment.updated_at = datetime.utcnow()
    session.add(appointment)
    session.flush()
    session.refresh(appointment)
    return appointment

