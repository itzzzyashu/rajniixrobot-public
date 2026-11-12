import requests
import asyncio
import io
import os
import random
import re
import string
import subprocess
import textwrap
import contextlib
import nltk

from random import randint, randrange, uniform
from cowpy import cow
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from telethon.tl.types import DocumentAttributeFilename, InputMessagesFilterDocument, InputMediaDice
from telethon import events
from zalgo_text import zalgo

from RajniiRobot.utils.errors import capture_err
from RajniiRobot.utils.carbon import make_carbon
from RajniiRobot.events import register
from RajniiRobot import telethn, ubot, TEMP_DOWNLOAD_DIRECTORY, SUPPORT_CHAT, LOGGER

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

WIDE_MAP = {i: i + 0xFEE0 for i in range(0x21, 0x7F)}
WIDE_MAP[0x20] = 0x3000


@telethn.on(events.NewMessage(pattern="^/news ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    infintyvar = event.pattern_match.group(1)
    main_url = f"https://inshortsapi.vercel.app/news?category={infintyvar}"
    stuber = await event.reply(
        f"Ok ! Fectching {infintyvar} From inshortsapi Server And Sending To News Channel",
    )
    await stuber.edit("All News Has Been Sucessfully fetched, sendning to you."
                      )
    starknews = requests.get(main_url).json()
    for item in starknews["data"]:
        sedlyf = item["content"]
        img = item["imageUrl"]
        writter = item["author"]
        dateis = item["date"]
        readthis = item["readMoreUrl"]
        titles = item["title"]
        sed1 = img
        sedm = f"**Title : {titles}** \n{sedlyf} \nDate : {dateis} \nAuthor : {writter} \nReadMore : {readthis}"
        await telethn.send_file(event.chat_id, sed1, caption=sedm)


@register(pattern="^/ball(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    inputstr = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice("🏀"))
    input_int = int(inputstr)
    if input_int > 5:
        await event.reply("hey nigga use number 1 to 6 only")

    else:
        with contextlib.suppress(BaseException):
            required_number = input_int
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))


@register(pattern="^/asupan ?(.*)")
async def asupan(event):
    try:
        resp = requests.get(
            "https://tede-api.herokuapp.com/api/asupan/ptl").json()
        asupannya = f"{resp['url']}"
        return await telethn.send_file(event.chat_id, asupannya)
    except Exception:
        await event.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/wibu ?(.*)")
async def wibu(event):
    try:
        resp = requests.get(
            "https://tede-api.herokuapp.com/api/asupan/wibu").json()
        wibunya = f"{resp['url']}"
        return await telethn.send_file(event.chat_id, wibunya)
    except Exception:
        await event.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/chika ?(.*)")
async def chika(event):
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/chika").json()
        chikanya = f"{resp['url']}"
        return await telethn.send_file(event.chat_id, chikanya)
    except Exception:
        await event.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/truth ?(.*)")
async def _(td):
    try:
        resp = requests.get("https://api.safone.tech/truth").json()
        results = f"{resp['truth']}"
        return await td.reply(results)
    except Exception:
        await td.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/dare ?(.*)")
async def _(dr):
    try:
        resp = requests.get("https://api.safone.tech/dare").json()
        results = f"{resp['dare']}"
        return await dr.reply(results)
    except Exception:
        await dr.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/fact ?(.*)")
async def _(dr):
    try:
        resp = requests.get("https://api.safone.tech/fact").json()
        results = f"{resp['fact']}"
        return await dr.reply(results)
    except Exception:
        await dr.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/quotes ?(.*)")
async def _(dr):
    try:
        resp = requests.get("https://api.safone.tech/quote").json()
        results = f"{resp['quote']}"
        return await dr.reply(results)
    except Exception:
        await dr.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/joke ?(.*)")
async def _(dr):
    try:
        resp = requests.get("https://api.safone.tech/joke").json()
        results = f"{resp['joke']}"
        return await dr.reply(results)
    except Exception:
        await dr.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/bully ?(.*)")
async def _(dr):
    try:
        resp = requests.get("https://api.safone.tech/bully").json()
        results = f"{resp['bully']}"
        return await dr.reply(results)
    except Exception:
        await dr.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/advice ?(.*)")
async def _(dr):
    try:
        resp = requests.get("https://api.safone.tech/advice").json()
        results = f"{resp['advice']}"
        return await dr.reply(results)
    except Exception:
        await dr.reply(f"Error Report @{SUPPORT_CHAT}")


@register(pattern="^/owu$")
async def msg(event):

    reply_tex = await event.get_reply_message()
    if not reply_tex or not reply_tex.text:
        await event.reply("Reply to a message to make meme.")
        return
    reply_text = reply_tex.text
    faces = [
        "(・`ω´・)",
        ";;w;;",
        "owo",
        "UwU",
        ">w<",
        "^w^",
        r"\(^o\) (/o^)/",
        "( ^ _ ^)∠☆",
        "(ô_ô)",
        "~:o",
        ";____;",
        "(*^*)",
        "(>_",
        "(♥_♥)",
        "*(^O^)*",
        "((+_+))",
    ]
    text = re.sub(r"[rl]", "w", reply_text)
    text = re.sub(r"[ｒｌ]", "ｗ", reply_text)
    text = re.sub(r"[RL]", "W", text)
    text = re.sub(r"[ＲＬ]", "Ｗ", text)
    text = re.sub(r"n([aeiouａｅｉｏｕ])", r"ny\1", text)
    text = re.sub(r"ｎ([ａｅｉｏｕ])", r"ｎｙ\1", text)
    text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", text)
    text = re.sub(r"Ｎ([ａｅｉｏｕＡＥＩＯＵ])", r"Ｎｙ\1", text)
    text = re.sub(r"\!+", f" {random.choice(faces)}", text)
    text = re.sub(r"！+", f" {random.choice(faces)}", text)
    text = text.replace("ove", "uv")
    text = text.replace("ｏｖｅ", "ｕｖ")
    text += f" {random.choice(faces)}"
    await event.reply(text)


@register(pattern="^/copypasta$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    rtext = rtex.text
    emojis = [
        "😂",
        "😂",
        "👌",
        "✌",
        "💞",
        "👍",
        "👌",
        "💯",
        "🎶",
        "👀",
        "😂",
        "👓",
        "👏",
        "👐",
        "🍕",
        "💥",
        "🍴",
        "💦",
        "💦",
        "🍑",
        "🍆",
        "😩",
        "😏",
        "👉👌",
        "👀",
        "👅",
        "😩",
        "🚰",
    ]
    reply_text = random.choice(emojis)
    b_char = random.choice(rtext).lower()
    for c in rtext:
        if c == " ":
            reply_text += random.choice(emojis)
        elif c in emojis:
            reply_text += c
            reply_text += random.choice(emojis)
        elif c.lower() == b_char:
            reply_text += "🅱️"
        else:
            reply_text += c.upper() if bool(
                random.getrandbits(1)) else c.lower()
    reply_text += random.choice(emojis)
    await event.reply(reply_text)


@register(pattern="^/bmoji$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    rtext = rtex.text
    b_char = random.choice(rtext).lower()
    reply_text = rtext.replace(b_char, "🅱️").replace(b_char.upper(), "🅱️")
    await event.reply(reply_text)


@register(pattern="^/clapmoji$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    rtext = rtex.text
    reply_text = "👏 "
    reply_text += rtext.replace(" ", " 👏 ")
    reply_text += " 👏"
    await event.reply(reply_text)


@register(pattern="^/stretch$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    rtext = rtex.text
    count = random.randint(3, 10)
    reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])", (r"\1" * count), rtext)
    await event.reply(reply_text)


@register(pattern="^/vapor(?: |$)(.*)")
async def msg(event):

    rtex = await event.get_reply_message()
    rtext = rtex.text if rtex else None
    data = rtext or event.pattern_match.group(1)
    if data is None:
        await event.reply("Either provide some input or reply to a message.")
        return

    reply_text = str(data).translate(WIDE_MAP)
    await event.reply(reply_text)


@register(pattern="^/zalgofy$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    rtext = rtex.text
    reply_text = zalgo.zalgo().zalgofy(rtext)
    await event.reply(reply_text)


@register(pattern="^/forbesify$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    data = rtex.text

    data = data.lower()
    accidentals = ["VB", "VBD", "VBG", "VBN"]
    reply_text = data.split()
    offset = 0

    tagged = dict(nltk.pos_tag(reply_text))

    for k in range(len(reply_text)):
        i = reply_text[k + offset]
        if tagged.get(i) in accidentals:
            reply_text.insert(k + offset, "accidentally")
            offset += 1

    reply_text = string.capwords(" ".join(reply_text))
    await event.reply(reply_text)


@register(pattern="^/angrymoji$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    rtext = rtex.text
    reply_text = "😡 "
    for i in rtext:
        reply_text += " 😡 " if i == " " else i
    reply_text += " 😡"
    await event.reply(reply_text)


@register(pattern="^/crymoji$")
async def msg(event):

    rtex = await event.get_reply_message()
    if not rtex or not rtex.text:
        await event.reply("Reply to a message to make meme.")
        return
    rtext = rtex.text
    reply_text = "😭 "
    for i in rtext:
        reply_text += " 😭 " if i == " " else i
    reply_text += " 😭"
    await event.reply(reply_text)


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]carbon$", incoming=True))
@capture_err
async def carbon_func(event):
    reply = await event.get_reply_message()
    if not reply or not reply.text:
        return await event.reply("Reply to a text message to make carbon.")
    m = await event.reply("Preparing Carbon.")
    carbon = await make_carbon(reply.text)
    await m.edit("Uploading...")
    await telethn.send_file(event.chat_id, carbon, file_name="carbon.png")
    await m.delete()
    carbon.close()


@register(pattern="^/deepfry(?: |$)(.*)")
async def deepfryer(event):

    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 1
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await event.reply("`I can't deep fry that!`")
            return
    else:
        await event.reply("`Reply to an image or sticker to deep fry it!`")
        return

    image = io.BytesIO()
    await telethn.download_media(data, image)
    image = Image.open(image)

    for _ in range(frycount):
        image = await deepfry(image)
    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)
    await event.reply(file=fried_io)


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )
    img = img.copy().convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width**uniform(0.8, 0.9)), int(height**uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width**uniform(0.85, 0.95)), int(height**uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width**uniform(0.89, 0.98)), int(height**uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageOps.colorize(overlay, colours[0], colours[1])
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))
    return img


async def check_media(reply_message):
    if not reply_message or not reply_message.media:
        return False
    if reply_message.photo:
        data = reply_message.photo
    elif reply_message.document:
        if (DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes):
            return False
        if (reply_message.gif or reply_message.video or reply_message.audio
                or reply_message.voice):
            return False
        data = reply_message.media.document
    else:
        return False
    if not data or data is None:
        return False
    return data


@register(pattern="^/type (.*)")
async def typewriter(typew):

    message = typew.pattern_match.group(1)
    if not message:
        await typew.reply("`Give a text to type!`")
        return
    typing_symbol = "|"
    old_text = ""
    now = await typew.reply(typing_symbol)
    await asyncio.sleep(2)
    for character in message:
        old_text = f"{old_text}{character}"
        typing_text = f"{old_text}{typing_symbol}"
        await now.edit(typing_text)
        await asyncio.sleep(2)
        await now.edit(old_text)
        await asyncio.sleep(2)


@register(pattern="^/sticklet (.*)")
async def sticklet(event):

    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)

    sticktext = event.pattern_match.group(1)

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = "\n".join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = await get_font_file(ubot, "@IndianBot_Fonts")

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512 - width) / 2, (512 - height) / 2),
                        sticktext,
                        font=font,
                        fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "@Julia.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.reply(file=image_stream,
                      reply_to=event.message.reply_to_msg_id)

    with contextlib.suppress(BaseException):
        os.remove(FONT_FILE)


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)
    return await client.download_media(font_file_message)


@register(pattern=r"^/(\w+)say (.*)")
async def univsaye(cowmsg):
    """For .cowsay module, uniborg wrapper for cow which says things."""
    if cowmsg.text[0].isalpha() or cowmsg.text[0] in ("#", "@"):
        return

    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.reply(f"`{cheese.milk(text).replace('`', '´')}`")


@register(pattern="^/basketball$")
async def _(event):
    if event.fwd_from:
        return

    input_str = LOGGER.debug(randrange(6))
    r = await event.reply(file=InputMediaDice("🏀"))
    if input_str:
        with contextlib.suppress(BaseException):
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🏀"))


@register(pattern="^/jackpot$")
async def _(event):
    if event.fwd_from:
        return

    await event.reply(file=InputMediaDice("🎰"))


@register(pattern="^/dart(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice("🎯"))
    input_int = int(input_str)
    if input_int > 6:
        await event.reply("hey nigga use number 1 to 6 only")

    else:
        with contextlib.suppress(BaseException):
            required_number = input_int
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice("🎯"))


COLORS = [
    "#F07975",
    "#F49F69",
    "#F9C84A",
    "#8CC56E",
    "#6CC7DC",
    "#80C1FA",
    "#BCB3F9",
    "#E181AC",
]

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+")


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


@register(pattern="^/animate (.*)")
async def stickerizer(event):

    newtext = event.pattern_match.group(1)
    animus = [20, 32, 33, 40, 41, 42, 58]
    sticcers = await ubot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(newtext))}")
    null = await sticcers[0].download_media(TEMP_DOWNLOAD_DIRECTORY)
    bara = str(null)
    await event.client.send_file(event.chat_id, bara, reply_to=event.id)
    os.remove(bara)


@register(pattern="^/dice(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice(""))
    input_int = int(input_str)
    if input_int > 6:
        await event.reply("hey nigga use number 1 to 6 only")

    else:
        with contextlib.suppress(BaseException):
            required_number = input_int
            while r.media.value != required_number:
                await r.delete()
                r = await event.reply(file=InputMediaDice(""))


@register(pattern="^/fortune$")
async def fortunate(event):
    if event.fwd_from:
        return

    jit = subprocess.check_output(["python", "fortune.py"])
    pit = jit.decode()
    await event.reply(pit)


ABUSE_STRINGS = (
    "Fuck off",
    "Stfu go fuck yourself",
    "Ur mum gey",
    "Ur dad lesbo",
    "You Assfucker",
    "Nigga",
    "Ur granny tranny",
    "you noob",
    "Relax your Rear,ders nothing to fear,The Rape train is finally here",
    "Stfu bc",
    "Stfu and Gtfo U nub",
    "GTFO bsdk",
    "CUnt",
    "Madharchod",
    " Gay is here",
    "Ur dad gey bc ",
)

EYES = [
    ["⌐■", "■"],
    [" ͠°", " °"],
    ["⇀", "↼"],
    ["´• ", " •`"],
    ["´", "`"],
    ["`", "´"],
    ["ó", "ò"],
    ["ò", "ó"],
    ["⸌", "⸍"],
    [">", "<"],
    ["Ƹ̵̡", "Ʒ"],
    ["ᗒ", "ᗕ"],
    ["⟃", "⟄"],
    ["⪧", "⪦"],
    ["⪦", "⪧"],
    ["⪩", "⪨"],
    ["⪨", "⪩"],
    ["⪰", "⪯"],
    ["⫑", "⫒"],
    ["⨴", "⨵"],
    ["⩿", "⪀"],
    ["⩾", "⩽"],
    ["⩺", "⩹"],
    ["⩹", "⩺"],
    ["◥▶", "◀◤"],
    ["◍", "◎"],
    ["/͠-", "┐͡-\\"],
    ["⌣", "⌣”"],
    [" ͡⎚", " ͡⎚"],
    ["≋"],
    ["૦ઁ"],
    ["  ͯ"],
    ["  ͌"],
    ["ළ"],
    ["◉"],
    ["☉"],
    ["・"],
    ["▰"],
    ["ᵔ"],
    [" ﾟ"],
    ["□"],
    ["☼"],
    ["*"],
    ["`"],
    ["⚆"],
    ["⊜"],
    [">"],
    ["❍"],
    ["￣"],
    ["─"],
    ["✿"],
    ["•"],
    ["T"],
    ["^"],
    ["ⱺ"],
    ["@"],
    ["ȍ"],
    ["  "],
    ["  "],
    ["x"],
    ["-"],
    ["$"],
    ["Ȍ"],
    ["ʘ"],
    ["Ꝋ"],
    [""],
    ["⸟"],
    ["๏"],
    ["ⴲ"],
    ["◕"],
    ["◔"],
    ["✧"],
    ["■"],
    ["♥"],
    [" ͡°"],
    ["¬"],
    [" º "],
    ["⨶"],
    ["⨱"],
    ["⏓"],
    ["⏒"],
    ["⍜"],
    ["⍤"],
    ["ᚖ"],
    ["ᴗ"],
    ["ಠ"],
    ["σ"],
    ["☯"],
]

MOUTHS = [
    ["v"],
    ["ᴥ"],
    ["ᗝ"],
    ["Ѡ"],
    ["ᗜ"],
    ["Ꮂ"],
    ["ᨓ"],
    ["ᨎ"],
    ["ヮ"],
    ["╭͜ʖ╮"],
    [" ͟ل͜"],
    [" ͜ʖ"],
    [" ͟ʖ"],
    [" ʖ̯"],
    ["ω"],
    [" ³"],
    [" ε "],
    ["﹏"],
    ["□"],
    ["ل͜"],
    ["‿"],
    ["╭╮"],
    ["‿‿"],
    ["▾"],
    ["‸"],
    ["Д"],
    ["∀"],
    ["!"],
    ["人"],
    ["."],
    ["ロ"],
    ["_"],
    ["෴"],
    ["ѽ"],
    ["ഌ"],
    ["⏠"],
    ["⏏"],
    ["⍊"],
    ["⍘"],
    ["ツ"],
    ["益"],
    ["╭∩╮"],
    ["Ĺ̯"],
    ["◡"],
    [" ͜つ"],
]

EARS = [
    ["q", "p"],
    ["ʢ", "ʡ"],
    ["⸮", "?"],
    ["ʕ", "ʔ"],
    ["ᖗ", "ᖘ"],
    ["ᕦ", "ᕥ"],
    ["ᕦ(", ")ᕥ"],
    ["ᕙ(", ")ᕗ"],
    ["ᘳ", "ᘰ"],
    ["ᕮ", "ᕭ"],
    ["ᕳ", "ᕲ"],
    ["(", ")"],
    ["[", "]"],
    ["¯\\_", "_/¯"],
    ["୧", "୨"],
    ["୨", "୧"],
    ["⤜(", ")⤏"],
    ["☞", "☞"],
    ["ᑫ", "ᑷ"],
    ["ᑴ", "ᑷ"],
    ["ヽ(", ")ﾉ"],
    ["\\(", ")/"],
    ["乁(", ")ㄏ"],
    ["└[", "]┘"],
    ["(づ", ")づ"],
    ["(ง", ")ง"],
    ["⎝", "⎠"],
    ["ლ(", "ლ)"],
    ["ᕕ(", ")ᕗ"],
    ["(∩", ")⊃━☆ﾟ.*"],
]

SFW_STRINGS = (
    "Owww ... Such a stupid idiot.",
    "Don't drink and type.",
    "I think you should go home or better a mental asylum.",
    "Command not found. Just like your brain.",
    "Do you realize you are making a fool of yourself? Apparently not.",
    "You can type better than that.",
    "Bot rule 544 section 9 prevents me from replying to stupid humans like you.",
    "Sorry, we do not sell brains.",
    "Believe me you are not normal.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
    "Zombies eat brains... you're safe.",
    "You didn't evolve from apes, they evolved from you.",
    "Come back and talk to me when your I.Q. exceeds your age.",
    "I'm not saying you're stupid, I'm just saying you've got bad luck when it comes to thinking.",
    "What language are you speaking? Cause it sounds like bullshit.",
    "Stupidity is not a crime so you are free to go.",
    "You are proof that evolution CAN go in reverse.",
    "I would ask you how old you are but I know you can't count that high.",
    "As an outsider, what do you think of the human race?",
    "Brains aren't everything. In your case they're nothing.",
    "Ordinarily people live and learn. You just live.",
    "I don't know what makes you so stupid, but it really works.",
    "Keep talking, someday you'll say something intelligent! (I doubt it though)",
    "Shock me, say something intelligent.",
    "Your IQ's lower than your shoe size.",
    "Alas! Your neurotransmitters are no more working.",
    "Are you crazy you fool.",
    "Everyone has the right to be stupid but you are abusing the privilege.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.",
    "You should try tasting cyanide.",
    "Your enzymes are meant to digest rat poison.",
    "You should try sleeping forever.",
    "Pick up a gun and shoot yourself.",
    "You could make a world record by jumping from a plane without parachute.",
    "Stop talking BS and jump in front of a running bullet train.",
    "Try bathing with Hydrochloric Acid instead of water.",
    "Try this: if you hold your breath underwater for an hour, you can then hold it forever.",
    "Go Green! Stop inhaling Oxygen.",
    "God was searching for you. You should leave to meet him.",
    "give your 100%. Now, go donate blood.",
    "Try jumping from a hundred story building but you can do it only once.",
    "You should donate your brain seeing that you never used it.",
    "Volunteer for target in an firing range.",
    "Head shots are fun. Get yourself one.",
    "You should try swimming with great white sharks.",
    "You should paint yourself red and run in a bull marathon.",
    "You can stay underwater for the rest of your life without coming back up.",
    "How about you stop breathing for like 1 day? That'll be great.",
    "Try provoking a tiger while you both are in a cage.",
    "Have you tried shooting yourself as high as 100m using a canon.",
    "You should try holding TNT in your mouth and igniting it.",
    "Try playing catch and throw with RDX its fun.",
    "I heard phogine is poisonous but i guess you wont mind inhaling it for fun.",
    "Launch yourself into outer space while forgetting oxygen on Earth.",
    "You should try playing snake and ladders, with real snakes and no ladders.",
    "Dance naked on a couple of HT wires.",
    "Active Volcano is the best swimming pool for you.",
    "You should try hot bath in a volcano.",
    "Try to spend one day in a coffin and it will be yours forever.",
    "Hit Uranium with a slow moving neutron in your presence. It will be a worthwhile experience.",
    "You can be the first person to step on sun. Have a try.",
    "People like you are the reason we have middle fingers.",
    "When your mom dropped you off at the school, she got a ticket for littering.",
    "You’re so ugly that when you cry, the tears roll down the back of your head…just to avoid your face.",
    "If you’re talking behind my back then you’re in a perfect position to kiss my a**!.",
    "Stupidity is not a crime so you are free to go.",
)


@register(pattern="^/insult$")
async def _(event):

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        replyto = reply.sender_id
    else:
        replyto = event.sender_id
    await telethn.send_message(event.chat_id,
                               random.choice(SFW_STRINGS),
                               reply_to=replyto)


reactionhappy = [
    "''̵͇З= ( ▀ ͜͞ʖ▀) =Ε/̵͇/’’",
    "ʕ•ᴥ•ʔ",
    "(づ｡◕‿‿◕｡)づ",
    "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ)",
    "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
    "(☞ﾟ∀ﾟ)☞",
    "| (• ◡•)| (❍ᴥ❍Ʋ)",
    "(◕‿◕✿)",
    "(ᵔᴥᵔ)",
    "(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)",
    "(づ￣ ³￣)づ",
    "♪~ ᕕ(ᐛ)ᕗ",
    "♥️‿♥️",
    "༼ つ ͡° ͜ʖ ͡° ༽つ",
    "༼ つ ಥ_ಥ ༽つ",
    "ヾ(⌐■_■)ノ♪",
    "~(˘▾˘~)",
    "◉_◉",
    "(•◡•) /",
    "(~˘▾˘)~",
    "(｡◕‿‿◕｡)",
    "☜(˚▽˚)☞",
    "(•Ω•)",
    "(｡◕‿◕｡)",
    "(っ˘ڡ˘Σ)",
    "｡◕‿‿◕｡",
    "☜(⌒▽⌒)☞",
    "｡◕‿◕｡",
    "(ღ˘⌣˘ღ)",
    "(▰˘◡˘▰)",
    "^̮^",
    "^̮^",
    ">_>",
    "(^̮^)",
    "^̮^",
    "^̮^",
]
reactionangry = [
    "▄︻̷┻═━一",
    "(▀Ĺ̯▀ )",
    "(ง ͠° ͟ل͜ ͡°)ง",
    "༼ つ ◕_◕ ༽つ",
    "ಠ_ಠ",
    "''̵͇З=( ͠° ͟ʖ ͡°)=Ε/̵͇/'",
    "(ง'̀-'́)ง",
    "(ノಠ益ಠ)ノ彡┻━┻",
    "(╯°□°)╯︵ ꞰOOQƎƆⱯɟ",
    "ლ(ಠ益ಠლ)",
    "ಠ╭╮ಠ",
    "''̵͇З=(•_•)=Ε/̵͇/''",
    "(╯°□°）╯︵ ┻━┻",
    "┻━┻ ︵ヽ(Д´)ﾉ︵ ┻━┻",
    "⌐╦╦═─",
    "（╯°□°）╯︵( .O.)",
    ":')",
    "┬──┬ ノ( ゜-゜ノ)",
    "ლ(´ڡლ)",
    "(°ロ°)☝️",
    "ლ,ᔑ•ﺪ͟͠•ᔐ.ლ",
    "┬─┬ノ( º _ ºノ)",
    "┬─┬﻿ ︵ /(.□. ）",
]

reactions = [
    "( ͡° ͜ʖ ͡°)",
    "( . •́ _ʖ •̀ .)",
    "( ಠ ͜ʖ ಠ)",
    "( ͡ ͜ʖ ͡ )",
    "(ʘ ͜ʖ ʘ)",
    "ヾ(´〇`)ﾉ♪♪♪",
    "ヽ(o´∀`)ﾉ♪♬",
    "♪♬((d⌒ω⌒b))♬♪",
    "└(＾＾)┐",
    "(￣▽￣)/♫•*¨*•.¸¸♪",
    "ヾ(⌐■_■)ノ♪",
    "乁( • ω •乁)",
    "♬♫♪◖(● o ●)◗♪♫♬",
    "(っ˘ڡ˘ς)",
    "( ˘▽˘)っ♨",
    "( ・ω・)⊃-[二二]",
    "(*´ー`)旦 旦(￣ω￣*)",
    "( ￣▽￣)[] [](≧▽≦ )",
    "(*￣▽￣)旦 且(´∀`*)",
    "(ノ ˘_˘)ノ ζ|||ζ ζ|||ζ ζ|||ζ",
    "(ノ°∀°)ノ⌒･*:.｡. .｡.:*･゜ﾟ･*☆",
    "(⊃｡•́‿•̀｡)⊃━✿✿✿✿✿✿",
    "(∩` ﾛ ´)⊃━炎炎炎炎炎",
    "( ・∀・)・・・--------☆",
    "( -ω-)／占~~~~~",
    "○∞∞∞∞ヽ(^ー^ )",
    "(*＾＾)/~~~~~~~~~~◎",
    "((( ￣□)_／",
    "(ﾒ￣▽￣)︻┳═一",
    "ヽ( ･∀･)ﾉ_θ彡☆Σ(ノ `Д´)ノ",
    "(*`0´)θ☆(メ°皿°)ﾉ",
    "(; -_-)――――――C<―_-)",
    "ヽ(>_<ヽ) ―⊂|=0ヘ(^‿^ )",
    "(҂` ﾛ ´)︻デ═一 ＼(º □ º l|l)/",
    "/( .□.)＼ ︵╰(°益°)╯︵ /(.□. /)",
    "(`⌒*)O-(`⌒´Q)",
    "(っ•﹏•)っ ✴==≡눈٩(`皿´҂)ง",
    "ヾ(・ω・)メ(・ω・)ノ",
    "(*^ω^)八(⌒▽⌒)八(-‿‿- )ヽ",
    "ヽ( ⌒ω⌒)人(=^‥^= )ﾉ",
    "｡*:☆(・ω・人・ω・)｡:゜☆｡",
    "(°(°ω(°ω°(☆ω☆)°ω°)ω°)°)",
    "(っ˘▽˘)(˘▽˘)˘▽˘ς)",
    "(*＾ω＾)人(＾ω＾*)",
    r"＼(▽￣ \ (￣▽￣) / ￣▽)／",
    "(￣Θ￣)",
    "＼( ˋ Θ ´ )／",
    "( ´(00)ˋ )",
    "＼(￣(oo)￣)／",
    "／(≧ x ≦)＼",
    "／(=･ x ･=)＼",
    "(=^･ω･^=)",
    "(= ; ｪ ; =)",
    "(=⌒‿‿⌒=)",
    "(＾• ω •＾)",
    "ଲ(ⓛ ω ⓛ)ଲ",
    "ଲ(ⓛ ω ⓛ)ଲ",
    "(^◔ᴥ◔^)",
    "[(－－)]..zzZ",
    "(￣o￣) zzZZzzZZ",
    "(＿ ＿*) Z z z",
    "☆ﾐ(o*･ω･)ﾉ",
    "ε=ε=ε=ε=┌(;￣▽￣)┘",
    "ε===(っ≧ω≦)っ",
    "__φ(．．)",
    "ヾ( `ー´)シφ__",
    "( ^▽^)ψ__",
    "|･ω･)",
    "|д･)",
    "┬┴┬┴┤･ω･)ﾉ",
    "|･д･)ﾉ",
    "(*￣ii￣)",
    "(＾〃＾)",
    "m(_ _)m",
    "人(_ _*)",
    "(シ. .)シ",
    "(^_~)",
    "(>ω^)",
    "(^_<)〜☆",
    "(^_<)",
    "(づ￣ ³￣)づ",
    "(⊃｡•́‿•̀｡)⊃",
    "⊂(´• ω •`⊂)",
    "(*・ω・)ﾉ",
    "(^-^*)/",
    "ヾ(*'▽'*)",
    "(^０^)ノ",
    "(*°ｰ°)ﾉ",
    "(￣ω￣)/",
    "(≧▽≦)/",
    "w(°ｏ°)w",
    "(⊙_⊙)",
    "(°ロ°) !",
    "∑(O_O;)",
    "(￢_￢)",
    "(¬_¬ )",
    "(↼_↼)",
    "(￣ω￣;)",
    "┐('～`;)┌",
    "(・_・;)",
    "(＠_＠)",
    "(•ิ_•ิ)?",
    "ヽ(ー_ー )ノ",
    "┐(￣ヘ￣)┌",
    "┐(￣～￣)┌",
    "┐( ´ д ` )┌",
    "╮(︶▽︶)╭",
    "ᕕ( ᐛ )ᕗ",
    "(ノωヽ)",
    "(″ロ゛)",
    "(/ω＼)",
    "(((＞＜)))",
    "~(>_<~)",
    "(×_×)",
    "(×﹏×)",
    "(ノ_<。)",
    "(μ_μ)",
    "o(TヘTo)",
    "( ﾟ，_ゝ｀)",
    "( ╥ω╥ )",
    "(／ˍ・、)",
    "(つω`｡)",
    "(T_T)",
    "o(〒﹏〒)o",
    "(＃`Д´)",
    "(・`ω´・)",
    "( `ε´ )",
    "(ﾒ` ﾛ ´)",
    "Σ(▼□▼メ)",
    "(҂ `з´ )",
    "٩(╬ʘ益ʘ╬)۶",
    "↑_(ΦwΦ)Ψ",
    "(ﾉಥ益ಥ)ﾉ",
    "(＃＞＜)",
    "(；￣Д￣)",
    "(￢_￢;)",
    "(＾＾＃)",
    "(￣︿￣)",
    "ヾ( ￣O￣)ツ",
    "(ᗒᗣᗕ)՞",
    "(ノ_<。)ヾ(´ ▽ ` )",
    "ヽ(￣ω￣(。。 )ゝ",
    "(ﾉ_；)ヾ(´ ∀ ` )",
    "(´-ω-`( _ _ )",
    "(⌒_⌒;)",
    "(*/_＼)",
    "( ◡‿◡ *)",
    "(//ω//)",
    "(￣▽￣*)ゞ",
    "(„ಡωಡ„)",
    "(ﾉ´ з `)ノ",
    "(♡-_-♡)",
    "(─‿‿─)♡",
    "(´ ω `♡)",
    "(ღ˘⌣˘ღ)",
    "(´• ω •`) ♡",
    "╰(*´︶`*)╯♡",
    "(≧◡≦) ♡",
    "♡ (˘▽˘>ԅ( ˘⌣˘)",
    "σ(≧ε≦σ) ♡",
    "(˘∀˘)/(μ‿μ) ❤",
    "Σ>―(〃°ω°〃)♡→",
    "(* ^ ω ^)",
    "(o^▽^o)",
    "ヽ(・∀・)ﾉ",
    "(o･ω･o)",
    "(^人^)",
    "( ´ ω ` )",
    "(´• ω •`)",
    "╰(▔∀▔)╯",
    "(✯◡✯)",
    "(⌒‿⌒)",
    "(*°▽°*)",
    "(´｡• ᵕ •｡`)",
    "ヽ(>∀<☆)ノ",
    "＼(￣▽￣)／",
    "(o˘◡˘o)",
    "(╯✧▽✧)╯",
    "( ‾́ ◡ ‾́ )",
    "(๑˘︶˘๑)",
    "(´･ᴗ･ ` )",
    "( ͡° ʖ̯ ͡°)",
    "( ఠ ͟ʖ ఠ)",
    "( ಥ ʖ̯ ಥ)",
    "(≖ ͜ʖ≖)",
    "ヘ(￣ω￣ヘ)",
    "(ﾉ≧∀≦)ﾉ",
    "└(￣-￣└))",
    "┌(＾＾)┘",
    "(^_^♪)",
    "(〜￣△￣)〜",
    "(｢• ω •)｢",
    "( ˘ ɜ˘) ♬♪♫",
    "( o˘◡˘o) ┌iii┐",
    "♨o(>_<)o♨",
    "( ・・)つ―{}@{}@{}-",
    "(*´з`)口ﾟ｡ﾟ口(・∀・ )",
    "( *^^)o∀*∀o(^^* )",
    "-●●●-ｃ(・・ )",
    "(ﾉ≧∀≦)ﾉ ‥…━━━★",
    "╰( ͡° ͜ʖ ͡° )つ──☆*:・ﾟ",
    "(∩ᄑ_ᄑ)⊃━☆ﾟ*･｡*･:≡( ε:)",
]


@register(pattern="^/react$")
async def _(event):

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        replyto = reply.sender_id
    else:
        replyto = event.sender_id
    react = random.choice(reactions)
    await event.reply(react, reply_to=replyto)


@register(pattern="^/rhappy$")
async def _(event):

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        replyto = reply.sender_id
    else:
        replyto = event.sender_id
    rhappy = random.choice(reactionhappy)
    await event.reply(rhappy, reply_to=replyto)


@register(pattern="^/rangry$")
async def _(event):

    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        replyto = reply.sender_id
    else:
        replyto = event.sender_id
    rangry = random.choice(reactionangry)
    await event.reply(rangry, reply_to=replyto)


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")