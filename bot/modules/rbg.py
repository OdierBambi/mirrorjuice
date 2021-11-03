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
    new_file = PATH + str(update.from_user.id) + "/"
    new_file_name = new_file + "no_bg."
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        file = await message.download(PATH+str(update.from_user.id))
        await message.edit_text(
            text="Photo downloaded successfully. Now removing background.",
            disable_web_page_preview=True
        )
        new_document = removebg_image(file)
    if new_document.status_code == 200:
        with open(new_file_name, "wb") as file:
            file.write(new_document.content)
            await message.reply_chat_action("upload_document")
    try:
        await message.reply_document(document=new_file_name, quote=True)
        try:
            os.remove(file)
        except:
            pass
        except Exception:  # pylint: disable=broad-except
            await message.reply_text("Something went wrong!\nCheck your usage quota!")
    else:
        await message.reply_text("Reply to a photo to remove background!")


def removebg_image(file):
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(file, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVE_BG_API}
    )
