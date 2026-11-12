from os import remove
from telethon import events

from RajniiRobot import SUDO_USERS, arq, telethn
from RajniiRobot.utils.errors import capture_err
from RajniiRobot.utils.permissions import adminsOnly
from RajniiRobot.modules.mongo.nsfw_mongo import is_nsfw_on, nsfw_off, nsfw_on


async def get_file_from_message(event):
    if not event.media:
        return None
    
    media_type = type(event.media).__name__
    
    # Check document/photo/sticker/animation/video attributes in Telethon
    if media_type == "MessageMediaDocument":
        doc = event.media.document
        if doc.size > 3145728:
            return None
        mime = getattr(doc, "mime_type", "")
        if mime not in ("image/png", "image/jpeg"):
            return None
        return await event.download_media()
        
    elif media_type in ("MessageMediaPhoto", "MessageMediaDocument"):
        return await event.download_media()
        
    return None


@telethn.on(events.NewMessage(incoming=True))
@capture_err
async def detect_nsfw(event):
    if event.is_private:
        return
    if not await is_nsfw_on(event.chat_id):
        return
        
    sender = await event.get_sender()
    if not sender:
        return
        
    # Check if media is present
    if not event.media:
        return
        
    file = await get_file_from_message(event)
    if not file:
        return
        
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        with contextlib.suppress(Exception):
            remove(file)
        return
        
    with contextlib.suppress(Exception):
        remove(file)
        
    if not results.ok:
        return
    results = results.result
    nsfw = results.is_nsfw
    
    if sender.id in SUDO_USERS:
        return
    if not nsfw:
        return
        
    try:
        await event.delete()
    except Exception:
        return
        
    user_mention = f"<a href='tg://user?id={sender.id}'>{sender.first_name}</a>"
    await event.respond(f"""
**NSFW Image Detected & Deleted Successfully!
————————————————————**
**User:** {user_mention} [`{sender.id}`]
**Safe:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Adult:** `{results.sexy} %`
**Hentai:** `{results.hentai} %`
**Drawings:** `{results.drawings} %`
**————————————————————**
__Powered by__@Yuki_Network.
""", parse_mode='html')


@telethn.on(events.NewMessage(pattern=r"^/(nsfwscan|nsfwscan@RajniiRobot)(?:\s|$)", incoming=True))
@capture_err
async def nsfw_scan_command(event):
    if not event.is_reply:
        await event.reply("Reply to an image/document/sticker/animation to scan it.")
        return
        
    reply = await event.get_reply_message()
    if not reply.media:
        await event.reply("Reply to an image/document/sticker/animation to scan it.")
        return
        
    m = await event.reply("Scanning...")
    file = await reply.download_media()
    if not file:
        return await m.edit("Something wrong happened.")
        
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        with contextlib.suppress(Exception):
            remove(file)
        return await m.edit("Scan failed.")
        
    with contextlib.suppress(Exception):
        remove(file)
        
    if not results.ok:
        return await m.edit(str(results.result))
        
    results = results.result
    await m.edit(f"""
**Neutral:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Hentai:** `{results.hentai} %`
**Sexy:** `{results.sexy} %`
**Drawings:** `{results.drawings} %`
**NSFW:** `{results.is_nsfw}`
""")


@telethn.on(events.NewMessage(pattern=r"^/(antinsfw|antinsfw@RajniiRobot)(?:\s|$)", incoming=True))
@adminsOnly("can_change_info")
async def nsfw_enable_disable(event):
    if event.is_private:
        return
        
    args = event.raw_text.split()
    if len(args) != 2:
        await event.reply("Usage: /antinsfw [on/off]")
        return
        
    status = args[1].lower()
    chat_id = event.chat_id
    
    if status in ("on", "yes"):
        await nsfw_on(chat_id)
        await event.reply(
            "Enabled AntiNSFW System. I will Delete Messages Containing Inappropriate Content."
        )
    elif status in ("off", "no"):
        await nsfw_off(chat_id)
        await event.reply("Disabled AntiNSFW System.")
    else:
        await event.reply("Unknown Suffix, Use /antinsfw [on/off]")