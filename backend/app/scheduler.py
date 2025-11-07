import logging
from datetime import datetime, timedelta
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlmodel import select

from .config import get_settings
from .database import get_session
from .models import Appointment, AppointmentStatus
from .services.whatsapp import get_whatsapp_client
from . import crud


scheduler: Optional[AsyncIOScheduler] = None
logger = logging.getLogger("scheduler")


def _send_reminders() -> None:
    """Look for upcoming appointments and push WhatsApp reminders."""

    settings = get_settings()
    now = datetime.utcnow()
    window_end = now + timedelta(minutes=settings.reminder_lead_minutes)

    with get_session() as session:
        statement = (
            select(Appointment)
            .where(Appointment.status == AppointmentStatus.CONFIRMED)
            .where(Appointment.reminder_sent.is_(False))
            .where(Appointment.appointment_time >= now)
            .where(Appointment.appointment_time <= window_end)
        )
        appointments = session.exec(statement).all()

        if not appointments:
            return

        whatsapp_client = get_whatsapp_client()

        for appointment in appointments:
            try:
                reminder_message = (
                    f"Reminder: Hi {appointment.user_name}, you have an appointment at "
                    f"{appointment.appointment_time.isoformat()} for {appointment.reason}."
                )
                whatsapp_client.send_message(appointment.phone_number, reminder_message)
                crud.mark_reminder_sent(session, appointment)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.exception("Failed to send reminder for appointment %s: %s", appointment.id, exc)


def start_scheduler() -> None:
    """Boot the scheduler if it is not already running."""

    global scheduler

    if scheduler and scheduler.running:
        return

    scheduler = AsyncIOScheduler()
    settings = get_settings()
    scheduler.add_job(
        _send_reminders,
        trigger=IntervalTrigger(minutes=settings.reminder_check_interval_minutes),
        id="appointment_reminder_job",
        replace_existing=True,
    )
    scheduler.start()


def shutdown_scheduler() -> None:
    """Stop the scheduler when the application shuts down."""

    if scheduler and scheduler.running:
        scheduler.shutdown()

