import os
import png
from pyrogram import Client, filters
from pyqrcode import QRCode
from bot import app


@app.on_message(filters.command(["mkqr"]))
def qrcode(client, message):
    text = update.message.text.split(" ", 1)[1]
    message_id = update.message.message_id
    qr_file = f'{message_id}.png'
    try:
        await message.reply_text("Generating")
        Qr_Code = QRCode(text)
        Qr_Code.png(qr_file, scale=10)
        await message.reply_photo(photo=open(
            qr_file, "rb"), reply_to_message_id=message_id, caption=f"Here is Your Qr code for '{text}'")
        await message.reply_text("Finished")
        os.remove(qr_file)
    except Exception:
        await message.reply_text("Please Try Agian Later")
