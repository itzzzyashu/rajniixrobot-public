import os
import time
import html
import aiohttp
import asyncio
import datetime
import tempfile

from urllib.parse import quote as urlencode
from decimal import Decimal
from datetime import timedelta
from telethon import events, Button
from RajniiRobot import telethn

session = aiohttp.ClientSession()
progress_callback_data = {}


def format_bytes(size):
    size = int(size)
    power = 1024
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]+'B'}"


def return_progress_string(current, total):
    filled_length = int(30 * current // total)
    return '[' + '=' * filled_length + ' ' * (30 - filled_length) + ']'


def calculate_eta(current, total, start_time):
    if not current:
        return "00:00:00"
    end_time = time.time()
    elapsed_time = end_time - start_time
    seconds = (elapsed_time * (total / current)) - elapsed_time
    thing = "".join(str(timedelta(seconds=seconds)
                        ).split(".")[:-1]).split(", ")
    thing[-1] = thing[-1].rjust(8, "0")
    return ", ".join(thing)


@telethn.on(events.NewMessage(pattern=r"^[/!](?:whatanime)(?:\s+(.*))?$", incoming=True))
async def whatanime(event):
    reply = await event.get_reply_message()
    media = None
    
    if event.media:
        media = event.media
    elif reply and reply.media:
        media = reply.media
        
    if not media:
        await event.reply("Please reply it to a Photo or Gif or Video to work")
        return
        
    with tempfile.TemporaryDirectory() as tempdir:
        reply_msg = await event.reply("Downloading media...")
        
        async def progress_callback(current, total):
            await progress(current, total, reply_msg)

        path = await telethn.download_media(media, file=os.path.join(tempdir, "0"), progress_callback=progress_callback)
        new_path = os.path.join(tempdir, "1.png")
        
        proc = await asyncio.create_subprocess_exec("ffmpeg", "-i", path, "-frames:v", "1", new_path)
        await proc.communicate()
        
        await reply_msg.edit("Uploading media to Trace.moe and finding results...")
        with open(new_path, "rb") as file:
            async with session.post("https://api.trace.moe/search?anilistInfo", data={"image": file}) as resp:
                json_resp = await resp.json()
                
    if isinstance(json_resp, str):
        await reply_msg.edit(html.escape(json_resp))
    else:
        try:
            match = json_resp.get("result")
        except StopIteration:
            await reply_msg.edit("No match")
        else:
            if not match:
                return await reply_msg.edit("No match found.")
            match = match[0]
            title_native = match["anilist"]["title"].get("native", "")
            title_english = match["anilist"]["title"].get("english", "")
            title_romaji = match["anilist"]["title"].get("romaji", "")            
            anilist_id = match["anilist"]["id"]
            episode = match.get("episode")
            similarity = match["similarity"]
            synonyms = match["anilist"].get("synonyms", [])
            is_adult = match["anilist"].get("isAdult", False)
            
            from_time = str(datetime.timedelta(seconds=match["from"])).split(
                ".", 1)[0].rjust(8, "0")
            to_time = str(datetime.timedelta(seconds=match["to"])).split(
                ".", 1)[0].rjust(8, "0")
                
            text = f"<b>Anime Name:</b> {title_english or title_romaji}"
            if title_native:
                text += f" ({title_native}) \n "
            if synonyms:
                synonyms.sort()
                syn = ", ".join(synonyms)
                text += f"\n<b>Related:</b> {syn}"

            if is_adult:
                text += "\n<b>NSFW:</b> True"
            text += f"\n<b>Similarity:</b> {(Decimal(str(similarity)) * 100).quantize(Decimal('.01'))}%\n"
            if episode:
                text += f"<b>Episode:</b> {episode}"
            text += f"\n<b>Scene Timestamp:</b> from {from_time} to {to_time}\n"

            buttons = [[Button.url("More Info", url=f"https://anilist.co/anime/{anilist_id}")]]

            async def _send_preview():
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as file:
                    async with session.get(match["video"]) as resp:
                        while True:
                            chunk = await resp.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
                    vid_path = file.name
                try:
                    await telethn.send_file(
                        event.chat_id,
                        file=vid_path,
                        caption=text,
                        buttons=buttons,
                        parse_mode="html",
                        reply_to=event.reply_to_msg_id,
                    )
                    await reply_msg.delete()
                except Exception:
                    await reply_msg.reply("Cannot send preview :/")
                finally:
                    if os.path.exists(vid_path):
                        os.remove(vid_path)
                        
            await _send_preview()


async def progress(current, total, reply):
    message_identifier = (reply.chat_id, reply.id)
    last_edit_time, prevtext, start_time = progress_callback_data.get(
        message_identifier, (0, None, time.time()))
    if current == total:
        try:
            progress_callback_data.pop(message_identifier)
        except (KeyError, IndexError):
            pass
    elif (time.time() - last_edit_time) > 1:
        if last_edit_time:
            download_speed = format_bytes(
                (total - current) / (time.time() - start_time))
        else:
            download_speed = "0 B"
        text = f"""Downloading...
<code>{return_progress_string(current, total)}</code>
<b>Total Size:</b> {format_bytes(total)}
<b>Downloaded Size:</b> {format_bytes(current)}
<b>Download Speed:</b> {download_speed}/s
<b>ETA:</b> {calculate_eta(current, total, start_time)}"""
        if prevtext != text:
            try:
                await reply.edit(text, parse_mode="html")
                prevtext = text
                last_edit_time = time.time()
                progress_callback_data[message_identifier] = last_edit_time, prevtext, start_time
            except Exception:
                pass