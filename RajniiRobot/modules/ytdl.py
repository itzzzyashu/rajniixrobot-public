import traceback
from asyncio import gather
from os import remove
from random import randint

from telethon import events, Button

from RajniiRobot import telethn, arq, BOT_USERNAME
from RajniiRobot.utils.errors import capture_err
from RajniiRobot.utils.formatter import convert_seconds_to_minutes as timeFormat
from RajniiRobot.utils.functions import downloader

VIDEO_DATA = {}


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]ytdl(?:@\w+)?(?:\s+(.*))?$", incoming=True))
@capture_err
async def ytdl_func(event):
    args = event.text.split(None, 1)
    if len(args) != 2:
        return await event.reply(
            "please do like this `/ytdl (VIDEO_LINK)`")
    m = await event.reply("Processing")
    url = args[1]
    results = await arq.ytdl(url)
    if not results.ok:
        return await m.edit(results.result)
        
    result = results.result
    title = result.title
    thumbnail = result.thumbnail
    duration = result.duration
    video = result.video
    
    buttons = []
    keyboard_row = []
    for media in video:
        quality = media.quality
        size = media.size
        media_url = media.url
        media_format = media.format
        data = str(randint(999, 9999999))
        
        VIDEO_DATA[data] = {
            "url": media_url,
            "title": title,
            "size": size,
            "quality": quality,
            "duration": duration,
            "format": media_format,
            "thumbnail": thumbnail,
            "cc": event.sender.first_name if event.sender else "Anon",
        }
        
        keyboard_row.append(Button.inline(f"{quality} | {size}", data=f"ytdl {data}"))
        if len(keyboard_row) == 3:
            buttons.append(keyboard_row)
            keyboard_row = []
            
    if keyboard_row:
        buttons.append(keyboard_row)
        
    caption = f"""
**Title:** {title}
**Duration:** {await timeFormat(duration)}
"""
    await telethn.send_file(
        event.chat_id,
        file=thumbnail,
        caption=caption,
        buttons=buttons,
        parse_mode="markdown",
        reply_to=event.reply_to_msg_id,
    )
    await m.delete()


@telethn.on(events.CallbackQuery(pattern=r"^ytdl"))
async def ytdlCallback(event):
    await event.edit("Downloading")
    data_ = event.data.decode("utf-8").split()[1]
    try:
        data = VIDEO_DATA[data_]
        url = data["url"]
        title = data["title"]
        duration = data["duration"]
        media_format = data["format"]
        size = data["size"]
        thumbnail = data["thumbnail"]
        cc = data["cc"]
        
        caption = f"""
**Title:** {title}
**Size:** {size}
**Format:** {media_format}
**Duration:** {await timeFormat(duration)}
**CC:** {cc}
        """
        media, thumb = await gather(downloader.download(url),
                                    downloader.download(thumbnail))
        await event.edit("Uploading")
        
        if media_format == "mp3":
            await telethn.send_file(
                event.chat_id,
                file=media,
                caption=caption,
                thumb=thumb,
                attributes=[],
                supports_streaming=False,
                reply_to=event.message.reply_to_msg_id,
            )
        else:
            await telethn.send_file(
                event.chat_id,
                file=media,
                caption=caption,
                supports_streaming=True,
                reply_to=event.message.reply_to_msg_id,
            )
            
        del VIDEO_DATA[data_]
        with contextlib.suppress(Exception):
            remove(thumb)
            remove(media)
        await event.delete()
    except Exception as e:
        err_trace = traceback.format_exc()
        print(err_trace)
        if data_ in VIDEO_DATA:
            del VIDEO_DATA[data_]
        await event.delete()


__mod_name__ = "YoutubeDL"