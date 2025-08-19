import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

def _get_secret_url() -> str | None:
    # Read Streamlit Cloud secret if running in Streamlit
    try:
        import streamlit as st  # lazy import so local runs don't require streamlit at import time
        return st.secrets.get("database_url")
    except Exception:
        return None

def get_engine() -> Engine:
    """
    Return a SQLAlchemy Engine.

    Order of precedence for DB URL:
    1) .env file: DATABASE_URL
    2) Streamlit secrets: database_url
    3) Default local SQLite file: sqlite:///local.db
    """
    load_dotenv()
    db_url = os.getenv("DATABASE_URL") or _get_secret_url() or "sqlite:///local.db"

    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    engine = create_engine(db_url, pool_pre_ping=True, connect_args=connect_args)

    # Optional: ensure empty schema exists so Streamlit can render even before seeding
    try:
        from src.models import Base
        with engine.begin():
            Base.metadata.create_all(engine)
    except Exception:
        # If models aren't importable yet, we let the seeder create the schema later.
        pass

    return engine
