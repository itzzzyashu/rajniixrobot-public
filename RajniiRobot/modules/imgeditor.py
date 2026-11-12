from telethon import events, Button
from RajniiRobot import RAJNI_PTB, LOGGER

# By @TroJanzHEX
from RajniiRobot.utils.resources.ImageEditor.edit_1 import (
    black_white, box_blur, bright, g_blur, mix, normal_blur,
)
from RajniiRobot.utils.resources.ImageEditor.edit_2 import (
    cartoon, circle_with_bg, circle_without_bg, contrast, edge_curved, pencil,
    sepia_mode, sticker,
)
from RajniiRobot.utils.resources.ImageEditor.edit_3 import (
    black_border, blue_border, green_border, red_border,
)
from RajniiRobot.utils.resources.ImageEditor.edit_4 import (
    inverted, removebg_plain, removebg_sticker, removebg_white, rotate_90,
    rotate_180, rotate_270, round_sticker,
)
from RajniiRobot.utils.resources.ImageEditor.edit_5 import (
    normalglitch_1, normalglitch_2, normalglitch_3, normalglitch_4,
    normalglitch_5, scanlineglitch_1, scanlineglitch_2, scanlineglitch_3,
    scanlineglitch_4, scanlineglitch_5,
)
from RajniiRobot import telethn

lel = 00000000


@telethn.on(events.NewMessage(pattern=r"^[/.\?-](?:edit|editor)$", incoming=True))
async def photo(event):
    try:
        reply = await event.get_reply_message()
        if not reply or not reply.photo:
            await event.reply("Reply to an image man!ㅤㅤ")
            return
    except:
        return
    global lel
    try:
        lel = event.sender_id
    except:
        return
    try:
        buttons = [
            [
                Button.inline("💡 BRIGHT", data="bright"),
                Button.inline("🖼 MIXED", data="mix"),
                Button.inline("🔳 B&W", data="b|w"),
            ],
            [
                Button.inline("🟡 CIRCLE", data="circle"),
                Button.inline("🩸 BLUR", data="blur"),
                Button.inline("🌌 BORDER", data="border"),
            ],
            [
                Button.inline("🎉 STICKER", data="stick"),
                Button.inline("↩️ ROTATE", data="rotate"),
                Button.inline("🔦 CONTRAST", data="contrast"),
            ],
            [
                Button.inline("🌇 SEPIA", data="sepia"),
                Button.inline("✏️ PENCIL", data="pencil"),
                Button.inline("🐶 CARTOON", data="cartoon"),
            ],
            [
                Button.inline("🔄 INVERT", data="inverted"),
                Button.inline("🔮 GLITCH", data="glitch"),
                Button.inline("✂️ REMOVE BG", data="removebg"),
            ],
            [
                Button.inline("❌ CLOSE", data="close_e"),
            ],
        ]
        await telethn.send_message(
            event.chat_id,
            text="Select your required mode from below!ㅤㅤ",
            buttons=buttons,
            reply_to=reply.id,
        )
    except Exception as e:
        LOGGER.debug(f"photomarkup error - {str(e)}")
        if "USER_IS_BLOCKED" in str(e):
            return
        try:
            await event.reply("Something went wrong!", quote=True)
        except Exception:
            return


@telethn.on(events.CallbackQuery())
async def cb_handler(event):
    user_id = event.sender_id
    data = event.data.decode("utf-8")
    if lel == user_id:
        if data == "removebg":
            await event.edit(
                "**Select required mode**ㅤㅤㅤㅤ",
                buttons=[
                    [
                        Button.inline("WITH WHITE BG", data="rmbgwhite"),
                        Button.inline("WITHOUT BG", data="rmbgplain"),
                    ],
                    [
                        Button.inline("STICKER", data="rmbgsticker")
                    ],
                ],
            )
        elif data == "stick":
            await event.edit(
                "**Select a Type**",
                buttons=[
                    [
                        Button.inline("Normal", data="stkr"),
                        Button.inline("Edge Curved", data="cur_ved"),
                    ],
                    [
                        Button.inline("Circle", data="circle_sticker")
                    ],
                ],
            )
        elif data == "rotate":
            await event.edit(
                "**Select the Degree**",
                buttons=[
                    [
                        Button.inline("180", data="180"),
                        Button.inline("90", data="90"),
                    ],
                    [Button.inline("270", data="270")],
                ],
            )

        elif data == "glitch":
            await event.edit(
                "**Select required mode**ㅤㅤㅤㅤ",
                buttons=[[
                    Button.inline("NORMAL", data="normalglitch"),
                    Button.inline("SCAN LINES", data="scanlineglitch"),
                ]],
            )
        elif data == "normalglitch":
            await event.edit(
                "**Select Glitch power level**",
                buttons=[
                    [
                        Button.inline("1", data="normalglitch1"),
                        Button.inline("2", data="normalglitch2"),
                        Button.inline("3", data="normalglitch3"),
                    ],
                    [
                        Button.inline("4", data="normalglitch4"),
                        Button.inline("5", data="normalglitch5"),
                    ],
                ],
            )
        elif data == "scanlineglitch":
            await event.edit(
                "**Select Glitch power level**",
                buttons=[
                    [
                        Button.inline("1", data="scanlineglitch1"),
                        Button.inline("2", data="scanlineglitch2"),
                        Button.inline("3", data="scanlineglitch3"),
                    ],
                    [
                        Button.inline("4", data="scanlineglitch4"),
                        Button.inline("5", data="scanlineglitch5"),
                    ],
                ],
            )
        elif data == "blur":
            await event.edit(
                "**Select a Type**",
                buttons=[
                    [
                        Button.inline("box", data="box"),
                        Button.inline("normal", data="normal"),
                    ],
                    [
                        Button.inline("Gaussian", data="gas")
                    ],
                ],
            )
        elif data == "circle":
            await event.edit(
                "**Select required mode**",
                buttons=[[
                    Button.inline("WITH BG", data="circlewithbg"),
                    Button.inline("WITHOUT BG", data="circlewithoutbg"),
                ]],
            )
        elif data == "border":
            await event.edit(
                "**Select Border**",
                buttons=[
                    [
                        Button.inline("🔴 RED 🔴", data="red"),
                        Button.inline("🟢 Green 🟢", data="green"),
                    ],
                    [
                        Button.inline("⚫ Black ⚫", data="black"),
                        Button.inline("🔵 Blue 🔵", data="blue"),
                    ],
                ],
            )

        elif data == "bright":
            await event.delete()
            await bright(telethn, event.message)

        elif data == "close_e":
            await event.delete()

        elif data == "mix":
            await event.delete()
            await mix(telethn, event.message)

        elif data == "b|w":
            await event.delete()
            await black_white(telethn, event.message)

        elif data == "circlewithbg":
            await event.delete()
            await circle_with_bg(telethn, event.message)

        elif data == "circlewithoutbg":
            await event.delete()
            await circle_without_bg(telethn, event.message)

        elif data == "green":
            await event.delete()
            await green_border(telethn, event.message)

        elif data == "blue":
            await event.delete()
            await blue_border(telethn, event.message)

        elif data == "red":
            await event.delete()
            await red_border(telethn, event.message)

        elif data == "black":
            await event.delete()
            await black_border(telethn, event.message)

        elif data == "circle_sticker":
            await event.delete()
            await round_sticker(telethn, event.message)

        elif data == "inverted":
            await event.delete()
            await inverted(telethn, event.message)

        elif data == "stkr":
            await event.delete()
            await sticker(telethn, event.message)

        elif data == "cur_ved":
            await event.delete()
            await edge_curved(telethn, event.message)

        elif data == "90":
            await event.delete()
            await rotate_90(telethn, event.message)

        elif data == "180":
            await event.delete()
            await rotate_180(telethn, event.message)

        elif data == "270":
            await event.delete()
            await rotate_270(telethn, event.message)

        elif data == "contrast":
            await event.delete()
            await contrast(telethn, event.message)

        elif data == "box":
            await event.delete()
            await box_blur(telethn, event.message)

        elif data == "gas":
            await event.delete()
            await g_blur(telethn, event.message)

        elif data == "normal":
            await event.delete()
            await normal_blur(telethn, event.message)

        elif data == "sepia":
            await event.delete()
            await sepia_mode(telethn, event.message)

        elif data == "pencil":
            await event.delete()
            await pencil(telethn, event.message)

        elif data == "cartoon":
            await event.delete()
            await cartoon(telethn, event.message)

        elif data == "normalglitch1":
            await event.delete()
            await normalglitch_1(telethn, event.message)

        elif data == "normalglitch2":
            await event.delete()
            await normalglitch_2(telethn, event.message)

        elif data == "normalglitch3":
            await normalglitch_3(telethn, event.message)

        elif data == "normalglitch4":
            await event.delete()
            await normalglitch_4(telethn, event.message)

        elif data == "normalglitch5":
            await event.delete()
            await normalglitch_5(telethn, event.message)

        elif data == "scanlineglitch1":
            await event.delete()
            await scanlineglitch_1(telethn, event.message)

        elif data == "scanlineglitch2":
            await event.delete()
            await scanlineglitch_2(telethn, event.message)

        elif data == "scanlineglitch3":
            await event.delete()
            await scanlineglitch_3(telethn, event.message)

        elif data == "scanlineglitch4":
            await event.delete()
            await scanlineglitch_4(telethn, event.message)

        elif data == "scanlineglitch5":
            await event.delete()
            await scanlineglitch_5(telethn, event.message)

        elif data == "rmbgwhite":
            await event.delete()
            await removebg_white(telethn, event.message)

        elif data == "rmbgplain":
            await event.delete()
            await removebg_plain(telethn, event.message)

        elif data == "rmbgsticker":
            await removebg_sticker(telethn, event.message)

__mod_name__ = "Image Editor"
__help__ = f"""
RajniiRobot have some advanced image editing tools inbuilt
Bright, Circle, RemBG, Blur, Border, Flip, Glitch, Sticker maker and more
➛ /edit [reply to image]*:* Open the image editor
➛ /rmbg [REPLY]*:* Revove BG of replied image/sticker.

"""