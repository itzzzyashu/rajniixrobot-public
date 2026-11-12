import contextlib
import socket
import json
import sys
from random import randint
from time import time

import aiohttp
from googletrans import Translator
from motor import version as mongover
from pykeyboard import InlineKeyboard
from telethon import __version__ as telever
from telethon.tl.types import (
    InputBotInlineResult,
    InputBotInlineResultPhoto,
    InputTextFormatted,
)
from telethon.tl.custom import Button
from search_engine_parser import GoogleSearch

from RajniiRobot import OWNER_ID, telethn, arq, RAJNI_PTB, BOT_NAME, BOT_USERNAME
from RajniiRobot.utils.pluginhelpers import convert_seconds_to_minutes as time_convert
from RajniiRobot.utils.pluginhelpers import fetch

SUDOERS = OWNER_ID
app = telethn


async def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste(content):
    link = await _netcat("ezup.dev", 9999, content)
    return link


async def inline_help_func(__HELP__):
    buttons = [
        [
            Button.url("Explore Help", f"https://telegram.dog/{BOT_USERNAME}?start=start"),
            Button.switch_inline("Go Inline", "", current_switch=True),
        ]
    ]
    answerss = [
        app.builder.article(
            title="Inline Commands",
            description="Help Related To Inline Usage.",
            text=__HELP__,
            thumb="https://telegra.ph/file/ad9d8a4adb866d62c501f.png",
            buttons=buttons,
        )
    ]
    answerss = await alive_function(answerss)
    return answerss


async def alive_function(answers):
    bot_state = "Alive"
    try:
        me = await app.get_me()
        if not me:
            bot_state = "Dead"
    except Exception:
        bot_state = "Dead"

    buttons = [
        [
            Button.url("Main Service", f"https://telegram.dog/{BOT_USERNAME}"),
            Button.switch_inline("Go Inline!", "", current_switch=True),
        ]
    ]

    msg = f"""
**[{BOT_NAME}](https://github.com/Awesome-RJ/{BOT_USERNAME}):**

**MainBot:** `{bot_state}`
**UserBot:** `Alive`
**Python Version:** `v3.10.6`
**Telethon Version:** `{telever}`
**MongoDB Version:** `{mongover}`
**Platform:** `{sys.platform}`

**Profiles:** [{BOT_NAME}](https://telegram.dog/{BOT_USERNAME}) | [Userbot](https://telegram.dog/iKeshavVirmani)
"""
    answers.append(
        app.builder.article(
            title="Alive",
            description="Check Bot's Stats",
            thumb="https://telegra.ph/file/0d42f41c08e511b557ecc.png",
            text=msg,
            link_preview=False,
            buttons=buttons,
        ))
    return answers


async def webss(url):
    start_time = time()
    if "." not in url:
        return
    screenshot = await fetch(f"https://patheticprogrammers.cf/ss?site={url}")
    end_time = time()
    
    a = []
    pic = app.builder.photo(
        file=screenshot["url"],
        text=f"`{url}`\n__Took {round(end_time - start_time)} Seconds.__",
    )
    a.append(pic)
    return a


async def translate_func(answers, lang, tex):
    i = Translator().translate(tex, dest=lang)
    msg = f"""
__**Translated from {i.src} to {lang}**__
**INPUT:**
{tex}
**OUTPUT:**
{i.text}"""
    answers.extend([
        app.builder.article(
            title=f"Translated from {i.src} to {lang}.",
            description=i.text,
            text=msg,
        ),
        app.builder.article(
            title=i.text,
            text=i.text
        ),
    ])
    return answers


async def urban_func(answers, text):
    results = await arq.urbandict(text)
    if not results.ok:
        answers.append(
            app.builder.article(
                title="Error",
                description=results.result,
                text=results.result,
            ))
        return answers
    results = results.result
    limit = 0
    for i in results:
        if limit > 48:
            break
        limit += 1
        msg = f"""
**Query:** {text}
**Definition:** __{i.definition}__
**Example:** __{i.example}__"""

        answers.append(
            app.builder.article(
                title=i.word,
                description=i.definition,
                text=msg,
            ))
    return answers


async def google_search_func(answers, text):
    gresults = await GoogleSearch().async_search(text)
    limit = 0
    for i in gresults:
        if limit > 48:
            break
        limit += 1

        with contextlib.suppress(KeyError):
            msg = f"""
[{i["titles"]}]({i["links"]})
{i["descriptions"]}"""

            answers.append(
                app.builder.article(
                    title=i["titles"],
                    description=i["descriptions"],
                    text=msg,
                    link_preview=False,
                ))
    return answers


async def wall_func(answers, text):
    results = await arq.wall(text)
    if not results.ok:
        answers.append(
            app.builder.article(
                title="Error",
                description=results.result,
                text=results.result,
            ))
        return answers
    limit = 0
    results = results.result
    for i in results:
        if limit > 48:
            break
        limit += 1
        answers.append(
            app.builder.photo(
                file=i.url_image,
                text=f"[Source]({i.url_image})",
            ))
    return answers


async def saavn_func(answers, text):
    results = await arq.saavn(text)
    if not results.ok:
        answers.append(
            app.builder.article(
                title="Error",
                description=results.result,
                text=results.result,
            ))
        return answers
    results = results.result
    for i in results:
        buttons = [
            [Button.url("Download | Play", i.media_url)]
        ]
        duration = await time_convert(i.duration)
        caption = f"""
**Title:** {i.song}
**Album:** {i.album}
**Duration:** {duration}
**Release:** {i.year}
**Singers:** {i.singers}"""
        description = f"{i.album} | {duration} " + f"| {i.singers} ({i.year})"
        answers.append(
            app.builder.article(
                title=i.song,
                text=caption,
                link_preview=False,
                description=description,
                thumb=i.image,
                buttons=buttons,
            ))
    return answers


async def paste_func(answers, text):
    start_time = time()
    url = await paste(text)
    msg = f"__**{url}**__"
    end_time = time()
    answers.append(
        app.builder.article(
            title=f"Pasted In {round(end_time - start_time)} Seconds.",
            description=url,
            text=msg,
        ))
    return answers


async def deezer_func(answers, text):
    results = await arq.deezer(text, 5)
    if not results.ok:
        answers.append(
            app.builder.article(
                title="Error",
                description=results.result,
                text=results.result,
            ))
        return answers
    results = results.result
    for i in results:
        buttons = [
            [Button.url("Download | Play", i.url)]
        ]
        duration = await time_convert(i.duration)
        caption = f"""
**Title:** {i.title}
**Artist:** {i.artist}
**Duration:** {duration}
**Source:** [Deezer]({i.source})"""
        description = f"{i.artist} | {duration}"
        answers.append(
            app.builder.article(
                title=i.title,
                thumb=i.thumbnail,
                description=description,
                text=caption,
                link_preview=False,
                buttons=buttons,
            ))
    return answers


async def shortify(url):
    if "." not in url:
        return
    header = {
        "Authorization": "Bearer ad39983fa42d0b19e4534f33671629a4940298dc",
        "Content-Type": "application/json",
    }
    payload = {"long_url": f"{url}"}
    payload = json.dumps(payload)
    async with aiohttp.ClientSession() as session, session.post(
            "https://api-ssl.bitly.com/v4/shorten", headers=header,
            data=payload) as resp:
        data = await resp.json()
    msg = data["link"]
    a = []
    b = app.builder.article(
        title="Link Shortened!",
        description=data["link"],
        text=msg,
        link_preview=False,
    )
    a.append(b)
    return a


async def torrent_func(answers, text):
    results = await arq.torrent(text)
    if not results.ok:
        answers.append(
            app.builder.article(
                title="Error",
                description=results.result,
                text=results.result,
            ))
        return answers
    limit = 0
    results = results.result
    for i in results:
        if limit > 48:
            break
        title = i.name
        size = i.size
        seeds = i.seeds
        leechs = i.leechs
        upload_date = i.uploaded + " Ago"
        magnet = i.magnet
        caption = f"""
**Title:** __{title}__
**Size:** __{size}__
**Seeds:** __{seeds}__
**Leechs:** __{leechs}__
**Uploaded:** __{upload_date}__
**Magnet:** `{magnet}`"""

        description = f"{size} | {upload_date} | Seeds: {seeds}"
        answers.append(
            app.builder.article(
                title=title,
                description=description,
                text=caption,
                link_preview=False,
            ))
        limit += 1
    return answers


async def wiki_func(answers, text):
    data = await arq.wiki(text)
    if not data.ok:
        answers.append(
            app.builder.article(
                title="Error",
                description=data.result,
                text=data.result,
            ))
        return answers
    data = data.result
    msg = f"""
**QUERY:**
{data.title}
**ANSWER:**
__{data.answer}__"""
    answers.append(
        app.builder.article(
            title=data.title,
            description=data.answer,
            text=msg,
        ))
    return answers


async def ping_func(answers):
    t1 = time()
    # Telethon client ping equivalent check or time difference
    await app.get_me()
    t2 = time()
    ping = f"{round(t2 - t1, 2)} Seconds"
    answers.append(
        app.builder.article(
            title=ping,
            text=f"__**{ping}**__"))
    return answers


async def pokedexinfo(answers, pokemon):
    Pokemon = f"https://some-random-api.ml/pokedex?pokemon={pokemon}"
    result = await fetch(Pokemon)
    buttons = [
        [Button.switch_inline("Pokedex", "pokedex", current_switch=True)]
    ]
    caption = f"""
**Pokemon:** `{result["name"]}`
**Pokedex:** `{result["id"]}`
**Type:** `{result["type"]}`
**Abilities:** `{result["abilities"]}`
**Height:** `{result["height"]}`
**Weight:** `{result["weight"]}`
**Gender:** `{result["gender"]}`
**Stats:** `{result["stats"]}`
**Description:** `{result["description"]}`"""
    answers.append(
        app.builder.photo(
            file=f"https://img.pokemondb.net/artwork/large/{pokemon}.jpg",
            text=caption,
            buttons=buttons,
        ))
    return answers