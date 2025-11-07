from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from .. import crud
from ..dependencies import get_db
from ..models import AppointmentCreate, AppointmentRead
from ..services.whatsapp import WhatsAppSender, get_whatsapp_client


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    session: Session = Depends(get_db),
    whatsapp_client: WhatsAppSender = Depends(get_whatsapp_client),
):
    """Create a new appointment and notify the attendee via WhatsApp."""

    appointment = crud.create_appointment(session, payload)

    confirmation_message = (
        f"Hi {appointment.user_name}, your appointment is confirmed for "
        f"{appointment.appointment_time.isoformat()} for {appointment.reason}."
    )
    whatsapp_client.send_message(appointment.phone_number, confirmation_message)
    return AppointmentRead.model_validate(appointment)


@router.get("/", response_model=list[AppointmentRead])
def list_appointments(session: Session = Depends(get_db)):
    """Return all scheduled appointments that have not yet expired."""

    appointments = crud.list_appointments(session)
    return [AppointmentRead.model_validate(item) for item in appointments]


@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(
    appointment_id: int,
    session: Session = Depends(get_db),
):
    """Retrieve an appointment by identifier."""

    appointment = crud.get_appointment(session, appointment_id)
    return AppointmentRead.model_validate(appointment)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(
    appointment_id: int,
    session: Session = Depends(get_db),
    whatsapp_client: WhatsAppSender = Depends(get_whatsapp_client),
):
    """Cancel a scheduled appointment and inform the attendee."""

    appointment = crud.cancel_appointment(session, appointment_id)
    cancellation_message = (
        f"Hi {appointment.user_name}, your appointment on "
        f"{appointment.appointment_time.isoformat()} has been canceled."
    )
    whatsapp_client.send_message(appointment.phone_number, cancellation_message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

