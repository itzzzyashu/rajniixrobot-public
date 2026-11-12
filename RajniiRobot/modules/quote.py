from io import BytesIO
from traceback import format_exc

from telethon import events

from RajniiRobot.utils.errors import capture_err
from RajniiRobot import arq, telethn, LOGGER


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(event) -> str:
    args = event.text.strip().split(None, 1)
    if len(args) > 1:
        return args[1].strip()
    return ""


def isArgInt(event) -> list:
    arg = getArg(event)
    try:
        count = int(arg)
        return [True, count]
    except ValueError:
        return [False, 0]


@telethn.on(events.NewMessage(pattern=r"^[/.\?-](?:quote|q)(?:\s+(.*))?$", incoming=True))
@telethn.on(events.MessageEdited(pattern=r"^[/.\?-](?:quote|q)(?:\s+(.*))?$"))
@capture_err
async def quote(event):
    if event.is_forwarded:
        return
    try:
        await event.delete()
    except Exception:
        pass

    reply_to = await event.get_reply_message()
    if not reply_to:
        return await event.respond("Reply to a message to quote it.")
    if not reply_to.text:
        return await event.respond(
            "Replied message has no text, can't quote it.")
            
    m = await event.respond("Quoting Messages Please wait....")
    args = event.text.split()
    
    if len(args) < 2:
        messages = [reply_to]
    elif len(args) == 2:
        arg = isArgInt(event)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                return await m.edit("Argument must be between 2-10.")
            count = arg[1]
            # Fetch messages range in Telethon
            messages = []
            for msg_id in range(reply_to.id, reply_to.id + count):
                msg = await telethn.get_messages(event.chat_id, ids=msg_id)
                if msg and msg.text:
                    messages.append(msg)
            messages = messages[:count]
        else:
            if getArg(event) != "r":
                return await m.edit(
                    "Incorrect Argument, Pass **'r'** or **'INT'**, **EX:** __/q 2__"
                )
            # If 'r', fetch message with its reply context if available
            reply_message = reply_to
            messages = [reply_message]
    else:
        return await m.edit(
            "Incorrect argument, check quotly module in help section.")
            
    try:
        if not event:
            return await m.edit("Something went wrong.")
        sticker = await quotify(messages)
        if not sticker[0]:
            await event.respond(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await telethn.send_file(event.chat_id, sticker, reply_to=reply_to.id)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit("Something went wrong while quoting messages," +
                     " This error usually happens when there's a " +
                     " message containing something other than text," +
                     " or one of the messages in-between are deleted.")
        err_trace = format_exc()
        LOGGER.debug(err_trace)


__mod_name__ = "Quotly"