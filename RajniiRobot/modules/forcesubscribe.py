import logging
import time

from telethon import events, Button
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatBannedRights,
    ChannelParticipantCreator,
    ChannelParticipantAdmin,
)
from telethon.errors import RPCError
from telethon.errors.rpcerrorlist import (
    ChatAdminRequiredError,
    UserIdInvalidError,
    UsernameNotOccupiedError,
    UserNotParticipantError,
    ChannelPrivateError,
)

from RajniiRobot import BOT_ID, OWNER_ID as SUDO_USERS, telethn
from RajniiRobot.modules.sql import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)


@telethn.on(events.CallbackQuery(pattern=r"^onUnMuteRequest$"))
async def _onUnMuteRequest(event):
    try:
        user_id = event.sender_id
        chat_id = event.chat_id
    except:
        return
    
    if chat_db := sql.fs_settings(chat_id):
        channel = chat_db.channel
        try:
            # Check bot admin status in chat
            bot_participant = await telethn.get_permissions(chat_id, BOT_ID)
            if not bot_participant.is_admin:
                return await telethn.send_message(
                    chat_id,
                    f"❗ **A user is trying to UnMute himself but i can't unmute him because i am not an admin in this chat add me as admin again.**\n__#Leaving this chat...__",
                )
            
            chat_member = await telethn.get_permissions(chat_id, user_id)
        except Exception:
            return

        if chat_member.is_banned:
            # Check if restricted/banned by bot
            # Telethon doesn't easily expose who restricted via get_permissions, but we can verify status
            try:
                await telethn(
                    telethon.tl.functions.channels.GetParticipantRequest(
                        channel=channel, user_id=user_id
                    )
                )
                # If no exception, user has joined the channel, so unban/unmute them
                unmute_rights = ChatBannedRights(
                    until_date=None,
                    view_messages=False,
                    send_messages=False,
                    send_media=False,
                    send_stickers=False,
                    send_gifs=False,
                    send_games=False,
                    send_inline=False,
                    embed_links=False,
                )
                await telethn.edit_permissions(chat_id, user_id, unmute_rights)
                await event.delete()
            except UserNotParticipantError:
                await event.answer(
                    text=f"❗ Join our @{channel} channel and press 'UnMute Me' button.",
                    alert=True,
                )
            except ChannelPrivateError:
                unmute_rights = ChatBannedRights(
                    until_date=None,
                    view_messages=False,
                    send_messages=False,
                    send_media=False,
                    send_stickers=False,
                    send_gifs=False,
                    send_games=False,
                    send_inline=False,
                    embed_links=False,
                )
                await telethn.edit_permissions(chat_id, user_id, unmute_rights)
                await event.delete()
        else:
            await event.answer(
                text="❗ Warning! Don't press the button when you can talk.",
                alert=True,
            )


@telethn.on(events.MessageEdited(incoming=True))
async def _check_member(event):
    if event.is_private:
        return
    chat_id = event.chat_id
    if chat_db := sql.fs_settings(chat_id):
        try:
            user_id = event.sender_id
            if not user_id:
                return
        except:
            return
        
        try:
            permissions = await telethn.get_permissions(chat_id, user_id)
            if not permissions.is_admin and not permissions.is_creator:
                channel = chat_db.channel
                try:
                    await telethn(
                        telethon.tl.functions.channels.GetParticipantRequest(
                            channel=channel, user_id=user_id
                        )
                    )
                except UserNotParticipantError:
                    try:
                        sender = await event.get_sender()
                        sender_mention = f"[{sender.first_name}](tg://user?id={user_id})" if sender else "User"
                        
                        buttons = [
                            [Button.url("Join Channel", url=f"https://telegram.dog/{channel}")],
                            [Button.inline("UnMute Me", data="onUnMuteRequest")]
                        ]
                        
                        sent_message = await event.reply(
                            f"Welcome {sender_mention} 🙏 \n **You havent joined our @{channel} Channel yet** 😭 \n \nPlease Join [Our Channel](https://telegram.dog/{channel}) and hit the **UNMUTE ME** Button. \n \n ",
                            link_preview=False,
                            buttons=buttons,
                        )

                        restrict_rights = ChatBannedRights(
                            until_date=None,
                            view_messages=False,
                            send_messages=True,
                        )
                        await telethn.edit_permissions(chat_id, user_id, restrict_rights)
                    except ChatAdminRequiredError:
                        await sent_message.edit(
                            "❗ **Cutiepii Robot 愛 is not an admin here..**\n__Give me ban permissions and retry.. \n#Ending FSub...__"
                        )
                    except RPCError:
                        return

                except ChatAdminRequiredError:
                    await event.respond(
                        text=f"❗ **I am not an admin of @{channel} channel.**\n__Give me admin of that channel and retry.\n#Ending FSub...__",
                    )
                except ChannelPrivateError:
                    return
        except:
            return


@telethn.on(
    events.NewMessage(
        pattern=r"^[/.\?-](?:forcesubscribe|forcesub)(?:@RajniiRobot)?$",
        incoming=True,
    )
)
async def config(event):
    if event.is_private:
        return
    
    try:
        creator_check = await telethn.get_permissions(event.chat_id, event.sender_id)
        is_creator = creator_check.is_creator
    except:
        is_creator = False

    if is_creator or event.sender_id in SUDO_USERS:
        chat_id = event.chat_id
        args = event.text.split()
        if len(args) > 1:
            input_str = args[1].replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                await event.reply("❌ **Force Subscribe is Disabled Successfully.**")
            elif input_str.lower() in ("clear"):
                sent_message = await event.reply("**Unmuting all members who are muted by me...**")
                try:
                    async for user in telethn.iter_participants(chat_id, filter=telethon.tl.types.ChannelParticipantsBanned):
                        unmute_rights = ChatBannedRights(
                            until_date=None,
                            view_messages=False,
                            send_messages=False,
                        )
                        await telethn.edit_permissions(chat_id, user.id, unmute_rights)
                        time.sleep(1)
                    await sent_message.edit("✅ **UnMuted all members who are muted by me.**")
                except ChatAdminRequiredError:
                    await sent_message.edit(
                        "❗ **I am not an admin in this chat.**\n__I can't unmute members because i am not an admin in this chat make me admin with ban user permission.__"
                    )
            else:
                try:
                    await telethn(
                        telethon.tl.functions.channels.GetParticipantRequest(
                            channel=input_str, user_id="me"
                        )
                    )
                    sql.add_channel(chat_id, input_str)
                    await event.reply(
                        f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe this [channel](https://telegram.dog/{input_str}) in order to send messages in this group.__",
                        link_preview=False,
                    )
                except UserNotParticipantError:
                    await event.reply(
                        f"❗ **Not an Admin in the Channel**\n__I am not an admin in the [channel](https://telegram.dog/{input_str}). Add me as a admin in order to enable ForceSubscribe.__",
                        link_preview=False,
                    )
                except (UsernameNotOccupiedError, UserIdInvalidError):
                    await event.reply("❗ **Invalid Channel Username.**")
                except Exception as err:
                    await event.reply(f"❗ **ERROR:** ```{err}```")
        elif sql.fs_settings(chat_id):
            await event.reply(
                f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel](https://telegram.dog/{sql.fs_settings(chat_id).channel})__",
                link_preview=False,
            )
        else:
            await event.reply("❌ **Force Subscribe is disabled in this chat.**")
    else:
        await event.reply(
            "❗ **Group Creator Required**\n__You have to be the group creator to do that.__"
        )


__help__ = """
*Force Subscribe*:
- RajniiRobot can mute members who are not subscribed your channel until they subscribe
- When enabled I will mute unsubscribed members and show them a unmute button. When they pressed the button I will unmute them

*Setup*
1) First of all add me in the group as admin with ban users permission and in the channel as admin.
Note: Only creator of the group can setup me and i will not allow force subscribe again if not done so.

*Commmands*:
➛ /forcesubscribe*:* To get the current settings.
➛ /forcesubscribe <no/off/disable>*:* To turn of ForceSubscribe.
➛ /forcesubscribe <channel username>*:* To turn on and setup the channel.
➛ /forcesubscribe clear*:* To unmute all members who muted by me.
Note: /forcesub is an alias of /forcesubscribe

"""
__mod_name__ = "F-Sub"