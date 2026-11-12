from functools import wraps
from traceback import format_exc as err

from telethon.errors import ChatWriteForbiddenError, RPCError

from RajniiRobot import SUDO_USERS, LOGGER
from RajniiRobot.utils.pluginhelp import member_permissions


async def authorised(func, subFunc2, event, *args, **kwargs):
    try:
        await func(event, *args, **kwargs)
    except ChatWriteForbiddenError:
        return
    except Exception as e:
        try:
            await event.reply(str(getattr(e, 'message', e)))
        except Exception:
            pass
        e_str = err()
        LOGGER.debug(str(e_str))
    return subFunc2


async def unauthorised(event, permission, subFunc2):
    text = (
        "You don't have the required permission to perform this action. :)"
        + f"\n- **Permission:** `{permission}`"
    )
    try:
        await event.reply(text)
    except ChatWriteForbiddenError:
        return subFunc2


def adminsOnly(permission):
    def subFunc(func):
        @wraps(func)
        async def subFunc2(event, *args, **kwargs):
            chat_id = event.chat_id
            sender = await event.get_sender()
            
            if not sender:
                # Handle anonymous admin messages if applicable
                sender_chat = await event.get_chat()
                if sender_chat and sender_chat.id == event.chat_id:
                    return await authorised(
                        func,
                        subFunc2,
                        event,
                        *args,
                        **kwargs,
                    )
                return await unauthorised(event, permission, subFunc2)
                
            user_id = sender.id
            permissions = await member_permissions(chat_id, user_id)
            
            if user_id not in SUDO_USERS and permission not in permissions:
                return await unauthorised(event, permission, subFunc2)
                
            return await authorised(
                func, subFunc2, event, *args, **kwargs
            )

        return subFunc2

    return subFunc