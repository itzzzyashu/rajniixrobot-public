import sys
import traceback
from functools import wraps
from RajniiRobot import telethn, SUPPORT_CHAT
from telethon.errors import ChatWriteForbiddenError


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line

    result.append(small_msg)

    return result


def capture_err(func):

    @wraps(func)
    async def capture(event, *args, **kwargs):
        try:
            return await func(event, *args, **kwargs)
        except ChatWriteForbiddenError:
            try:
                await event.client.delete_dialog(event.chat_id)
            except Exception:
                pass
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            
            sender = await event.get_sender()
            user_id = sender.id if sender else 0
            chat_id = event.chat_id if event.chat_id else 0
            text_content = getattr(event, "raw_text", None) or getattr(event, "text", "")

            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    user_id,
                    chat_id,
                    text_content,
                    "".join(errors),
                ), )
            for x in error_feedback:
                await telethn.send_message(SUPPORT_CHAT, x)
            raise err

    return capture