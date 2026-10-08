import os
from collections.abc import Iterator
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

DEFAULT_DB_PATH = os.getenv("DATABASE_PATH", "./data/app.db")

engine = create_engine(f"sqlite:///{DEFAULT_DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:  # noqa: BLE001
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:  # noqa: BLE001
        session.rollback()
        raise
    finally:
        session.close()


def apply_seed_if_needed() -> None:
    """Insert the demo rows through the ORM when their tables are empty."""
    from .models import ActionItem, Note

    with get_session() as session:
        has_notes = session.execute(select(Note.id).limit(1)).first() is not None
        has_action_items = (
            session.execute(select(ActionItem.id).limit(1)).first() is not None
        )
        if not has_notes:
            session.add_all(
                [
                    Note(
                        title="Welcome",
                        content="This is a starter note. TODO: explore the app!",
                    ),
                    Note(title="Demo", content="Click around and add a note. Ship feature!"),
                ]
            )
        if not has_action_items:
            session.add_all(
                [
                    ActionItem(description="Try pre-commit", completed=False),
                    ActionItem(description="Run tests", completed=False),
                ]
            )


