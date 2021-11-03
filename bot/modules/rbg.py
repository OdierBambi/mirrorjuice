import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import app

REMOVEBG_API = "cvwHMNycC6yQdGJeRZgWLt2Y"
PATH = "./DOWNLOADS/"


START_TEXT = """
Hello {}, I am a media background remover bot. Send me a photo I will send the photo without background.

Made by @OdierBambi
"""
HELP_TEXT = """
- Just send me a photo
- I will download it
- I will send the photo without background

Made by @OdierBambi
"""
ABOUT_TEXT = """
- **Bot :** `Backround Remover Bot`
- **Creator :** [Fayas](https://telegram.me/TheFayas)
- **Channel :** [Fayas Noushad](https://telegram.me/FayasNoushad)
- **Source :** [Click here](https://github.com/FayasNoushad/Remove-BG-Bot/tree/main)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/FayasNoushad'),
        InlineKeyboardButton('Feedback', url='https://telegram.me/TheFayas')
        ],[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ERROR_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Owner', url='https://telegram.me/OdierBambi')
        ]]
    )

@app.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

@app.on_message(filters.command(["extrahelp"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

@app.on_message(filters.command(["removebg"]))
async def remove_background(bot, update):
    if not REMOVEBG_API:
        await update.reply_text(
            text="Error :- Remove BG Api is error",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return
    await update.reply_chat_action("typing")
    message = await update.reply_text(
        text="Processing",
        quote=True,
        disable_web_page_preview=True
    )
    new_file = PATH + str(update.from_user.id) + "/"
    new_file_name = new_file + "no_bg."
    replied = update.reply_to_message
    if replied.photo or (replied.document and "image" in replied.document.mime_type):
        new_file_name += "png"
        file = await update.download(PATH+str(update.from_user.id))
        await update.edit_text(
            text="Photo downloaded successfully. Now removing background.",
            disable_web_page_preview=True
        )
        new_document = removebg_image(file)
    elif update.video or (update.document and "video" in update.document.mime_type):
        new_file_name += "webm"
        file = await update.download(PATH+str(update.from_user.id))
        await upload.reply_text(
            text="Photo downloaded successfully. Now removing background.",
            disable_web_page_preview=True
        )
        new_document = removebg_video(file)
    else:
        await message.reply_text(text="Media not supported", disable_web_page_preview=True, reply_markup=ERROR_BUTTONS)
    if new_document.status_code == 200:
        with open(new_file_name, "wb") as file:
            file.write(new_document.content)
        await update.reply_chat_action("upload_document")
    else:
        await update.reply_text(text="API is error.", reply_markup=ERROR_BUTTONS)
        return
    try:
        await update.reply_document(document=new_file_name, quote=True)
        try:
            os.remove(file)
        except:
            pass
    except Exception as error:
        await message.edit_text(
            text=f"Error:- `{error}`",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )


def removebg_image(file):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(file, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVEBG_API}
    )
