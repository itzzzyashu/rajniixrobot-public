import os
import requests

from telethon import events
from json import JSONDecodeError

from RajniiRobot.utils.pluginhelpers import admins_only, fetch_audio
from RajniiRobot import telethn, SUPPORT_CHAT


@telethn.on(events.NewMessage(pattern=r"^[/.\?-](?:identify|shazam)(?:@RajniiRobot)?$", incoming=True))
@admins_only
async def shazamm(event):
    if event.is_private:
        return
        
    kek = await event.reply("`Shazaming In Progress!`")
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        await kek.edit("Reply To The Audio.")
        return
        
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
        
    downloaded_file_name = await telethn.download_media(reply, file="friday.mp3")
    if not downloaded_file_name or not os.path.exists(downloaded_file_name):
        return await kek.edit("Failed to download media for identification.")
        
    await kek.edit(
        "**Searching For This Song In RajniiRobot\'s DataBase.**")
        
    with open(downloaded_file_name, "rb") as f:
        files = {"file": (downloaded_file_name, f)}
        r = requests.post("https://starkapi.herokuapp.com/shazam/", files=files)
        
    try:
        xo = r.json()
    except JSONDecodeError:
        await kek.edit(
            "`Seems Like Our Server Has Some Issues, Please Try Again Later!`")
        if os.path.exists(downloaded_file_name):
            os.remove(downloaded_file_name)
        return
        
    if xo.get("success") is False:
        await kek.edit("`Song Not Found In Database. Please Try Again.`")
        if os.path.exists(downloaded_file_name):
            os.remove(downloaded_file_name)
        return
        
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    nt = zzz.get("images", {})
    image = nt.get("coverarthq", "")
    by = zzz.get("subtitle", "Unknown")
    title = zzz.get("title", "Unknown")
    
    messageo = f"""<b>Song Shazamed.</b>
<b>Song Name : </b>{title}
<b>Song By : </b>{by}
<u><b>Identified Using @RajniiRobot - Join our support @{SUPPORT_CHAT}</b></u>
<i>Powered by @Yuki_Netowrk</i>
"""

    await telethn.send_file(
        event.chat_id,
        file=image if image else None,
        caption=messageo,
        parse_mode="html",
        reply_to=reply.id,
    )
    
    if os.path.exists(downloaded_file_name):
        os.remove(downloaded_file_name)
    await kek.delete()