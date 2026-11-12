import time

from requests import get
from telethon import events, Button

from RajniiRobot import telethn


def latest():
    url = 'https://subsplease.org/api/?f=schedule&h=true&tz=Japan'
    res = get(url).json()

    k = None
    for x in res['schedule']:
        title = x['title']
        time_str = x['time']
        try:
            aired = bool(x['aired'])
            title = (
                f"**~~[{title}](https://subsplease.org/shows/{x['page']})~~**"
                if aired else
                f"**[{title}](https://subsplease.org/shows/{x['page']})**")

        except (KeyError, IndexError):
            title = f"**[{title}](https://subsplease.org/shows/{x['page']})**"
        data = f"{title} - {time_str}"

        k = f"{k}\n{data}" if k else data
    return k


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]latest(?:@RajniiRobot)?$", incoming=True))
async def lates(event):
    mm = latest()
    buttons = [[Button.inline("Refresh", data="fk")]]
    await event.reply(
        f"Today's Schedule:\nTZ: Japan\n{mm}",
        buttons=buttons,
        link_preview=False,
    )


@telethn.on(events.CallbackQuery(pattern=r"^fk$"))
async def callbackk(event):
    if event.data.decode("utf-8") == "fk":
        mm = latest()

        try:
            buttons = [[Button.inline("Refresh", data="fk")]]
            await event.edit(
                f"Today's Schedule:\nTZ: Japan\n{mm}",
                buttons=buttons,
                link_preview=False,
            )
            await event.answer("Refreshed!")
        except Exception:
            await event.answer("Refreshed!")