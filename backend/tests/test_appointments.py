from datetime import datetime, timedelta

from fastapi import status


def test_create_appointment(client, whatsapp_dummy):
    """Persist a new appointment and verify the confirmation message is queued."""

    payload = {
        "user_name": "Alice",
        "phone_number": "whatsapp:+15555555555",
        "reason": "Consultation",
        "appointment_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
    }

    response = client.post("/appointments/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["user_name"] == "Alice"
    assert len(whatsapp_dummy.messages) == 1


def test_prevent_past_appointment(client):
    """Reject appointments that are scheduled in the past."""

    payload = {
        "user_name": "Bob",
        "phone_number": "whatsapp:+15555555555",
        "reason": "Follow-up",
        "appointment_time": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
    }

    response = client.post("/appointments/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_double_booking_not_allowed(client):
    """Ensure a second request for the same time slot fails."""

    appointment_time = (datetime.utcnow() + timedelta(hours=3)).isoformat()
    payload = {
        "user_name": "Carol",
        "phone_number": "whatsapp:+1000000000",
        "reason": "Checkup",
        "appointment_time": appointment_time,
    }

    first = client.post("/appointments/", json=payload)
    assert first.status_code == status.HTTP_201_CREATED

    second = client.post("/appointments/", json=payload)
    assert second.status_code == status.HTTP_409_CONFLICT


def test_cancel_appointment(client, whatsapp_dummy):
    """Cancel an appointment and send a WhatsApp notification."""

    appointment_time = (datetime.utcnow() + timedelta(hours=4)).isoformat()
    payload = {
        "user_name": "Dave",
        "phone_number": "whatsapp:+12223334444",
        "reason": "Therapy",
        "appointment_time": appointment_time,
    }

    response = client.post("/appointments/", json=payload)
    appointment_id = response.json()["id"]

    cancel_response = client.delete(f"/appointments/{appointment_id}")
    assert cancel_response.status_code == status.HTTP_204_NO_CONTENT
    assert len(whatsapp_dummy.messages) == 2


def test_list_appointments(client):
    """Return a list response when requesting all future appointments."""

    response = client.get("/appointments/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_prevent_duplicate_cancel(client):
    """Avoid double cancellation and respond with a conflict."""

    appointment_time = (datetime.utcnow() + timedelta(hours=5)).isoformat()
    payload = {
        "user_name": "Eve",
        "phone_number": "whatsapp:+14445556666",
        "reason": "Consult",
        "appointment_time": appointment_time,
    }

    response = client.post("/appointments/", json=payload)
    appointment_id = response.json()["id"]

    first_cancel = client.delete(f"/appointments/{appointment_id}")
    assert first_cancel.status_code == status.HTTP_204_NO_CONTENT

    second_cancel = client.delete(f"/appointments/{appointment_id}")
    assert second_cancel.status_code == status.HTTP_409_CONFLICT

