from typing import Generator

from fastapi import Depends
from sqlmodel import Session

from .database import get_session


def session_dependency() -> Generator[Session, None, None]:
    """Yield a database session for the duration of the request."""

    with get_session() as session:
        yield session


def get_db(session: Session = Depends(session_dependency)) -> Session:
    """Expose the database session to FastAPI routes."""

    return session

