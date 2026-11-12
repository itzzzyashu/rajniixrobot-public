import os
import re
import time
import requests
import wget

from bs4 import BeautifulSoup
from telethon import events

from RajniiRobot.utils.pluginhelpers import admins_only
from RajniiRobot import telethn


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]mod(?:\s+(.*))?$", incoming=True))
@telethn.on(events.MessageEdited(pattern=r"^[/.\?-]mod(?:\s+(.*))?$"))
@admins_only
async def mudapk(event):
    if event.is_private:
        # If restriction to admins only implies groups/chats, handle or allow as needed
        pass
        
    pablo = await event.reply("`Searching For Mod App.....`")
    args = event.text.split(None, 1)
    if len(args) < 2:
        await pablo.edit(
            "Invalid Command Syntax, Please Check Help Menu To Know More!"
        )
        return
    sgname = args[1]
    PabloEscobar = (
        f"https://an1.com/tags/MOD/?story={sgname}&do=search&subaction=search"
    )
    r = requests.get(PabloEscobar)
    soup = BeautifulSoup(r.content, "html5lib")
    mydivs = soup.find_all("div", {"class": "search-results"})
    if not mydivs:
        return await pablo.edit("No mod app found for the given search query.")
        
    Pop = soup.find_all("div", {"class": "title"})
    sucker = mydivs[0]
    pH9 = sucker.find("a").contents[0]
    file_name = pH9

    pH = sucker.findAll("img")
    imme = wget.download(pH[0]["src"])
    Pablo = Pop[0].a["href"]

    ro = requests.get(Pablo)
    soup = BeautifulSoup(ro.content, "html5lib")

    mydis = soup.find_all("a", {"class": "get-product"})
    if not mydis:
        return await pablo.edit("Could not retrieve the product download link.")

    Lol = mydis[0]
    lemk = "https://an1.com" + Lol["href"]

    rr = requests.get(lemk)
    soup = BeautifulSoup(rr.content, "html5lib")

    script = soup.find("script", type="text/javascript")
    if not script or not script.text:
        return await pablo.edit("Failed to extract download script.")

    leek = re.search(r'href=[\'"]?([^\'" >]+)', script.text)
    if not leek:
        return await pablo.edit("Failed to extract direct download link.")
        
    dl_link = leek.group()[5:]

    r = requests.get(dl_link)
    await pablo.edit("Downloading Mod App")
    apk_filename = f"{file_name}.apk"
    with open(apk_filename, "wb") as f:
        f.write(r.content)
        
    await pablo.edit(f"`Downloaded {file_name}! Now Uploading APK...`")
    
    # Telethon progress bar wrapper function or direct file upload
    async def telethn_progress(current, total):
        # Optional progress handler logic if needed, or omit
        pass

    await telethn.send_file(
        event.chat_id,
        file=apk_filename,
        thumb=imme,
        caption=f"`Uploading {file_name} Mod App`",
        progress_callback=telethn_progress,
        reply_to=event.reply_to_msg_id,
    )
    
    with contextlib.suppress(Exception):
        os.remove(apk_filename)
        os.remove(imme)
    await pablo.delete()