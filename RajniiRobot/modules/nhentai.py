import requests

from telethon import events, Button

from RajniiRobot import telethn, telegraph
from RajniiRobot.utils.errors import capture_err


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]nhentai(?:\s+(.*))?$", incoming=True))
@capture_err
async def nhentai(event):
    if event.is_private:
        return
    args = event.text.split(None, 1)
    if len(args) < 2:
        return await event.reply("/nhentai `[code]`")
        
    query = args[1]
    title, tags, artist, total_pages, post_url, cover_image = nhentai_data(
        query)
    
    buttons = [[Button.url("Read Here", url=post_url)]]
    await event.reply(
        f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        buttons=buttons,
        parse_mode="html",
        link_preview=False,
    )


def nhentai_data(noombers):
    url = f"https://nhentai.net/api/gallery/{noombers}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res["num_pages"]
    extensions = {"j": "jpg", "p": "png", "g": "gif"}
    for i, x in enumerate(pages):
        media_id = res["media_id"]
        temp = x["t"]
        file = f"{i+1}.{extensions[temp]}"
        link = f"https://i.nhentai.net/galleries/{media_id}/{file}"
        links.append(link)

    for i in info:
        if i["type"] == "tag":
            tag = i["name"]
            tag = tag.split(" ")
            tag = "_".join(tag)
            tags += f"#{tag} "
        if i["type"] == "artist":
            artist = f"{i['name']} "

    post_content = "".join(f"<img src={link}><br>" for link in links)

    post = telegraph.create_page(
        f"{title}",
        html_content=post_content,
        author_name="@RajniiRobot",
        author_url="https://telegram.dog/RajniiRobot")
    return title, tags, artist, total_pages, post["url"], links[0]