import requests

from RajniiRobot import telethn
from RajniiRobot.utils.errors import capture_err
from telethon import events, Button


def ikb(data: dict, row_width: int = 2):
    """
    Converts a dict to telethon buttons
    Ex: dict_to_keyboard({"click here": "this is callback data"})
    """
    buttons = []
    current_row = []
    for text, url_or_data in data.items():
        if url_or_data.startswith("http://") or url_or_data.startswith("https://"):
            current_row.append(Button.url(text, url_or_data))
        else:
            current_row.append(Button.inline(text, url_or_data))
        
        if len(current_row) == row_width:
            buttons.append(current_row)
            current_row = []
    if current_row:
        buttons.append(current_row)
    return buttons


n = "\n"
w = " "

bold = lambda x: f"**{x}:** "
bold_ul = lambda x: f"**--{x}:**-- "

mono = lambda x: f"`{x}`{n}"


def section(
    title: str,
    body: dict,
    indent: int = 2,
    underline: bool = False,
) -> str:

    text = (bold_ul(title) + n) if underline else bold(title) + n

    for key, value in body.items():
        text += (indent * w + bold(key) +
                 ((value[0] + n) if isinstance(value, list) else mono(value)))
    return text


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]crypto$", incoming=True))
@capture_err
async def crypto(event):
    args = event.text.split(None, 1)
    if len(args) < 2:
        return await event.reply("/crypto `[currency]`")

    currency = args[1].lower()

    btn = ikb(
        {"Available Currencies": "https://plotcryptoprice.herokuapp.com"}, 
    )

    m = await event.reply("`Processing...`")

    try:
        response = requests.get(
            "https://x.wazirx.com/wazirx-falcon/api/v2.0/crypto_rates",
            timeout=5,
        )
        r = response.json()
    except Exception:
        return await m.edit("[ERROR]: Something went wrong.")

    if not isinstance(r, dict) or currency not in r:
        return await m.edit(
            "[ERROR]: INVALID CURRENCY",
            buttons=btn,
        )

    body = {i.upper(): j for i, j in r.get(currency).items()}

    text = section(f"Current Crypto Rates For {currency.upper()}", body)
    await m.edit(text, buttons=btn)