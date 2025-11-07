"""Sample interactions with the generated Python SDK.

Run the SDK generator first so the `python_client` package is available.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from python_client import ApiClient, Configuration
from python_client.api.appointments_api import AppointmentsApi
from python_client.models.appointment_create import AppointmentCreate


def main() -> None:
    configuration = Configuration(host="http://localhost:8000")
    with ApiClient(configuration) as api_client:
        api = AppointmentsApi(api_client)

        appointment_time = (datetime.utcnow() + timedelta(hours=2)).isoformat()
        payload = AppointmentCreate(
            user_name="SDK Tester",
            phone_number="whatsapp:+15555555555",
            reason="Integration test",
            appointment_time=appointment_time,
        )

        created = api.create_appointment(payload)
        print("Created appointment:", created)

        all_appointments = api.list_appointments()
        print("Appointments:", all_appointments)

        api.cancel_appointment(created.id)
        print("Appointment canceled")


if __name__ == "__main__":
    main()

