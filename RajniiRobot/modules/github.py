import aiohttp

from telethon import events
from RajniiRobot import telethn, LOGGER
from RajniiRobot.utils.errors import capture_err

__mod_name__ = "Github"


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]github$", incoming=True))
@capture_err
async def github(event):
    args = event.text.split(None, 1)
    if len(args) != 2:
        await event.reply("/git Username")
        return
    username = args[1]
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session, session.get(URL) as request:
        if request.status == 404:
            return await event.reply("404")

        result = await request.json()
        try:
            url = result["html_url"]
            name = result["name"]
            company = result["company"]
            bio = result["bio"]
            created_at = result["created_at"]
            avatar_url = result["avatar_url"]
            blog = result["blog"]
            location = result["location"]
            repositories = result["public_repos"]
            followers = result["followers"]
            following = result["following"]
            caption = f"""**Info Of {name}**
**Username:** `{username}`
**Bio:** `{bio}`
**Profile Link:** [Here]({url})
**Company:** `{company}`
**Created On:** `{created_at}`
**Repositories:** `{repositories}`
**Blog:** `{blog}`
**Location:** `{location}`
**Followers:** `{followers}`
**Following:** `{following}`"""
        except Exception as e:
            LOGGER.debug(e)
            return await event.reply("An error occurred while fetching GitHub profile details.")
            
    await telethn.send_file(
        event.chat_id,
        file=avatar_url,
        caption=caption,
        reply_to=event.reply_to_msg_id,
        link_preview=False,
    )