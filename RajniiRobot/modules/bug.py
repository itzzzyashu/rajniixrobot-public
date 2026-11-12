from datetime import datetime

from telethon import events
from telethon.tl.custom import Button

from RajniiRobot import telethn, OWNER_ID, OWNER_USERNAME, SUPPORT_CHAT
from RajniiRobot.utils.errors import capture_err


def content(text: str) -> [None, str]:
    if not text:
        return None
    if " " not in text:
        return None
    try:
        return text.split(None, 1)[1]
    except IndexError:
        return None


@telethn.on(events.NewMessage(pattern=r"^/bug(?:\s|$)", incoming=True))
@capture_err
async def bug(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    if not sender:
        return

    if event.is_private:
        await event.reply("❎ <b>This command only works in groups.</b>", parse_mode='html')
        return

    if chat.username:
        chat_username = f"@{chat.username} / `{chat.id}`"
    else:
        chat_username = f"Private Group / `{chat.id}`"

    bugs = content(event.raw_text)
    user_id = sender.id
    mention = f"<a href='tg://user?id={user_id}'>{sender.first_name}</a>"

    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    bug_report = f"""
**#BUG : ** **@{OWNER_USERNAME}**
**From User : ** **{mention}**
**User ID : ** **{user_id}**
**Group : ** **{chat_username}**
**Bug Report : ** **{bugs}**
**Event Stamp : ** **{datetimes}**"""

    if user_id == OWNER_ID:
        if bugs:
            await event.reply("❎ <b>How can be owner bot reporting bug??</b>", parse_mode='html')
            return
        await event.reply("Owner noob!")
    elif bugs:
        buttons = [[Button.inline("Close", data="close_reply")]]
        await event.reply(
            f"<b>Bug Report : {bugs}</b>\n\n"
            "✅ <b>The bug was successfully reported to the support group!</b>",
            parse_mode='html',
            buttons=buttons,
        )

        thumb = "https://i.pinimg.com/564x/f2/47/8b/f2478ba4e193470ebcdf61a2ad0f33ce.jpg"
        msg_link = await event.get_link()

        support_buttons = [
            [Button.url("➡ View Bug", msg_link)],
            [Button.inline("❌ Close", data="close_send_photo")]
        ]

        await telethn.send_message(
            SUPPORT_CHAT,
            file=thumb,
            message=bug_report,
            parse_mode='markdown',
            buttons=support_buttons
        )
    else:
        await event.reply("❎ <b>No bug to Report!</b>", parse_mode='html')


@telethn.on(events.CallbackQuery(data=b"close_reply"))
async def close_reply(event):
    await event.delete()


@telethn.on(events.CallbackQuery(data=b"close_send_photo"))
async def close_send_photo(event):
    sender_id = event.sender_id
    chat_id = event.chat_id
    
    try:
        perms = await telethn.get_permissions(chat_id, sender_id)
        is_admin = perms and perms.is_admin
        can_delete = perms.participant.admin_rights.delete_messages if perms and perms.participant and perms.participant.admin_rights else False
    except Exception:
        is_admin = False
        can_delete = False

    if sender_id != OWNER_ID and not can_delete:
        await event.answer("You're not allowed to close this.", alert=True)
        return
        
    await event.delete()


__mod_name__ = "Bug"