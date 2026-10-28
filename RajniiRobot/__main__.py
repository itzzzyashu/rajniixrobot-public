import contextlib
import html
import json
import importlib
import time
import re
import signal
import traceback
import asyncio
import sys
import traceback
from sys import argv
from typing import Optional
from pyrogram import idle as pyrogram_idle
from telethon.errors import FloodWaitError


# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ContextTypes, filters, CallbackQueryHandler, MessageHandler)
from telegram.error import (BadRequest, ChatMigrated, NetworkError, TelegramError, TimedOut, Forbidden)
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode
# ✅ Trick Python into pointing the old name to the new v21 Type
CallbackContext = ContextTypes.DEFAULT_TYPE

from RajniiRobot.modules import ALL_MODULES
import RajniiRobot.modules.sql.users_sql as sql
from RajniiRobot.modules.disable import DisableAbleCommandHandler
from RajniiRobot.modules.helper_funcs.misc import paginate_modules
from RajniiRobot.modules.helper_funcs.chat_status import is_user_admin
from RajniiRobot import (DONATION_LINK, LOGGER, OWNER_ID, OWNER_USERNAME, PORT, TOKEN, URL, WEBHOOK, SUPPORT_CHAT, UPDATES_LOGS, BOT_NAME, BOT_USERNAME, BOT_START_GIF, BOT_START_PIC, ERROR_LOGS, RAJNI_PTB, SOURCE_CODE, StartTime, telethn, pgram, ubot, init_aiohttp_session, init_arq_client, close_aiohttp_session)
from RajniiRobot.strings import (START_GROUP_STRING, HELP_GROUP_STRING, START_SECTION_STRING, ABOUT_SECTION_STRING, DONATE_SECTION_STRING, HELP_SECTION_STRING, MANUAL_SECTION_STRING, ADMIN_SETUP_STRING, ANTISPAM_SETUP_STRING, SUPPORT_SECTION_STRING, CREDITS_SECTION_STRING, TANDC_SECTION_STRING)


# Data Sets
IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}
GDPR = []
FAILED_PLUGINS = []
SUCCESS_PLUGINS = []

# Import Modules
for module_name in ALL_MODULES:
    try:
        # Try importing the module
        imported_module = importlib.import_module(f"RajniiRobot.modules.{module_name}")
        SUCCESS_PLUGINS.append(module_name)
        
        # Set a default mod_name if not already set
        if not hasattr(imported_module, "__mod_name__"):
            imported_module.__mod_name__ = imported_module.__name__

        # Ensure no duplicates of module names
        if imported_module.__mod_name__.lower() not in IMPORTED:
            IMPORTED[imported_module.__mod_name__.lower()] = imported_module
        else:
            raise Exception(f"Can't have two modules with the same name: {module_name}. Please change one.")

        # Add to helpable, migrateable, and other lists if attributes exist
        if hasattr(imported_module, "__help__") and imported_module.__help__:
            HELPABLE[imported_module.__mod_name__.lower()] = imported_module

        if hasattr(imported_module, "__migrate__"):
            MIGRATEABLE.append(imported_module)

        if hasattr(imported_module, "__stats__"):
            STATS.append(imported_module)

        if hasattr(imported_module, "__gdpr__"):
            GDPR.append(imported_module)

        if hasattr(imported_module, "__user_info__"):
            USER_INFO.append(imported_module)

        if hasattr(imported_module, "__import_data__"):
            DATA_IMPORT.append(imported_module)

        if hasattr(imported_module, "__export_data__"):
            DATA_EXPORT.append(imported_module)

        if hasattr(imported_module, "__chat_settings__"):
            CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

        if hasattr(imported_module, "__user_settings__"):
            USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    except Exception as e:
        # Log the error and add the module to the failed list
        FAILED_PLUGINS.append(module_name)
        LOGGER.error(f"Failed to load plugin {module_name}: {e}: {traceback.format_exc()}")

# Log the loaded and failed plugins
LOGGER.info(f"\n\n-------------------------------\nSuccessfully loaded plugins: {SUCCESS_PLUGINS}\n\n")
if FAILED_PLUGINS:
    LOGGER.warning(f"\n\n-------------------------------\nFailed to load plugins: {FAILED_PLUGINS}\n\n")



# Get Readable Time Format
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time



# Debugging handlers
async def test(update: Update):
    # LOGGER.debug(eval(str(update)))
    # await update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    await update.effective_message.reply_text("This person edited a message")
    LOGGER.debug(update.effective_message)



async def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)
    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb = "".join(tb_list)
    # Build the message with some markup and additional information about what happened.
    message = f"An exception was raised while handling an update\n<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}</pre>\n\n<pre>{html.escape(tb)}</pre>"
    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    await context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)



# Error Callback
async def error_callback(_, context: CallbackContext):
    try:
        raise context.error
    except (BadRequest):
        pass
        # remove update.message.chat_id from conversation list
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors



# Start Handler
async def start(update: Update, context: CallbackContext):
    LOGGER.info("ok")
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_SECTION_STRING)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(text="☆ Back", callback_data="help_back"),
                            InlineKeyboardButton(text="☆ Home", callback_data="rajni_back")
                        ]
                    ]),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["extras"].markdown_help_sender(update)
            elif args[0].lower() == "disasters":
                IMPORTED["disasters"].send_disasters(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = await RAJNI_PTB.bot.getChat(match[1])
                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)
            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)
        else:
            await update.effective_message.reply_text(
                START_SECTION_STRING.format(
                    escape_markdown(context.bot.first_name),
                    BOT_START_PIC,
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats()
                ),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False,
                timeout=60,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(text=f"Add {BOT_NAME} to your group", url=f"https://telegram.me/{BOT_USERNAME}?startgroup=true")
                    ],
                    [
                        InlineKeyboardButton(text="☆ About", callback_data="about_section"),
                        InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                    ],
                    [
                        InlineKeyboardButton(text=f"☆ Powered by Unix System ☆", url=f"https://telegram.me/TeamUnixSystem")
                    ]
                ]),
            )
    else:
        await update.effective_message.reply_animation(
            BOT_START_GIF,
            caption=START_GROUP_STRING.format(uptime),
            parse_mode=ParseMode.HTML,
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="➥ Support", url=f"https://telegram.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton(text="➥ Updates", url=f"https://telegram.me/{UPDATES_LOGS}"),
                    InlineKeyboardButton(text="➥ Global", url=f"https://telegram.me/{GLOBAL_LOGS}")
                ],
                [
                    InlineKeyboardButton(text="☆ Unix System ☆", url="https://telegram.me/TeamUnixSystem")
                ]
            ])
        )



# Help Handler
async def send_help(context: CallbackContext, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELPABLE, "help")
        )
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )



# Help Buttons Callback
async def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = f"Here is the help for *{HELPABLE[module].__mod_name__}* module:\n" + HELPABLE[module].__help__
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(text="➥ Support", url=f"https://telegram.me/{SUPPORT_CHAT}"),
                        InlineKeyboardButton(text="➥ Updates", url=f"https://telegram.me/{UPDATES_LOGS}"),
                        InlineKeyboardButton(text="➥ Global", url=f"https://telegram.me/{GLOBAL_LOGS}")
                    ],
                    [
                        InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                        InlineKeyboardButton(text="☆ Back", callback_data="help_back")
                    ],
                ]),
            )
        elif prev_match:
            curr_page = int(prev_match[1])
            await query.message.edit_text(
                text=HELP_SECTION_STRING.format(
                    context.bot.first_name,
                    SUPPORT_CHAT,
                    SUPPORT_CHAT
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELPABLE, "help"))
            )
        elif next_match:
            next_page = int(next_match[1])
            await query.message.edit_text(
                text=HELP_SECTION_STRING.format(
                    context.bot.first_name,
                    SUPPORT_CHAT,
                    SUPPORT_CHAT
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(paginate_modules(next_page + 1, HELPABLE, "help")),
            )
        elif back_match:
            await query.message.edit_text(
                text=HELP_SECTION_STRING.format(
                    context.bot.first_name,
                    SUPPORT_CHAT,
                    SUPPORT_CHAT
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
            )
        # ensure no spinny white circle
        await context.bot.answer_callback_query(query.id)
        # await query.message.delete()
    except BadRequest:
        pass



# get Help Callback
async def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)
    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        update.effective_message.reply_animation(
            BOT_START_GIF,
            HELP_GROUP_STRING,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="☆ Help", url=f"https://telegram.me/{context.bot.username}?start=help")
                ]
            ]),
        )
        return
    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = f"Here is the available help for the *{HELPABLE[module].__mod_name__}* module:\n" + HELPABLE[module].__help__
        send_help(
            chat.id, text,
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="➥ Support", url=f"https://telegram.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton(text="➥ Updates", url=f"https://telegram.me/{UPDATES_LOGS}"),
                    InlineKeyboardButton(text="➥ Global", url=f"https://telegram.me/{GLOBAL_LOGS}")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Back", callback_data="help_back")
                ]
            ])
        )
    else:
        send_help(chat.id, HELP_SECTION_STRING.format(context.bot.first_name, SUPPORT_CHAT, SUPPORT_CHAT))



# Help Sections
async def about_callback_handler(update, context):
    query = update.callback_query
    if query.data == "about_section":
        await query.message.edit_text(
            text=ABOUT_SECTION_STRING.format(
                context.bot.first_name,
                context.bot.first_name,
                SOURCE_CODE[0],
                SOURCE_CODE[2],
                SOURCE_CODE[3],
                SOURCE_CODE[1],
                SOURCE_CODE[2],
                SOURCE_CODE[3],
                SUPPORT_CHAT,
                UPDATES_LOGS
                ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="➥ Credits", callback_data="credits_section"),
                    InlineKeyboardButton(text="➥ Support", callback_data="support_section"),
                    InlineKeyboardButton(text="➥ Manual", callback_data="manual_section")
                ],
                [
                    InlineKeyboardButton(text="➥ T & C", callback_data="tandc_section")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                ],
            ])
        )
    elif query.data == "rajni_back":
        await query.message.edit_text(
            START_SECTION_STRING.format(escape_markdown(context.bot.first_name), BOT_START_PIC, escape_markdown(uptime), sql.num_users(), sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(
                InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(text=f"▻ Add {BOT_NAME} to your group", url=f"t.me/{BOT_USERNAME}?startgroup=true")
                    ],
                    [
                        InlineKeyboardButton(text="☆ About", callback_data="about_section"),
                        InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                    ],
                ])
            ),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )



async def support_callback_handler(update, context):
    query = update.callback_query
    if query.data == "support_section":
        await query.message.edit_text(
            text=SUPPORT_SECTION_STRING.format(
                SUPPORT_CHAT,
                UPDATES_LOGS
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Back", callback_data="about_section")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                ],
            ])
        )



async def credits_callback_handler(update, context):
    query = update.callback_query
    if query.data == "credits_section":
        await query.message.edit_text(
            text=CREDITS_SECTION_STRING.format(
                OWNER_USERNAME
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Back", callback_data="about_section")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                ],
            ])
        )



async def term_condition_handler(update, context):
    query = update.callback_query
    if query.data == "tandc_section":
        await query.message.edit_text(
            text=TANDC_SECTION_STRING.format(
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name,
                SUPPORT_CHAT,
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name,
                SUPPORT_CHAT
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Back", callback_data="about_section")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                ],
            ])
        )



async def manual_callback_handler(update, context):
    query = update.callback_query
    if query.data == "manual_section":
        await query.message.edit_text(
            text=MANUAL_SECTION_STRING.format(
                context.bot.first_name
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Add Me", url=f"https://telegram.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    InlineKeyboardButton(text="Admin Setup", callback_data="admin_setup_section"),
                    InlineKeyboardButton(text="Anti-Spam Setup", callback_data="antispam_setup_section")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data="about_section")
                ]
            ])
        )



async def admin_setup_handler(update, context):
    query = update.callback_query
    if query.data == "admin_setup_section":
        await query.message.edit_text(
            text=ADMIN_SETUP_STRING.format(
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name,
                context.bot.first_name
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Back", callback_data="manual_section"),
                    InlineKeyboardButton(text="About", callback_data="about_section")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                ]
            ])
        )


 
async def antispam_setup_handler(update, context):
    query = update.callback_query
    if query.data == "antispam_setup_section":
        await query.message.edit_text(
            text=ANTISPAM_SETUP_STRING,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="About", callback_data="about_section")
                ],
                [
                    InlineKeyboardButton(text="☆ Home", callback_data="rajni_back"),
                    InlineKeyboardButton(text="☆ Help", callback_data="help_back")
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data="manual_section")
                ]
            ])
        )




# Send Settings Handler
async def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(f"*{mod.__mod_name__}*:\n{mod.__user_settings__(user_id)}"
            for mod in USER_SETTINGS.values()
            )
            await RAJNI_PTB.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" +  settings,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await RAJNI_PTB.bot.send_message(
                user_id,
                "Seems like there aren\'t any user specific settings available.",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        if CHAT_SETTINGS:
            chat_name = RAJNI_PTB.bot.getChat(chat_id).title
            await RAJNI_PTB.bot.send_message(
                user_id,
                text=f"Which module would you like to check {chat_name}'s settings for?",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                )
            )
        else:
            await RAJNI_PTB.bot.send_message(
                user_id,
                text="Seems like there aren't any chat settings available,\nSend this in a group chat you\'re admin in to find it\'s current settings!",
                parse_mode=ParseMode.MARKDOWN
            )



# Settings Button Callback
async def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            await query.message.reply_text(
                text = f"*{escape_markdown(chat.title)}* has the following settings for the *{CHAT_SETTINGS[module].__mod_name__}* module:\n\n" + \
                    CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(text="Back", callback_data="stngs_back({chat_id})")
                    ]
                ])
            )
        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            await query.message.reply_text(
                text=f"Hi there! There are quite a few settings for {chat.title} - go ahead and pick what you're interested in.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id)
                )
            )
        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            await query.message.reply_text(
                text=f"Hi there! There are quite a few settings for {chat.title} - go ahead and pick what you're interested in.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id)
                )
            )
        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            await query.message.reply_text(
                text=f"Hi there! There are quite a few settings for {escape_markdown(chat.title)} - go ahead and pick what you're interested in.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                )
            )
        # ensure no spinny white circle
        await bot.answer_callback_query(query.id)
        await query.message.delete()
    except BadRequest as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))



async def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type Optional[Chat]
    user = update.effective_user  # type Optional[User]
    msg = update.effective_message  # type Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
        else:
            text = "Click here to check your settings."
        await msg.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="☆ Settings", url=f"t.me/{context.bot.username}?start=stngs_{chat.id}")
                ]
            ])
        )
    else:
        send_settings(chat.id, user.id, True)



# Donate Section Handler
async def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type Optional Chat
    bot = context.bot
    donate_promotional_buttons = [
        [
            InlineKeyboardButton(text="Updates", url=f"https://telegram.me/{UPDATES_LOGS}"),
            InlineKeyboardButton(text="Support", url=f"https://telegram.me/{SUPPORT_CHAT}"),
            InlineKeyboardButton(text="Global", url="https://telegram.me/{GLOBAL_LOGS}")
        ],
        [
            InlineKeyboardButton(text="Follow TeamUltraUnion (Github)", url="https://github.com/TeamUltraUnion")
        ],
        [
            InlineKeyboardButton(text="Team Unix", url="https://telegram.me/TeamUnixSystem"),
            InlineKeyboardButton(text="Mystical Illusion", url="https://telegram.com/MysticalIllusion")
        ]
    ]
    if chat.type == "private":
        await update.effective_message.reply_text(
            text=DONATE_SECTION_STRING,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Donate Now", url=DONATION_LINK)
                ]
            ])
        )
        if OWNER_ID != 254318997 and DONATION_LINK:
            await update.effective_message.reply_text(
                text="Thanks for supporting us! :D\nYou can join our Group & Channels instead too ;)",
                disable_web_page_preview=True,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(donate_promotional_buttons)
            )
    else:
        try:
            await bot.send_message(user.id, DONATE_SECTION_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            await update.effective_message.reply_text(
                text="I'm free for everyone❤️\njust donate by join updates channel & support chat as well.",
                reply_markup=InlineKeyboardMarkup(donate_promotional_buttons)
            )
        except Forbidden:
            await update.effective_message.reply_text("Contact me in PM first to get donation information.")



# Chats Migration
async def migrate_chats(update: Update):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", old_chat, new_chat)
    for mod in MIGRATEABLE:
        with contextlib.suppress(KeyError, AttributeError):
            mod.__migrate__(old_chat, new_chat)
    LOGGER.info("Successfully migrated!")



async def safe_telethon_start():
    while True:
        try:
            # ✅ FIX: Pass the bot token explicitly so Telethon logs in automatically as a bot
            await telethn.start(bot_token=TOKEN) 
            LOGGER.info("Telethon bot started successfully.")
            return True
        except telethon_errors.FloodWaitError as e:
            wait = int(e.seconds) + 10
            LOGGER.warning(f"Telethon FloodWait: sleeping {wait}s")
            await asyncio.sleep(wait)
        except Exception as e:
            LOGGER.error(f"Telethon failed to start: {e}")
            LOGGER.error(traceback.format_exc())
            return False



async def userbot_safe_start(client, name):
    while True:
        try:
            await client.start()
            LOGGER.info(f"{name} started successfully.")
            return True
        except telethon_errors.FloodWaitError as e:
            wait = int(e.seconds) + 10
            LOGGER.warning(f"{name} FloodWait: sleeping {wait}s")
            await asyncio.sleep(wait)
        except Exception as e:
            # Catching Pyrogram FloodWait explicitly if raised dynamically
            if "FloodWait" in str(type(e)) or hasattr(e, "value"):
                wait = getattr(e, "value", 15) + 5
                LOGGER.warning(f"{name} FloodWait caught: sleeping {wait}s")
                await asyncio.sleep(wait)
                continue
            LOGGER.error(f"{name} failed: {e}")
            LOGGER.error(traceback.format_exc())
            return False



async def start_clients():
    LOGGER.info("Starting all Telegram clients concurrently...")
    # Use asyncio.gather to prevent one failing framework from blocking the others
    results = await asyncio.gather(
        safe_telethon_start(),
        userbot_safe_start(pgram, "Pyrogram"),
        userbot_safe_start(ubot, "Userbot"),
        return_exceptions=True
    )
    LOGGER.info(f"[{BOT_NAME}] | Telegram clients startup attempt complete. Statuses: {results}")



# --- 3. HANDLER CONFIGURATION ---
def setup_handlers():
    RAJNI_PTB.add_handler(DisableAbleCommandHandler("start", start))
    RAJNI_PTB.add_handler(DisableAbleCommandHandler("test", test))
    RAJNI_PTB.add_handler(DisableAbleCommandHandler("help", get_help))
    RAJNI_PTB.add_handler(CallbackQueryHandler(help_button, pattern=r"help_.*"))
    RAJNI_PTB.add_handler(DisableAbleCommandHandler("settings", get_settings))
    RAJNI_PTB.add_handler(CallbackQueryHandler(settings_button, pattern=r"stngs_"))
    RAJNI_PTB.add_handler(DisableAbleCommandHandler("donate", donate))

    RAJNI_PTB.add_handler(CallbackQueryHandler(about_callback_handler, pattern=r"about_section"))
    RAJNI_PTB.add_handler(CallbackQueryHandler(support_callback_handler, pattern=r"support_section"))
    RAJNI_PTB.add_handler(CallbackQueryHandler(credits_callback_handler, pattern=r"credits_section"))
    RAJNI_PTB.add_handler(CallbackQueryHandler(term_condition_handler, pattern=r"tandc_section"))
    RAJNI_PTB.add_handler(CallbackQueryHandler(manual_callback_handler, pattern=r"manual_section"))
    RAJNI_PTB.add_handler(CallbackQueryHandler(admin_setup_handler, pattern=r"admin_setup_section"))
    RAJNI_PTB.add_handler(CallbackQueryHandler(antispam_setup_handler, pattern=r"antispam_setup_section"))

    RAJNI_PTB.add_handler(MessageHandler(filters.StatusUpdate.MIGRATE, migrate_chats))
    RAJNI_PTB.add_error_handler(error_callback)



# --- 4. SHUTDOWN LOGIC ---
# Global flag to completely prevent back-to-back concurrent triggers
SHUTTING_DOWN = False

async def shutdown():
    global SHUTTING_DOWN
    if SHUTTING_DOWN:
        return  # Exit immediately if shutdown is already running
    SHUTTING_DOWN = True

    LOGGER.info(f"[{BOT_NAME}] | Shutting down frameworks safely...")
    
    # 1. Shutdown Python-Telegram-Bot
    try:
        if RAJNI_PTB.updater and RAJNI_PTB.updater.running:
            await RAJNI_PTB.updater.stop()
        
        # Guard checking framework run states safely for PTB v21
        if getattr(RAJNI_PTB, "running", False):
            await RAJNI_PTB.stop()
            await RAJNI_PTB.shutdown()
        LOGGER.info("PTB closed cleanly.")
    except Exception as e:
        LOGGER.error(f"Error stopping PTB: {e}")

    # 2. Shutdown Telethon Clients (Main Telethon + Telethon Userbot)
    for telethon_client, name in [(telethn, "Telethon Main"), (ubot, "Userbot")]:
        try:
            if telethon_client and telethon_client.is_connected():
                await telethon_client.disconnect()
            LOGGER.info(f"{name} disconnected cleanly.")
        except Exception as e:
            LOGGER.error(f"Error disconnecting {name}: {e}")

    # 3. Shutdown Pyrogram Client cleanly
    try:
        if pgram:
            is_connected = pgram.is_connected
            if callable(is_connected):
                is_connected = await is_connected() if asyncio.iscoroutinefunction(is_connected) else is_connected()
            
            if is_connected:
                await pgram.stop(block=False)
            LOGGER.info("Pyrogram closed cleanly.")
    except Exception as e:
        LOGGER.error(f"Error stopping Pyrogram: {e}")

    # 4. Final session cleanup
    try:
        # Added your global HTTPX AsyncClient closure here to fix the unclosed warning
        await close_http_client()
        await close_aiohttp_session()
        LOGGER.info(f"[{BOT_NAME}] | All network sessions closed cleanly.")
    except Exception as e:
        LOGGER.error(f"Error closing HTTP sessions: {e}")

    LOGGER.info(f"[{BOT_NAME}] | Shutdown complete.")



# --- 5. MAIN BOOTSTRAP SYSTEM ---
async def main():
    session_status = await init_aiohttp_session()
    if not session_status.get("status"):
        LOGGER.error(f"[{BOT_NAME}] | aiohttp session failed.")
        sys.exit(1)

    await init_arq_client(session_status["aiohttpsession"])
    await start_clients()

    await asyncio.sleep(2)

    # --- PROPER PTB MANUAL INTERFACE LIFECYCLE ---
    await RAJNI_PTB.initialize()

     # ✅ FIX: Register handlers FIRST while the update pipeline is still clear
    setup_handlers() 

    await RAJNI_PTB.updater.start_polling()
    await RAJNI_PTB.start()
    LOGGER.info(f"[{BOT_NAME}] | PTB initialized and polling successfully.")

    if ERROR_LOGS:
        try:
            LOGGER.info(f"[{BOT_NAME}] | Attempting to send online status at the ERROR LOGS Channel ({ERROR_LOGS}).")
            await RAJNI_PTB.bot.send_message(f"@{ERROR_LOGS}", "I am now online!")
        except TelegramError as e:
            LOGGER.warning(f"{BOT_NAME} couldn't send log initialization alert: {e.message}")
    else:
        LOGGER.error(f"[{BOT_NAME}] | ERROR_LOGS Channel not mentioned.")

    LOGGER.info(f"[{BOT_NAME}] | TUU • Connection Successful!")
    LOGGER.info(f"[{BOT_NAME}] | TUU • {BOT_NAME} deployed, check @{SUPPORT_CHAT}")
    LOGGER.info(f"[{BOT_NAME}] | TUU • entering main loop block.")

    # Shared continuous runtime keep-alive engine
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        LOGGER.info("Main loop task cancelled.")
    finally:
        await shutdown()



if __name__ == '__main__':
    LOGGER.info("=" * 50)
    
    # Setup standard process signal hooks cleanly across platforms
    loop = asyncio.get_event_loop()
    main_task = None
    
    def signal_handler():
        LOGGER.info("System interruption received! Triggering graceful termination...")
        if main_task:
            main_task.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            # Fallback handling structure for development on Windows OS
            pass

    try:
        main_task = loop.create_task(main())
        loop.run_until_complete(main_task)
        LOGGER.info(f"\n===================================\n[{BOT_NAME}] | TUU | BOT STOPPED CLEANLY\n===================================\n")
    except KeyboardInterrupt:
        LOGGER.info(f"\n===================================\n[{BOT_NAME}] | TUU | SHUTDOWN THROUGH TERMINAL INTERRUPT\n===================================\n")
    except Exception as e:
        LOGGER.error(f"\n===================================\n[{BOT_NAME}] | TUU | DEPLOYMENT CRITICAL FAILURE\n\nError: {e}\n{traceback.format_exc()}\n===================================\n")