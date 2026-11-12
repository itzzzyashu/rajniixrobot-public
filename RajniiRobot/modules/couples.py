import random

from datetime import datetime
from telethon import events
from RajniiRobot import telethn as app, BOT_USERNAME
from RajniiRobot.utils.errors import capture_err
from RajniiRobot.modules.mongo.couples_mongo import get_couple, save_couple

__mod_name__ = "Couples"


# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (str(int(dt()[0].split("/")[0]) + 1) + "/" + dt()[0].split("/")[1] +
         "/" + dt()[0].split("/")[2])
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())


@app.on(events.NewMessage(pattern=f"^/couples(?:@{BOT_USERNAME})?$", incoming=True))
@capture_err
async def couple(event):
    if event.is_private:
        return await event.reply("This command only works in groups[cite: 3].")
    try:
        chat_id = event.chat_id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for user in app.iter_participants(chat_id):
                if not user.bot:
                    list_of_users.append(user.id)
            if len(list_of_users) < 2:
                return await event.reply("Not enough users[cite: 3]")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            
            c1_user = await app.get_entity(c1_id)
            c2_user = await app.get_entity(c2_id)
            
            c1_mention = f"[{c1_user.first_name}](tg://user?id={c1_id})"
            c2_mention = f"[{c2_user.first_name}](tg://user?id={c2_id})"

            couple_selection_message = f"""**Couple of the day:**[cite: 3]
{c1_mention} + {c2_mention} = ❤️[cite: 3]
__New couple of the day may be chosen at 12AM {tomorrow}__[cite: 3]"""
            await event.respond(couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_user = await app.get_entity(c1_id)
            c2_user = await app.get_entity(c2_id)
            c1_name = c1_user.first_name
            c2_name = c2_user.first_name
            couple_selection_message = f"""Couple of the day:[cite: 3]
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = ❤️[cite: 3]
__New couple of the day may be chosen at 12AM {tomorrow}__[cite: 3]"""
            await event.respond(couple_selection_message)
    except Exception as e:
        print(e)
        await event.reply(str(e))