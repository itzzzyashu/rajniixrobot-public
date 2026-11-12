import asyncio
import re

from telethon import events

from RajniiRobot import telethn
from RajniiRobot.utils.errors import capture_err
from RajniiRobot.utils.permissions import adminsOnly
from RajniiRobot.modules.mongo.karma_mongo import (alpha_to_int, get_karma,
                                                      get_karmas, int_to_alpha,
                                                      update_karma)
from RajniiRobot.modules.mongo.karma_mongo import is_karma_on, karma_off, karma_on

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|👎)$"


@telethn.on(events.MessageEdited(pattern=regex_upvote, incoming=True))
@capture_err
async def upvote(event):
    if event.is_private:
        return
    chat_id = event.chat_id
    if not await is_karma_on(chat_id):
        return
    
    reply = await event.get_reply_message()
    if not reply or not reply.sender:
        return
    
    sender = await event.get_sender()
    if not sender or reply.sender_id == sender.id or reply.sender.bot:
        return
        
    user_id = reply.sender_id
    user_mention = f"[{reply.sender.first_name}](tg://user?id={user_id})"
    
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma + 1
    else:
        karma = 1
    new_karma = {"karma": karma}
    await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await event.reply(
        f"Incremented Karma of {user_mention} By 1 \nTotal Points: {karma}"
    )


@telethn.on(events.MessageEdited(pattern=regex_downvote, incoming=True))
@capture_err
async def downvote(event):
    if event.is_private:
        return
    chat_id = event.chat_id
    if not await is_karma_on(chat_id):
        return
        
    reply = await event.get_reply_message()
    if not reply or not reply.sender:
        return
        
    sender = await event.get_sender()
    if not sender or reply.sender_id == sender.id or reply.sender.bot:
        return

    user_id = reply.sender_id
    user_mention = f"[{reply.sender.first_name}](tg://user?id={user_id})"
    
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    if current_karma:
        current_karma = current_karma["karma"]
        karma = current_karma - 1
    else:
        karma = 1
    new_karma = {"karma": karma}
    await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
    await event.reply(
        f"Decremented Karma Of {user_mention} By 1 \nTotal Points: {karma}"
    )


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]karma(?:@RajniiRobot)?$", incoming=True))
@capture_err
async def command_karma(event):
    if event.is_private:
        return
    chat_id = event.chat_id
    reply = await event.get_reply_message()
    
    if not reply:
        m = await event.reply("Getting Karma list of top 10 users wait...")
        karma = await get_karmas(chat_id)
        if not karma:
            await m.edit("No karma in DB for this chat.")
            return
            
        chat = await event.get_chat()
        chat_title = chat.title if chat and hasattr(chat, "title") else "this chat"
        msg = f"🏆 Top list of Karma owners in the {chat_title}»: \n"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(
                    karma_dicc.items(),
                    key=lambda item: item[1],
                    reverse=True,
                ))
        if not karma_dicc:
            await m.edit("No karma in DB for this chat.")
            return
            
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                user = await telethn.get_entity(int(user_idd))
                await asyncio.sleep(0.8)
            except Exception:
                continue
            first_name = user.first_name
            if not first_name:
                continue
            username = user.username
            if username:
                msg += f"\n[{first_name}](https://telegram.dog/{username}) — {karma_count}"
            else:
                msg += f"\n[{first_name}](tg://user?id={user.id}) — {karma_count}"
            limit += 1
        await m.edit(msg, link_preview=False)
    else:
        user_id = reply.sender_id
        if not user_id:
            return
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        karma = karma["karma"] if karma else 0
        await event.reply(f"**Total Points**: __{karma}__")


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]karmas$", incoming=True))
@adminsOnly("can_change_info")
async def captcha_state(event):
    if event.is_private:
        return
    usage = "**Usage:**\n/karmas [on|off]"
    args = event.text.split()
    if len(args) != 2:
        return await event.reply(usage)
    chat_id = event.chat_id
    state = args[1].lower()
    if state == "on":
        await karma_on(chat_id)
        await event.reply("Enabled karma System!")
    elif state == "off":
        await karma_off(chat_id)
        await event.reply("Disabled karma System!")
    else:
        await event.reply(usage)


__help__ = """
*Upvote* - Use upvote keywords like "+", "+1", "thanks", etc. to upvote a message.
*Downvote* - Use downvote keywords like "-", "-1", etc. to downvote a message.

*Commands*
➛ /karma*:* reply to a user to check that user's karma points.
➛ /karma*:* send without replying to any message to check karma point list of top 10
➛ /karmas [off/on]*:* Enable/Disable karma in your group.
"""

__mod_name__ = "Karma"