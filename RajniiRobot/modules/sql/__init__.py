import sys
from RajniiRobot import SQL_DATABASE, LOGGER, BOT_NAME
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


def start() -> scoped_session:
    # ✅ FIX: Added pool recovery params to prevent stale SSL handshake timeouts
    engine = create_engine(
        SQL_DATABASE, 
        client_encoding="utf8",
        pool_pre_ping=True,       # Verifies connection viability before running queries
        pool_recycle=300,         # Recycle connections every 5 minutes
        pool_size=10,             # Keep baseline pool size controlled
        max_overflow=20           # Allow temporary burst overhead allocations
    )
    LOGGER.info(f"[{BOT_NAME}] | Postgre SQL Connecting to database with Pre-Ping validation pools...")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=True))


BASE = declarative_base()
try:
    SESSION: scoped_session = start()
except Exception as e:
    LOGGER.exception(f"[{BOT_NAME}] | PostgreSQL Failed to connect due to {e}")
    sys.exit()

LOGGER.info(f"[{BOT_NAME}] | PostgreSQL Connection successful, session started.")