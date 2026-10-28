from time import sleep
from typing import Optional, List
from telegram import Update
from telegram.error import BadRequest, Forbidden, NetworkError, TelegramError
from telegram.ext import Filters, CommandHandler
from telegram.ext.RAJNI_PTB import run_async, CallbackContext

import random
import RajniiRobot.modules.sql.users_sql as sql
from RajniiRobot.modules.helper_funcs.filters import CustomFilters
from RajniiRobot import RAJNI_PTB, OWNER_ID, LOGGER
from RajniiRobot.modules.disable import DisableAbleCommandHandler

USERS_GROUP = 4


@run_async
def snipe(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text(
            "Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except (BadRequest, Forbidden, NetworkError, TelegramError) as e:
            LOGGER.warning(
                f"Couldn\'t send to group {str(chat_id)}\nError: {e}"
            )
            update.effective_message.reply_text(
                f"Couldn\'t send the message. Perhaps I'm not part of that group?\nError: {e}"
            )


__mod_name__ = "Snipe"

SNIPE_HANDLER = CommandHandler("snipe",
                               snipe,
                               pass_args=True,
                               filters=CustomFilters.sudo_filter)

RAJNI_PTB.add_handler(SNIPE_HANDLER)
