import logging
from typing import Protocol

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from ..config import get_settings


class WhatsAppSender(Protocol):
    """Simple interface used by the rest of the codebase."""

    def send_message(self, to_number: str, body: str) -> None:  # pragma: no cover - protocol
        ...


class WhatsAppClient:
    """Thin wrapper over Twilio's WhatsApp API."""

    def __init__(self) -> None:
        settings = get_settings()
        self._client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        self._from_number = settings.whatsapp_from_number

    def send_message(self, to_number: str, body: str) -> None:
        """Forward a WhatsApp message via Twilio."""

        try:
            self._client.messages.create(
                from_=self._from_number,
                to=to_number,
                body=body,
            )
        except TwilioRestException as exc:  # pragma: no cover - network error
            raise RuntimeError(f"Failed to send WhatsApp message: {exc}") from exc


class ConsoleWhatsAppClient:
    """Fallback that logs messages when credentials are missing."""

    def __init__(self) -> None:
        self._logger = logging.getLogger("whatsapp.mock")

    def send_message(self, to_number: str, body: str) -> None:  # pragma: no cover - logging
        self._logger.info("Mock WhatsApp message to %s: %s", to_number, body)


def get_whatsapp_client() -> WhatsAppSender:
    """Return a real WhatsApp client when configured, otherwise log messages."""

    settings = get_settings()
    if (
        settings.twilio_account_sid
        and settings.twilio_auth_token
        and settings.whatsapp_from_number
    ):
        return WhatsAppClient()
    return ConsoleWhatsAppClient()

