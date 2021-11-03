import os
from datetime import datetime
from removebg import RemoveBg
from ptrogram.types import Message
from bot import app

REMOVEBG_API = "cvwHMNycC6yQdGJeRZgWLt2Y"
PATH = "./DOWNLOADS/"


@app.on_message(filters.command(["removebg"]))
async def remove_background(message: Message):
    if not REMOVE_BG_API:
        await update.reply_text(
            text="Error :- Remove BG Api is error",
            quote=True,
            disable_web_page_preview=True
          )
        return
    await message.edit_text("Analysing...")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        start_t = datetime.now()
        if os.path.exists(PATH):
            os.remove(PATH)
        await message.client.download_media(message=replied,
                                            file_name=PATH
                                            )
        
        try:
            rmbg = RemoveBg(REMOVE_BG_API)
            rmbg.remove_background_from_img_file(PATH)
            rbg_path = PATH + "_no_bg.png"
            await message.client.send_document(
                chat_id=message.chat.id,
                document=rbg_path,
                disable_notification=True,
                )
            await message.delete()
        except Exception:  # pylint: disable=broad-except
            await message.edit_text("Something went wrong!\nCheck your usage quota!")
            return
    else:
        await message.edit_text("Reply to a photo to remove background!")
