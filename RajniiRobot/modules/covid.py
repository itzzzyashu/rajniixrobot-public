import requests
import json
import datetime

from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode

from RajniiRobot import RAJNI_PTB
from RajniiRobot.modules.disable import DisableAbleCommandHandler


async def dot(number, thousand_separator="."):

    def reverse(string):
        string = "".join(reversed(string))
        return string

    s = reverse(str(number))
    count = 0
    result = ""
    for char in s:
        count = count + 1
        if count % 3 == 0:
            if len(s) == count:
                result = char + result
            else:
                result = thousand_separator + char + result
        else:
            result = char + result
    return result


async def covid(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    args = context.args
    query = " ".join(args)
    remove_space = query.split(" ")
    country = "%20".join(remove_space)
    if not country:
        url = "https://disease.sh/v3/covid-19/all?yesterday=false&twoDaysAgo=false&allowNull=true"
        country = "World"
    else:
        url = f"https://disease.sh/v3/covid-19/countries/{country}?yesterday=false&twoDaysAgo=false&strict=true&allowNull=true"
    request = requests.get(url).text
    case = json.loads(request)
    try:
        json_date = case["updated"]
    except (KeyError, IndexError):
        await message.reply_text("Make sure you have input correct country")
        return
    float_date = float(json_date) / 1000.0
    date = datetime.datetime.fromtimestamp(float_date).strftime(
        "%d %b %Y %I:%M:%S %p")
    try:
        flag = case["countryInfo"]["flag"]
    except (KeyError, IndexError):
        flag = []
    if flag:
        text = f"*COVID-19 Statistics in* [{query}]({flag})\n"
    else:
        text = f"*COVID-19 Statistics in {country} :*\n"
    text += f"Last Updated on `{date} GMT`\n\n🔼 Confirmed Cases : `{dot(case['cases'])}` | `+{dot(case['todayCases'])}`\n🔺 Active Cases : `{dot(case['active'])}`\n⚰️ Deaths : `{dot(case['deaths'])}` | `+{dot(case['todayDeaths'])}`\n💹 Recovered Cases: `{dot(case['recovered'])}` | `+{dot(case['todayRecovered'])}`\n💉 Total Tests : `{dot(case['tests'])}`\n👥 Populations : `{dot(case['population'])}`\n🌐 Source : worldometers"
    try:
        await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except Exception:
        await message.reply_text(
            "Try again in few times, maybe API are go down")


RAJNI_PTB.add_handler(
    DisableAbleCommandHandler(["covid", "corona"], covid))
