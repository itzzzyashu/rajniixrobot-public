import os

from RajniiRobot import telethn, MONGO_DB_URL
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from pymongo import MongoClient


async def is_admins(chat_id: int):
    try:
        return [
            user.id
            async for user in telethn.iter_participants(
                chat_id, filter=ChannelParticipantsAdmins
            )
        ]
    except Exception:
        return []


levellink = [
    "https://telegra.ph/file/8a6319ed2e80c9e0ce4dc.mp4",
    "https://telegra.ph/file/e162746b57234a0a65a26.mp4",
    "https://telegra.ph/file/efddc21909ca5edff01ee.mp4",
    "https://telegra.ph/file/d2c0b1e4e590f2c941b5c.mp4",
    "https://telegra.ph/file/9feb100c211e1c3cd3c01.mp4",
    "https://telegra.ph/file/8b9f7e314ab915eadb3ff.mp4",
    "https://telegra.ph/file/dc99f2d3e1efad001d109.mp4",
    "https://telegra.ph/file/24bd609d460cfbb4d29a9.mp4",
]
levelname = [
    "Team Rocket",
    "Stray God",
    "Vector",
    "Hero Association",
    "Z Warrior",
    "Black Knight",
    "Ghoul",
    "Overlord",
]
levelnum = [2, 5, 15, 25, 35, 50, 70, 100]


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]level$", incoming=True))
async def levelsystem(event):
    if event.is_private:
        return
    leveldb = MongoClient(MONGO_DB_URL)
    toggle = leveldb["ToggleDb"]["Toggle"]
    sender = await event.get_sender()
    if sender:
        user = sender.id
        chat_id = event.chat_id
        admins = await is_admins(chat_id)
        if admins and user not in admins:
            return await event.reply("You are not admin")

    is_level = toggle.find_one({"chat_id": event.chat_id})
    if not is_level:
        toggle.insert_one({"chat_id": event.chat_id})
        await event.reply("Level System Enable")
    else:
        toggle.delete_one({"chat_id": event.chat_id})
        await event.reply("Level System Disable")


@telethn.on(events.NewMessage(incoming=True))
async def level(event):
    if event.is_private:
        return

    # Check for text or media types (document, photo, sticker, animation, video)
    if not (event.text or event.document or event.photo or event.sticker or event.video):
        return

    chat = event.chat_id
    sender = await event.get_sender()
    if not sender or sender.bot:
        return
    user_id = sender.id

    leveldb = MongoClient(MONGO_DB_URL)
    level_col = leveldb["LevelDb"]["Level"]
    toggle = leveldb["ToggleDb"]["Toggle"]

    is_level = toggle.find_one({"chat_id": chat})
    if is_level:
        xpnum = level_col.find_one({"level": user_id, "chatid": chat})

        if xpnum is None:
            newxp = {"level": user_id, "chatid": chat, "xp": 10}
            level_col.insert_one(newxp)
        else:
            xp = xpnum["xp"] + 10
            level_col.update_one(
                {"level": user_id, "chatid": chat}, {"$set": {"xp": xp}}
            )
            l = 0
            while True:
                if xp < ((50 * (l ** 2)) + (50 * l)):
                    break
                l += 1
            xp -= ((50 * ((l - 1) ** 2)) + (50 * (l - 1)))
            if xp == 0:
                user_mention = f"[{sender.first_name}](tg://user?id={user_id})"
                await event.reply(
                    f"🌟 {user_mention}, You have reached level {l}**, Nothing can stop you on your way!"
                )

                for lv in range(len(levelname)) and range(len(levellink)):
                    if l == levelnum[lv]:
                        link = f"{levellink[lv]}"
                        await event.client.send_file(
                            chat,
                            link,
                            caption=f"{user_mention}, You have reached Rank Name **{levelname[lv]}**",
                        )


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]rank$", incoming=True))
async def rank(event):
    if event.is_private:
        return
    chat = event.chat_id
    sender = await event.get_sender()
    if not sender:
        return
    user_id = sender.id

    leveldb = MongoClient(MONGO_DB_URL)
    level_col = leveldb["LevelDb"]["Level"]
    toggle = leveldb["ToggleDb"]["Toggle"]

    is_level = toggle.find_one({"chat_id": chat})
    if is_level:
        xpnum = level_col.find_one({"level": user_id, "chatid": chat})
        if not xpnum:
            return await event.reply("You don't have any XP records yet!")
        xp = xpnum["xp"]
        l = 0
        r = 0
        while True:
            if xp < ((50 * (l ** 2)) + (50 * l)):
                break
            l += 1

        xp -= ((50 * ((l - 1) ** 2)) + (50 * (l - 1)))
        rank_cursor = level_col.find().sort("xp", -1)
        for k in rank_cursor:
            r += 1
            if xpnum["level"] == k["level"]:
                break
        user_mention = f"[{sender.first_name}](tg://user?id={user_id})"
        await event.reply(
            f"{user_mention} Level Info:\nLevel: {l}\nProgess: {xp}/{int(200 * ((1 / 2) * l))}\n Ranking: {r}"
        )