import os
from dotenv import load_dotenv

# Load variables from the .env file if present
load_dotenv(".env.local")

def get_user_list(config_key, default=""):
    """Helper to parse comma-separated environment variables into a list of integers."""
    val = os.getenv(config_key, default)
    if not val:
        return []
    return [int(x.strip()) for x in val.split(",") if x.strip().isdigit()]

class Config(object):
    """This Config class that contains all config values that are required to run your bot.\n
    This config.py file will help you to host your bot from command line interface or local hosting.\n
    You need to fill all required values correctly.\n
    =========================================================\n
    Requirements you need to host from a cli are:
    - Command Line Interface(VPS)
    - Browser
    - Any IDE for further development, Microsoft Visual Studio Code is Recommended.
    - Should know python basics
    - Should know about telegram APIs
    - A device to save all the files for backup.
    
    Now edit the config.py file as it wants, Read the comments for perfect guide to get all necessary values.\n
    Please read the manual for more information.\n
    You can also get deploying tutorials there. [[Read Manual](https://www.itzzzyashu-cf.tk/projects#rajniiroboactive)].\n
    =========================================================\n
    This Class is seperated in six sections:
    - `Required [V-PTB]` for your Values related to your Python Telegram Bot.
    - `Required [C/S-U/I]` for required Channel and Support - Usernames/IDs.
    - `Required [V-SU]` for required Values of Support Users.
    - `Required [V-D/C]` for required Values related to Database and Cloud.
    - `Required [V-IAK]` for required Values related to IDs, APIs and KEYs.
    - `Required [V-P/D]` for required Values related to Paths and Directories.
    + Values with '+' in comments are Important for bot to run.

    =========================================================\n
    [Team Sanatan Raksha Network™](https://www.github.com/TeamSanatanRakshaNetwork), All rights reserved.\n
    Project [rajniiroboactive](https://www.github.com/TeamSanatanRakshaNetwork/rajniiroboactive) have © Copyright of [@itzzzyashu](https://www.github.com/itzzzyashu).
    
    =========================================================\n
    """
    
    LOGGER = os.getenv("LOGGER", "True").lower() == "true"

    # "Required [V-PTB]"
    TOKEN = os.getenv("TOKEN", "") 
    BOT_NAME = os.getenv("BOT_NAME", "") 
    BOT_ID = int(os.getenv("BOT_ID", "0")) 
    BOT_USERNAME = os.getenv("BOT_USERNAME", "") 
    BOT_START_PIC = os.getenv("BOT_START_PIC", "") 
    BOT_START_GIF = os.getenv("BOT_START_GIF", "") 
    SOURCE_CODE = [
        os.getenv("SOURCE_CODE_PLATFORM", "Github"),
        os.getenv("SOURCE_CODE_URL", "http://github.com"),
        os.getenv("SOURCE_CODE_OWNER", "MysticalIllusion"),
        os.getenv("SOURCE_CODE_REPO", "rajniixrobot")
    ]
    INFOPIC = os.getenv("INFOPIC", "True").lower() == "true" 
    STRICT_GMUTE = os.getenv("STRICT_GMUTE", "True").lower() == "true" 
    STRICT_GBAN = os.getenv("STRICT_GBAN", "True").lower() == "true" 
    ALLOW_EXCL = os.getenv("ALLOW_EXCL", "True").lower() == "true" 
    ALLOW_CHATS = os.getenv("ALLOW_CHATS", "True").lower() == "true" 
    DEL_CMDS = os.getenv("DEL_CMDS", "True").lower() == "true" 
    DONATION_LINK = os.getenv("DONATION_LINK", "") 
    BAN_STICKER = os.getenv("BAN_STICKER", "x") 
    LOAD = os.getenv("LOAD", "").split()
    NO_LOAD = os.getenv("NO_LOAD", "").split()
    
    # "Required [C/S-U/I]"
    SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "") 
    UPDATES_LOGS = os.getenv("UPDATES_LOGS", "") 
    JOIN_LOGGER = os.getenv("JOIN_LOGGER", "-1003950589619") 
    ERROR_LOGS = os.getenv("ERROR_LOGS", "") 
    GLOBAL_LOGS = os.getenv("GLOBAL_LOGS", "") 
    SPAMWATCH_SUPPORT_CHAT = os.getenv("SPAMWATCH_SUPPORT_CHAT", "SPAMWATCHSUPPORT") 
    BL_CHATS = os.getenv("BL_CHATS", "") 

    # "Required [V-SU]"
    OWNER_ID = int(os.getenv("OWNER_ID", "6226195038")) 
    OWNER_USERNAME = os.getenv("OWNER_USERNAME", "xoizzu") 
    DEV_USERS = get_user_list("DEV_USERS", "6226195038,6226195038") 
    SUDO_USERS = get_user_list("SUDO_USERS", "6226195038") 
    SUPPORT_USERS = get_user_list("SUPPORT_USERS", "") 
    TIGER_USERS = get_user_list("TIGER_USERS", "") 
    WHITELIST_USERS = get_user_list("WHITELIST_USERS", "") 

    # "Required - [V-D/C]"
    WORKERS = int(os.getenv("WORKERS", "8")) 
    SQL_DATABASE = os.getenv("SQL_DATABASE", "") 
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    REDIS_ENDPOINT = os.getenv("REDIS_ENDPOINT", "")
    HEROKU_DEPLOY = os.getenv("HEROKU_DEPLOY", "False").lower() == "true"
    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "") 
    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "") 
    URL = os.getenv("URL") or (f"https://{HEROKU_APP_NAME}.herokuapp.com/" if HEROKU_APP_NAME else "") 
    WEBHOOK = os.getenv("WEBHOOK", "") 
    MONGO_DB = os.getenv("MONGO_DB", "rajniixrobot") 
    MONGO_PORT = int(os.getenv("MONGO_PORT", "27018")) 
    MONGO_DB_URL = os.getenv("MONGO_DB_URL", "") 
    ARQ_API_URL = os.getenv("ARQ_API_URL", "http://arq.hamker.dev") 
    BACKUP_PASS = os.getenv("BACKUP_PASS", "")

    # "Required [V-IAK]"
    API_ID = int(os.getenv("API_ID", "0")) 
    API_HASH = os.getenv("API_HASH", "") 
    OPENWEATHERMAP_ID = os.getenv("OPENWEATHERMAP_ID", "")  
    REM_BG_API_KEY = os.getenv("REM_BG_API_KEY", "") 
    TELEGRAPH_ACCESS_TOKEN = os.getenv("TELEGRAPH_ACCESS_TOKEN", "") 
    CASH_API_KEY = os.getenv("CASH_API_KEY", "") 
    TIME_API_KEY = os.getenv("TIME_API_KEY", "") 
    AI_API_URL = os.getenv("AI_API_URL", "https://blue-api.vercel.app/chatbot1")
    AI_API_KEY = os.getenv("AI_API_KEY", "") 
    STRING_SESSION = os.getenv("STRING_SESSION", "") 
    ARQ_API_KEY = os.getenv("ARQ_API_KEY", "") 
    WALL_API = os.getenv("WALL_API", "") 
    SPAMWATCH_API = os.getenv("SPAMWATCH_API", "") 

    # "Required [V-P/D]"
    TEMP_DOWNLOAD_DIRECTORY = os.getenv("TEMP_DOWNLOAD_DIRECTORY", "./") 
    CERT_PATH = os.getenv("CERT_PATH", "CERT_PATH") 
    GOOGLE_CHROME_BIN = os.getenv("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome") 
    CHROME_DRIVER = os.getenv("CHROME_DRIVER", "/usr/bin/chromedriver") 
    PORT = int(os.getenv("PORT", "5000")) 

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True