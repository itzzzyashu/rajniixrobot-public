"""
This __init__.py file takes input from config.py file and changes variables.
It also creates other different instances which are needed by bot to run all modules correctly.

=========================================================\n

© [TeamUltraUnion/rajniixrobot](https://www.github.com/TeamUltraUnion) \n
© [itzzzyashu/rajniixrobot](https://www.github.com/itzzzyashu/rajniixrobot) \n
© [AnimeKaizoku/SaitamaRobot](https://www.github.com/AnimeKaizoku/SaitamaRobot) \n
© [PaulSonOfLars/tgbot](https://www.github.com/PaulSonOfLars/tgbot) \n
All rights reserved.

=========================================================\n
"""

import json
import logging
import traceback
import os
import sys
import time

import telegram.ext as tg
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from telegram import Chat
from telegram.request import HTTPXRequest
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.sessions import StringSession
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from pymongo import MongoClient
from redis import StrictRedis
from Python_ARQ import ARQ
from aiohttp import ClientSession
from telegram.ext import Application, Defaults
from telegraph import Telegraph
from httpx import AsyncClient, Timeout

__version__ = "7.0"

StartTime = time.time()

def get_user_list(__init__, key):
    with open(f"{os.getcwd()}/RajniiRobot/{__init__}", "r") as json_file:
        return json.load(json_file)[key]


# enable logging
logging.basicConfig(
    format='%(asctime)s • %(name)s | %(levelname)s : %(message)s',
    handlers=[
        logging.FileHandler('log.txt'),
        logging.StreamHandler()
    ],
    level=logging.INFO)


LOGGER = logging.getLogger(__name__)
# logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)



# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 9:
    LOGGER.error("You MUST have a python version of at least 3.9! Multiple features depend on this. Quitting Deployment.",)
    sys.exit(1)


ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get("TOKEN")

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID"))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME")

    try:
        SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = {
            int(x)
            for x in os.environ.get("SUPPORT_USERS", "").split()
        }
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = {
            int(x)
            for x in os.environ.get("WHITELIST_USERS", "").split()
        }
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = {
            int(x)
            for x in os.environ.get("TIGER_USERS", "").split()
        }
    except ValueError:
        raise Exception("Your scout users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", False))  # Info Pic (use True[Value] If You Want To Show In /info.)
    GLOBAL_LOGS = os.environ.get("GLOBAL_LOGS")  # G-Ban Logs (Channel) (-100)
    ERROR_LOGS = os.environ.get("ERROR_LOGS")  # Error Logs (Channel Ya Group Choice Is Yours) (-100)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # If You Deploy On Heraku. [URL PERTEN:- https://{App Name}.herokuapp.com/ || EXP:- https://yuki-cutiepii-robot.herokuapp.com/]
    PORT = int(os.environ.get("PORT", 8443))
    CUSTOM_CMD = os.environ.get("CUSTOM_CMD", False)
    API_ID = os.environ.get("API_ID")  # Bot Owner's API_ID (From:- https://my.telegram.org/auth)
    API_HASH = os.environ.get("API_HASH")  # Bot Owner's API_HASH (From:- https://my.telegram.org/auth)
    DATABASE_URL = os.environ.get("DATABASE_URL")  # Any SQL Database Link (RECOMMENDED:- PostgreSQL & https://www.elephantsql.com)
    DONATION_LINK = os.environ.get("DONATION_LINK")  # Donation Link (ANY)
    LOAD = os.environ.get("LOAD", "").split()  # Don't Change
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()  # Don't Change
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))  # Don't Change
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN",False))  # Use `True` Value
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")  # Don't Change
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)  # Don't Change
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")  # Don't Change
    CASH_API_KEY = os.environ.get("CASH_API_KEY")  # From:- https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = os.environ.get("TIME_API_KEY")  # From:- https://timezonedb.com/api
    WALL_API = os.environ.get("WALL_API")  # From:- https://wall.alphacoders.com/api.php
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY")  # From:- https://www.remove.bg/
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "")  # From:- https://openweathermap.org/api
    GENIUS_API_TOKEN = os.environ.get("GENIUS_API_TOKEN")  # From:- http://genius.com/api-clients
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL")  # MongoDB URL (From:- https://www.mongodb.com/)
    REDIS_URL = os.environ.get("REDIS_URL")  # REDIS URL (Take it from redislabs.com and the format should be redis://username:password@publicendpoint:port/)
    UPDATES_LOGS = os.environ.get("UPDATES_LOGS") #Updates Channel Username
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT")  # Support Chat Username (don't add @)
    STRING_SESSION = os.environ.get("STRING_SESSION")  # Telethon Based String Session (2nd ID) [ From https://repl.it/@SpEcHiDe/GenerateStringSession ]
    APP_ID = os.environ.get("APP_ID")  # 2nd ID
    APP_HASH = os.environ.get("APP_HASH")  # 2nd 
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)  # Don't Change
    DATABASE_NAME = os.environ.get("DATABASE_NAME", True)  # needed for cron_jobs module, use same databasename from SQLALCHEMY_DATABASE_URI
    BACKUP_PASS = os.environ.get("BACKUP_PASS", True)  # The password used for the cron backups zip
    MONGO_DB = "Cutiepii"
    BOT_API_FILE_URL = "https://api.telegram.org/file/bot"
    BOT_API_URL = "https://api.telegram.org/bot"
    BOT_ID = int(TOKEN.split(":")[0])
    HELP_IMG = os.environ.get("HELP_IMG", True)
    GROUP_START_IMG = os.environ.get("GROUP_START_IMG", True)

    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
    from .config import Config
    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    try:
        REMINDER_LIMIT = int(os.environ.get("REMINDER_LIMIT", 20))
    except ValueError:
        raise Exception("Your REMINDER_LIMIT env variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        SUDO_USERS = {int(x) for x in Config.SUDO_USERS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = {int(x) for x in Config.SUPPORT_USERS or []}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = {int(x) for x in Config.WHITELIST_USERS or []}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = {int(x) for x in Config.TIGER_USERS or []}
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    AI_API_URL = Config.AI_API_URL
    AI_API_KEY = Config.AI_API_KEY
    INFOPIC = Config.INFOPIC
    BOT_NAME = Config.BOT_NAME
    BOT_ID = Config.BOT_ID
    BOT_USERNAME = Config.BOT_USERNAME
    BOT_START_GIF = Config.BOT_START_GIF
    BOT_START_PIC = Config.BOT_START_PIC
    SOURCE_CODE = Config.SOURCE_CODE
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    SQL_DATABASE = Config.SQL_DATABASE
    DONATION_LINK = Config.DONATION_LINK
    STRICT_GBAN = Config.STRICT_GBAN
    BAN_STICKER = Config.BAN_STICKER
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    ARQ_API_URL = Config.ARQ_API_URL
    ARQ_API_KEY= Config.ARQ_API_KEY
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    REDIS_ENDPOINT = Config.REDIS_ENDPOINT
    REDIS_PASSWORD = Config.REDIS_PASSWORD
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    UPDATES_LOGS = Config.UPDATES_LOGS
    ERROR_LOGS = Config.ERROR_LOGS
    GLOBAL_LOGS = Config.GLOBAL_LOGS
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    STRING_SESSION = Config.STRING_SESSION
    ALLOW_EXCL = Config.ALLOW_EXCL
    DEL_CMDS = Config.DEL_CMDS
    MONGO_DB = Config.MONGO_DB
    MONGO_DB_URL = Config.MONGO_DB_URL


    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

# Credits Logger
LOGGER.info(f"[{BOT_NAME}] | Activating TUU • Project #C437 | Licensed Under GPLv3.")
LOGGER.info(f"[{BOT_NAME}] | [ACTIVATING #C437]: Initializing Required Clients")
LOGGER.info(f"""[{BOT_NAME}] | Project Maintained By:
• [github.com/TeamUltraUnion]
• (telegram.me/TeamUnixSystem)
\n""")

telegraph = Telegraph()
ACCESS_TOKEN = os.getenv("TELEGRAPH_ACCESS_TOKEN")

if ACCESS_TOKEN:
    telegraph.token = ACCESS_TOKEN
else:
    try:
        account = telegraph.create_account(short_name="rajniixrobot")
        ACCESS_TOKEN = account["access_token"]
        LOGGER.info(f"[{BOT_NAME}] | Telegraph account created.")
    except Exception as e:
        LOGGER.error(
            f"[{BOT_NAME}] | Telegraph account init failed\nError: {e}\n{traceback.format_exc()}"
        )

# Initializing Telethon Client 
try:
    telethn = TelegramClient(StringSession(), API_ID, API_HASH)
    LOGGER.info(f"[{BOT_NAME}] | Initialized Telethon Client.")
except Exception as e:
    LOGGER.error(f"[{BOT_NAME}] | Initializing Telethon Client Failed\nError: {e}\n{traceback.format_exc()}")

# Initializing Pyrogram Client 
try:
    PyroGram = TOKEN.split(":")[0]
    pgram = Client(
        name=PyroGram,
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=TOKEN,
        workers=min(32, os.cpu_count() + 4),
        parse_mode=ParseMode.DEFAULT, 
        sleep_threshold=180,  
        in_memory=True
    )
    LOGGER.info(f"[{BOT_NAME}] | Initialized Pyrogram Client.")
except Exception as e:
    LOGGER.error(f"[{BOT_NAME}] | Initializing Pyrogram Client Failed\nError: {e}\n{traceback.format_exc()}")

# Initializing RAJNII_PTB
try:
    defaults = Defaults(block=False)
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )
    RAJNI_PTB = (
        Application.builder()
        .token(TOKEN)
        .request(request)
        .defaults(defaults)
        .concurrent_updates(True)
        .build()
    )
    LOGGER.info(f"[{BOT_NAME}] | Initialized Telegram Bot Client.")
except Exception as e:
    LOGGER.error(
        f"[{BOT_NAME}] | Failed to initialize Telegram Bot Client.\n"
        f"Error: {e}\n{traceback.format_exc()}"
    )
    sys.exit(1)

# Global Network Session Variables Placeholders
aiohttpsession = None  
arq = None 
http = None # ✅ Placeholder for the global HTTPX client

# Initialize aiohttp session (must be async)
async def init_aiohttp_session():
    global aiohttpsession
    try:
        aiohttpsession = ClientSession()
        LOGGER.info(f"[{BOT_NAME}] | Initialized aiohttp session.")
        status = {"status": True, "aiohttpsession": aiohttpsession}
        return status
    except Exception as e:
        LOGGER.error(f"[{BOT_NAME}] | Could not initialize aiohttp session. Error: {e}")
        status = {"status": False}
        return status

# Close aiohttp session
async def close_aiohttp_session():
    global aiohttpsession
    if aiohttpsession:
        try:
            await aiohttpsession.close()
            LOGGER.info(f"[{BOT_NAME}] | Aiohttp session closed.")
            status = {"status": True}
        except Exception as e:
            LOGGER.error(f"[{BOT_NAME}] | Error closing aiohttp session: {e}")
            status = {"status": False}
    else:
        LOGGER.warning(f"[{BOT_NAME}] | No aiohttp session to close.")
        status = {"status": True}  
    return status

# ✅ FIX: Initialize HTTPX Client Cleanly inside the loop setup phase
async def init_http_client():
    global http
    try:
        timeout = Timeout(20) # Safely keeps timeouts under PTB's 30s connection limits
        http = AsyncClient(http2=True, timeout=timeout)
        LOGGER.info(f"[{BOT_NAME}] | Initialized global HTTPX AsyncClient cleanly inside active loop context.")
        return True
    except Exception as e:
        LOGGER.error(f"[{BOT_NAME}] | Initializing HTTPX Client Failed\nError: {e}\n{traceback.format_exc()}")
        return False

# ✅ FIX: Clear HTTPX closure function mapped for the termination handler
async def close_http_client():
    global http
    if http:
        try:
            await http.aclose()
            LOGGER.info(f"[{BOT_NAME}] | Global HTTPX AsyncClient closed cleanly.")
        except Exception as e:
            LOGGER.error(f"[{BOT_NAME}] | Error closing HTTPX Client: {e}")

# Initialize ARQ client
async def init_arq_client(session):
    global arq  
    if session is not None:
        try:
            arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)
            LOGGER.info(f"[{BOT_NAME}] | ARQ Client initialized successfully.")
        except Exception as e:
            LOGGER.error(f"[{BOT_NAME}] | Failed to initialize ARQ Client\nError: {e}\n{traceback.format_exc()}")
            sys.exit(1)  
    else:
        raise RuntimeError("aiohttp session must be initialized first.")

# Initializing Telethon Userbot Client
try:
    ubot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    LOGGER.info(f"[{BOT_NAME}] | Connected to {BOT_NAME}\'s Userbot. (telegram.me/iKeshavVirmani)")
except Exception as e:
    LOGGER.error(f"[{BOT_NAME}] | Connection to {BOT_NAME}\'s Userbot Failed. (telegram.me/iKeshavVirmani)\nError: {e}\n{traceback.format_exc()}")

# Connecting to MongoDB Database 
try:
    mongodb = MongoClient(MONGO_DB_URL, 27017)[MONGO_DB]
    motor = AsyncIOMotorClient(MONGO_DB_URL)
    db = motor[MONGO_DB]
    engine = AIOEngine(motor, MONGO_DB)
    LOGGER.info(f"[{BOT_NAME}] | Connected to Database • Asia/Mumbai • MongoDB Database (NOSQL)")
except Exception as e:
    LOGGER.error(f"[{BOT_NAME}] | Connection to Database • Asia/Mumbai • MongoDB Database (NOSQL)\nError: {e}\n{traceback.format_exc()}")

REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_ENDPOINT}"
REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
try:
    REDIS.ping()
    LOGGER.info(f"[{BOT_NAME}] | Connected to Database • Data Center • Asia/Mumbai • Redis Database")
except Exception as e:
    LOGGER.error(f"[{BOT_NAME}] | Connection to Database Failed • Data Center • Asia/Mumbai • Redis Database\nError: {e}\n{traceback.format_exc()}")
finally:
    REDIS.ping()
    LOGGER.info(f"[{BOT_NAME}] | Connected To Database • Data Center • Asia/Mumbai • Redis Database")

LOGGER.info(f"""\n
=======================================================
[{BOT_NAME}] | TUU | Initialization Completed
[{BOT_NAME}] | TUU | Visit @{UPDATES_LOGS} for Updates!!
=======================================================\n\n\n""")

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_users(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client

apps = [pgram]
SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
TIGER_USERS = list(TIGER_USERS)
ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "RajniiRobot/elevated_users.json")

# Load at end to ensure all prev variables have been set
from RajniiRobot.modules.helper_funcs.handlers import CustomCommandHandler

CustomCommandHandler.has_args = True
# make sure the regex handler can take extra kwargs safely via the new async engine
tg.CommandHandler = CustomCommandHandler