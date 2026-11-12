import requests

from RajniiRobot import CASH_API_KEY, RAJNI_PTB
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler


async def convert(update: Update):
    args = await update.effective_message.text.split(" ")
    message = update.effective_message

    if len(args) == 4:
        try:
            orig_cur_amount = float(args[1])

        except ValueError:
            await update.effective_message.reply_text(
                "Invalid Amount Of Currency")
            return

        orig_cur = args[2].upper()

        new_cur = args[3].upper()

        request_url = (f"https://www.alphavantage.co/query"
                       f"?function=CURRENCY_EXCHANGE_RATE"
                       f"&from_currency={orig_cur}"
                       f"&to_currency={new_cur}"
                       f"&apikey={CASH_API_KEY}")
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response["Realtime Currency Exchange Rate"]
                ["5. Exchange Rate"], )
        except (KeyError, IndexError):
            await update.effective_message.reply_text("Currency Not Supported."
                                                      )
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        await message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}", )

    elif len(args) == 1:
        await message.reply_text(_help_, parse_mode=ParseMode.MARKDOWN)

    else:
        await message.reply_text(
            f"*Invalid Args!!:* Required 3 But Passed {len(args) -1}",
            parse_mode=ParseMode.MARKDOWN,
        )


_help_ = """
💴 Currency converter:
➛ /cash`: currency converter.

Example:
 `/cash 1 USD INR`
      OR
 `/cash 1 usd inr`

Output: `1.0 USD = 75.505 INR`
"""

RAJNI_PTB.add_handler(CommandHandler("cash", convert))

__command_list__ = ["cash"]
