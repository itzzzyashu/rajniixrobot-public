__all__ = ['get_collection']

import asyncio
from RajniiRobot import LOGGER, MONGO_DB_URL, BOT_NAME
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection

LOGGER.debug("Connecting to Database ...")

_MGCLIENT: AgnosticClient = AsyncIOMotorClient(MONGO_DB_URL)
_RUN = asyncio.get_event_loop().run_until_complete

if f"{BOT_NAME}" in _RUN(_MGCLIENT.list_database_names()):
    LOGGER.debug(f"[{BOT_NAME}] Anime  Database Found :) => Now Logging to it...")
else:
    LOGGER.debug(f"[{BOT_NAME}] Anime Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT[f"{BOT_NAME}"]


def get_collection(name: str) -> AgnosticCollection:
    """ Create or Get Collection from your database """
    return _DATABASE[name]


def _close_db() -> None:
    _MGCLIENT.close()