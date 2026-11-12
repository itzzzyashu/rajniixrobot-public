from telethon import events
from telethon.errors import RPCError

from RajniiRobot import telethn
from RajniiRobot.utils.pluginhelpers import admins_only, get_text


@telethn.on(events.NewMessage(pattern=r"^/captedit(?:\s|$)", incoming=True))
@telethn.on(events.MessageEdited(pattern=r"^/captedit(?:\s|$))"))
@admins_only
async def loltime(event):
    if event.is_private:
        return
        
    lol = await event.reply("Processing please wait")
    cap = get_text(event)
    
    if not event.is_reply:
        await lol.edit("reply to any message to edit caption")
        return
        
    reply = await event.get_reply_message()
    try:
        # Copy the message with the new caption to the same chat
        await telethn.send_message(
            event.chat_id,
            reply,
            message=cap
        )
        await lol.delete()
    except RPCError as i:
        await lol.edit(str(i))
        return