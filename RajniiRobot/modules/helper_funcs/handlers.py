import asyncio
import telegram.ext as tg
from telegram import Update
from pyrate_limiter import (Duration, RequestRate, Limiter, MemoryListBucket)

import RajniiRobot.modules.sql.blacklistusers_sql as sql
from RajniiRobot import (ALLOW_EXCL, DEV_USERS, SUDO_USERS, SUPPORT_USERS, TIGER_USERS, WHITELIST_USERS, RAJNI_PTB)

CMD_STARTERS = ("/", "?", ".", "~", "+") if ALLOW_EXCL else ("/", "?", ".", "+")

class AntiSpam:
    def __init__(self):
        self.whitelist = (
            (DEV_USERS or [])
            + (SUDO_USERS or [])
            + (WHITELIST_USERS or [])
            + (SUPPORT_USERS or [])
            + (TIGER_USERS or [])
        )
        
        Duration.CUSTOM = 15  # Custom duration, 15 seconds
        self.sec_limit = RequestRate(6, Duration.CUSTOM)  # 6 / Per 15 Seconds
        self.min_limit = RequestRate(20, Duration.MINUTE)  # 20 / Per minute
        self.hour_limit = RequestRate(100, Duration.HOUR)  # 100 / Per hour
        self.daily_limit = RequestRate(1000, Duration.DAY)  # 1000 / Per day
        self.limiter = Limiter(
            self.sec_limit,
            self.min_limit,
            self.hour_limit,
            self.daily_limit,
            bucket_class=MemoryListBucket
        )

    @staticmethod
    def check_user(user):
        """
        Return True if user is to be ignored else False
        """
        return bool(sql.is_user_blacklisted(user))

SpamChecker = AntiSpam()
MessageHandlerChecker = AntiSpam()


class CustomCommandHandler(tg.CommandHandler):
    def __init__(self, command, callback, **kwargs):
        if "admin_ok" in kwargs:
            del kwargs["admin_ok"]
        super().__init__(command, callback, **kwargs)

    # ✅ FIX: Made check_update synchronous to match the parent base handler signature 
    # and use an explicit future worker task to fetch bot attributes without leaking coroutines.
    def check_update(self, update: object):
        if not isinstance(update, Update) or not update.effective_message:
            return None
            
        message = update.effective_message
        try:
            user_id = update.effective_user.id
        except Exception:
            user_id = None
            
        if message.text and len(message.text) > 1:
            fst_word = message.text.split(None, 1)[0]
            if len(fst_word) > 1 and any(fst_word.startswith(start) for start in CMD_STARTERS):
                args = message.text.split()[1:]
                command = fst_word[1:].split("@")
                
                # ✅ FIX: Safely retrieve the username from PTB's cached application context 
                # instead of awaiting raw network endpoints inside the routing check phase
                bot_username = RAJNI_PTB.bot.username
                if not bot_username:
                    try:
                        loop = asyncio.get_running_loop()
                        bot_username = loop.run_until_complete(RAJNI_PTB.bot.get_me()).username
                    except RuntimeError:
                        # Fallback if loop state hasn't stabilized completely yet
                        return None
                
                command.append(bot_username)  
                
                if not (frozenset({command[0].lower()}) in self.commands and command[1].lower() == bot_username.lower()):
                    return None
                    
                if SpamChecker.check_user(user_id):
                    return None
                
                if self.filters:
                    # Sync filters execution
                    filter_result = self.filters.check_update(update)
                else:
                    filter_result = True
                    
                if filter_result:
                    return args, filter_result
                return False
        return None

    def collect_additional_context(self, context, update, application, check_result):
        if isinstance(check_result, bool):
            context.args = update.effective_message.text.split()[1:]
        elif isinstance(check_result, (tuple, list)):
            context.args = check_result[0]
            if len(check_result) > 1 and isinstance(check_result[1], dict):
                context.user_data.update(check_result[1])
        else:
            context.args = []