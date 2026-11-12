from telethon import events

from RajniiRobot import telethn
from RajniiRobot.utils.errors import capture_err


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]webss(?:\s+(.*))?$", incoming=True))
@capture_err
async def take_ss(event):
    try:
        args = event.text.split(None, 1)
        if len(args) != 2:
            return await event.reply("Give A Url To Fetch Screenshot.")
        url = args[1]
        m = await event.reply("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await telethn.send_file(
                event.chat_id,
                file=f"https://webshot.amanoteam.com/print?q={url}",
                reply_to=event.reply_to_msg_id,
            )
        except TypeError:
            return await m.edit("No Such Website.")
        await m.delete()
    except Exception as e:
        await event.reply(str(e))


__mod_name__ = "webss"