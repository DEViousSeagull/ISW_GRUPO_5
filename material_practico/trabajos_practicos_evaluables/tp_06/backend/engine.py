from sqlalchemy import create_engine, event
from pathlib import Path

# Absolute path to avoid “different cwd” issues with uvicorn reload
DB_PATH = Path(__file__).resolve().parent / "tickets.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite + FastAPI
)

@event.listens_for(engine, "connect")
def _fk_on(dbapi_conn, _):
    dbapi_conn.execute("PRAGMA foreign_keys = ON")