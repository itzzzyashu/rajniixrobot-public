import os
import requests
import wget

from telethon import events

from RajniiRobot import telethn
from RajniiRobot.utils.saavnhelp import get_arg


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]saavn(?:@RajniiRobot)?(?:\s+(.*))?$", incoming=True))
async def song(event):
    if event.is_private:
        return
    arg_text = get_arg(event)
    args = f"{arg_text} song" if arg_text else " song"
    if args.startswith(" ") or not arg_text:
        await event.reply("<b> Song name required!! </b>", parse_mode="html")
        return ""
        
    m = await event.reply("Downloading the song, Please wait...")
    try:
        r = requests.get(f"https://jostapi.herokuapp.com/saavn?query={args}")
        res_json = r.json()
    except Exception as e:
        await m.edit(str(e))
        return
        
    if not res_json:
        return await m.edit("No songs found for the given query.")
        
    sname = res_json[0]["song"]
    slink = res_json[0]["media_url"]
    ssingers = res_json[0]["singers"]
    
    file = wget.download(slink)
    ffile = file.replace("mp4", "m4a")
    if os.path.exists(ffile):
        os.remove(ffile)
    os.rename(file, ffile)
    
    await telethn.send_file(
        event.chat_id,
        file=ffile,
        caption=f"🎵 **Title:** {sname}\n🎤 **Singer(s):** {ssingers}",
        reply_to=event.reply_to_msg_id,
    )
    
    if os.path.exists(ffile):
        os.remove(ffile)
    await m.delete()