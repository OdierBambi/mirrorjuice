import os
from pyrogram import Client, filters
from removebg import RemoveBg
from pyrogram.types import Message
from bot import app

REMOVE_BG_API = "cvwHMNycC6yQdGJeRZgWLt2Y"
PATH = "./DOWNLOADS/"


@app.on_message(filters.command(["removebg"]))
async def remove_background(client, message):
    if not REMOVE_BG_API:
        await update.reply_text(
            text="Error :- Remove BG Api is error",
            quote=True,
            disable_web_page_preview=True
          )
        return
    await message.reply_text("Analysing...")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        if os.path.exists(PATH):
            os.remove(PATH)
        await bot.download_media(message=replied,
                                            file_name=PATH
                                            )        
        try:
            rmbg = RemoveBg(REMOVE_BG_API)
            rmbg.remove_background_from_img_file(PATH)
            rbg_path = PATH + "_no_bg.png"
            await bot.send_document(
                chat_id=message.chat.id,
                document=rbg_path,
                disable_notification=True,
                )
            await message.delete()
        except Exception:  # pylint: disable=broad-except
            await message.reply_text("Something went wrong!\nCheck your usage quota!")
            return
    else:
        await message.reply_text("Reply to a photo to remove background!")
