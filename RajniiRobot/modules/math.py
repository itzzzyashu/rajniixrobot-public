import math
import pynewtonmath as newton

from RajniiRobot import RAJNI_PTB
from RajniiRobot.modules.disable import DisableAbleCommandHandler

from telegram import Update
from telegram.ext import ContextTypes


# ---------- helpers ----------
def get_arg(context):
    return context.args[0] if context.args else None


# ---------- Newton based ----------
async def simplify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if not arg:
        return await update.effective_message.reply_text("Give expression")

    result = newton.simplify(str(arg))
    await update.effective_message.reply_text(str(result))


async def factor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if not arg:
        return await update.effective_message.reply_text("Give expression")

    result = newton.factor(str(arg))
    await update.effective_message.reply_text(str(result))


async def derive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if not arg:
        return await update.effective_message.reply_text("Give expression")

    result = newton.derive(str(arg))
    await update.effective_message.reply_text(str(result))


async def integrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if not arg:
        return await update.effective_message.reply_text("Give expression")

    result = newton.integrate(str(arg))
    await update.effective_message.reply_text(str(result))


async def zeroes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if not arg:
        return await update.effective_message.reply_text("Give expression")

    result = newton.zeroes(str(arg))
    await update.effective_message.reply_text(str(result))


async def tangent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if not arg:
        return await update.effective_message.reply_text("Give expression")

    result = newton.tangent(str(arg))
    await update.effective_message.reply_text(str(result))


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if not arg:
        return await update.effective_message.reply_text("Give expression")

    result = newton.area(str(arg))
    await update.effective_message.reply_text(str(result))


# ---------- math functions ----------
async def cos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.cos(float(arg))))


async def sin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.sin(float(arg))))


async def tan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.tan(float(arg))))


async def arccos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.acos(float(arg))))


async def arcsin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.asin(float(arg))))


async def arctan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.atan(float(arg))))


async def absolute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.fabs(float(arg))))


async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arg = get_arg(context)
    if arg is None:
        return await update.effective_message.reply_text("Give number")

    await update.effective_message.reply_text(str(math.log(float(arg))))


__help__ = """
Solves complex math problems using https://newton.now.sh
 ◇ `/math`*:* Math `/math 2^2+2(2)`
 ◇ `/factor`*:* Factor `/factor x^2 + 2x`
 ◇ `/derive`*:* Derive `/derive x^2+2x`
 ◇ `/integrate`*:* Integrate `/integrate x^2+2x`
 ◇ `/zeroes`*:* Find 0's `/zeroes x^2+2x`
 ◇ `/tangent`*:* Find Tangent `/tangent 2lx^3`
 ◇ `/area`*:* Area Under Curve `/area 2:4lx^3`
 ◇ `/cos`*:* Cosine `/cos pi`
 ◇ `/sin`*:* Sine `/sin 0`
 ◇ `/tan`*:* Tangent `/tan 0`
 ◇ `/arccos`*:* Inverse Cosine `/arccos 1`
 ◇ `/arcsin`*:* Inverse Sine `/arcsin 0`
 ◇ `/arctan`*:* Inverse Tangent `/arctan 0`
 ◇ `/abs`*:* Absolute Value `/abs -1`
 ◇ `/log`*:* Logarithm `/log 2l8`

_Keep in mind_: To find the tangent line of a function at a certain x value, send the request as c|f(x) where c is the given x value and f(x) is the function expression, the separator is a vertical bar '|'. See the table above for an example request.
To find the area under a function, send the request as c:d|f(x) where c is the starting x value, d is the ending x value, and f(x) is the function under which you want the curve between the two x values.
To compute fractions, enter expressions as numerator(over)denominator. For example, to process 2/4 you must send in your expression as 2(over)4. The result expression will be in standard math notation (1/2, 3/4).
"""

__mod_name__ = "Math"

SIMPLIFY_HANDLER = DisableAbleCommandHandler("math", simplify)
FACTOR_HANDLER = DisableAbleCommandHandler("factor", factor)
DERIVE_HANDLER = DisableAbleCommandHandler("derive", derive)
INTEGRATE_HANDLER = DisableAbleCommandHandler("integrate", integrate)
ZEROES_HANDLER = DisableAbleCommandHandler("zeroes", zeroes)
TANGENT_HANDLER = DisableAbleCommandHandler("tangent", tangent)
AREA_HANDLER = DisableAbleCommandHandler("area", area)
COS_HANDLER = DisableAbleCommandHandler("cos", cos)
SIN_HANDLER = DisableAbleCommandHandler("sin", sin)
TAN_HANDLER = DisableAbleCommandHandler("tan", tan)
ARCCOS_HANDLER = DisableAbleCommandHandler("arccos", arccos)
ARCSIN_HANDLER = DisableAbleCommandHandler("arcsin", arcsin)
ARCTAN_HANDLER = DisableAbleCommandHandler("arctan", arctan)
ABS_HANDLER = DisableAbleCommandHandler("abs", abs)
LOG_HANDLER = DisableAbleCommandHandler("log", log)

RAJNI_PTB.add_handler(SIMPLIFY_HANDLER)
RAJNI_PTB.add_handler(FACTOR_HANDLER)
RAJNI_PTB.add_handler(DERIVE_HANDLER)
RAJNI_PTB.add_handler(INTEGRATE_HANDLER)
RAJNI_PTB.add_handler(ZEROES_HANDLER)
RAJNI_PTB.add_handler(TANGENT_HANDLER)
RAJNI_PTB.add_handler(AREA_HANDLER)
RAJNI_PTB.add_handler(COS_HANDLER)
RAJNI_PTB.add_handler(SIN_HANDLER)
RAJNI_PTB.add_handler(TAN_HANDLER)
RAJNI_PTB.add_handler(ARCCOS_HANDLER)
RAJNI_PTB.add_handler(ARCSIN_HANDLER)
RAJNI_PTB.add_handler(ARCTAN_HANDLER)
RAJNI_PTB.add_handler(ABS_HANDLER)
RAJNI_PTB.add_handler(LOG_HANDLER)
