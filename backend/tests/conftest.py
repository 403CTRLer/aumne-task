from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.dependencies import get_db
from app.main import create_app
from app.services.whatsapp import WhatsAppSender, get_whatsapp_client


class DummyWhatsAppClient:
    """Record outbound messages so tests can assert on them."""

    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def send_message(self, to_number: str, body: str) -> None:
        self.messages.append((to_number, body))


@pytest.fixture()
def test_engine():
    """Spin up an in-memory SQLite database for each test session."""

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(test_engine) -> Generator[Session, None, None]:
    """Yield a database session bound to the shared in-memory engine."""

    with Session(test_engine) as session:
        yield session


@pytest.fixture()
def whatsapp_dummy() -> DummyWhatsAppClient:
    """Provide a fake WhatsApp client so tests avoid real network calls."""

    return DummyWhatsAppClient()


@pytest.fixture()
def app(db_session: Session, whatsapp_dummy: DummyWhatsAppClient):
    """Create a FastAPI test application with stubbed dependencies."""

    fastapi_app = create_app(enable_scheduler=False, initialize_database=False)

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    def override_whatsapp_client() -> WhatsAppSender:
        return whatsapp_dummy

    fastapi_app.dependency_overrides[get_db] = override_get_db
    fastapi_app.dependency_overrides[get_whatsapp_client] = override_whatsapp_client

    yield fastapi_app

    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def client(app) -> Generator[TestClient, None, None]:
    """Expose a synchronous test client for exercising the API."""

    with TestClient(app) as test_client:
        yield test_client

