import asyncio
import math
import shlex
import sys
import time
import traceback
from functools import wraps
from typing import Callable, Coroutine, Dict, List, Tuple, Union

from PIL import Image
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import ChannelParticipantsAdmins

from RajniiRobot import OWNER_ID, SUPPORT_CHAT, telethn
from RajniiRobot.utils.errors import split_limits


def get_user(event, text: str) -> Tuple[Union[int, str, None], Union[str, None]]:
    asplit = None if text is None else text.split(" ", 1)
    user_s = None
    reason_ = None
    if event.is_reply:
        pass
    if asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (((str(days) + " day(s), ") if days else "") +
           ((str(hours) + " hour(s), ") if hours else "") +
           ((str(minutes) + " minute(s), ") if minutes else "") +
           ((str(seconds) + " second(s), ") if seconds else "") +
           ((str(milliseconds) + " millisecond(s), ") if milliseconds else ""))
    return tmp[:-2]


async def delete_or_pass(event):
    sender = await event.get_sender()
    if sender and sender.id == 1141839926:
        return event
    return await event.delete()


def humanbytes(size) -> str:
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def progress(current, total, event, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("🔴" for i in range(math.floor(percentage / 10))),
            "".join("🔘" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total),
            time_formatter(estimated_total_time))
        if file_name:
            try:
                await event.edit("{}\n**File Name:** `{}`\n{}".format(
                    type_of_ps, file_name, tmp))
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except Exception:
                pass
        else:
            try:
                await event.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except Exception:
                pass


def get_text(event) -> Union[str, None]:
    text_to_return = event.raw_text
    if not text_to_return or " " not in text_to_return:
        return None

    try:
        return text_to_return.split(None, 1)[1]
    except IndexError:
        return None


async def iter_chats(client):
    chats = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            chats.append(dialog.id)
    return chats


async def fetch_audio(event):
    if not event.is_reply:
        await event.reply("`Reply To A Video / Audio.`")
        return
    reply_msg = await event.get_reply_message()
    if not reply_msg.audio and not reply_msg.video:
        await event.reply("`Format Not Supported`")
        return
    if reply_msg.video:
        lel = await event.reply("`Video Detected, Converting To Audio !`")
        warner_bros = await reply_msg.download_media()
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a friday.mp3"
        await runcmd(stark_cmd)
        final_warner = "friday.mp3"
    elif reply_msg.audio:
        lel = await edit_or_reply(event, "`Download Started !`")
        final_warner = await reply_msg.download_media()
    await lel.edit("`Almost Done!`")
    await lel.delete()
    return final_warner


async def edit_or_reply(event, text, parse_mode="md"):
    if event.is_reply:
        return await event.reply(text, parse_mode=parse_mode)
    return await event.respond(text, parse_mode=parse_mode)


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def convert_to_image(event, client) -> Union[str, None]:
    """Convert Most Media Formats To Raw Image"""
    if not event.is_reply:
        return None
    reply_msg = await event.get_reply_message()
    final_path = None
    if not (reply_msg.photo or reply_msg.sticker or reply_msg.media or reply_msg.document):
        return None
    if reply_msg.photo:
        final_path = await reply_msg.download_media()
    elif reply_msg.sticker:
        if reply_msg.file.mime_type == "image/webp":
            final_path = "webp_to_png_s_proton.png"
            path_s = await reply_msg.download_media()
            im = Image.open(path_s)
            im.save(final_path, "PNG")
        else:
            path_s = await client.download_media(reply_msg)
            final_path = "lottie_proton.png"
            cmd = (
                f"lottie_convert.py --frame 0 -if lottie -of png {path_s} {final_path}"
            )
            await runcmd(cmd)
    elif reply_msg.audio:
        try:
            thumb = reply_msg.audio.thumbs[0]
            final_path = await client.download_media(thumb)
        except Exception:
            pass
    elif reply_msg.video or reply_msg.document:
        final_path = "fetched_thumb.png"
        vid_path = await reply_msg.download_media()
        await runcmd(
            f"ffmpeg -i {vid_path} -filter:v scale=500:500 -an {final_path}")
    return final_path


# Admin check cache dictionary
admins: Dict[str, List] = {}


def set(chat_id: Union[str, int], admins_: List):
    if isinstance(chat_id, int):
        chat_id = str(chat_id)
    admins[chat_id] = admins_


def get(chat_id: Union[str, int]) -> Union[List, bool]:
    if isinstance(chat_id, int):
        chat_id = str(chat_id)
    if chat_id in admins:
        return admins[chat_id]
    return False


async def get_administrators(chat_id) -> List:
    _get = get(chat_id)
    if _get:
        return _get
    
    admin_list = []
    async for user in telethn.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
        admin_list.append(user)
        
    set(chat_id, admin_list)
    return admin_list


def admins_only(func: Callable) -> Coroutine:
    async def wrapper(event, *args, **kwargs):
        sender = await event.get_sender()
        if not sender:
            return
        if sender.id == OWNER_ID:
            return await func(event, *args, **kwargs)
        
        admin_list = await get_administrators(event.chat_id)
        for admin in admin_list:
            if admin.id == sender.id:
                return await func(event, *args, **kwargs)
    return wrapper


def capture_err(func):
    @wraps(func)
    async def capture(event, *args, **kwargs):
        try:
            return await func(event, *args, **kwargs)
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            sender = await event.get_sender()
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not sender else sender.id,
                    0 if not event.chat_id else event.chat_id,
                    event.raw_text,
                    "".join(errors),
                ), )
            for x in error_feedback:
                await telethn.send_message(SUPPORT_CHAT, x)
            raise err
    return capture


# Special credits to TheHamkerCat
async def member_permissions(chat_id: int, user_id: int) -> List[str]:
    perms = []
    try:
        permissions = await telethn.get_permissions(chat_id, user_id)
        if not permissions or not permissions.is_admin:
            return []
        
        p = permissions.participant.admin_rights
        if p:
            if getattr(p, "post_messages", False): perms.append("can_post_messages")
            if getattr(p, "edit_messages", False): perms.append("can_edit_messages")
            if getattr(p, "delete_messages", False): perms.append("can_delete_messages")
            if getattr(p, "ban_users", False): perms.append("can_restrict_members")
            if getattr(p, "add_admins", False): perms.append("can_promote_members")
            if getattr(p, "change_info", False): perms.append("can_change_info")
            if getattr(p, "invite_users", False): perms.append("can_invite_users")
            if getattr(p, "pin_messages", False): perms.append("can_pin_messages")
            if getattr(p, "manage_call", False): perms.append("can_manage_video_chats")
    except Exception:
        return []
    return perms