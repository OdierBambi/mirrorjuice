import asyncio

import cv2
import qrcode
from pyrogram import filters
from pyrogram.types import Message

from bot import app


@app.on_message(filters.command(["qr"]))
async def generate_qr(client, message):
    if qr_text := await client.extract_command_text(message):
        img = qrcode.make(qr_text)

        with open('downloads/qr.png', 'wb') as f:
            img.save(f)

        await asyncio.gather(
            client.send_photo(message.chat.id, 'bot/qr.png'),
            message.delete()
        )


@app.on_message(filters.command(["qrscan"]) & filters.reply)
async def scan_qr(_, message: Message):
    await message.reply_to_message.download('bot/qr.png')
    img = cv2.imread('downloads/qr.png')
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    await message.reply_text(data)
