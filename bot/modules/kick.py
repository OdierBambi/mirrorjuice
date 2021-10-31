import re
from html import escape
from urllib.parse import quote, unquote
from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message
from bot import app, dispatcher
from telegram.ext import CommandHandler


@app.on_message(filters.command(['urlencode']))
async def urlencode(c: Client, m: Message):
    await m.reply_text(quote(m.text.split(None, 1)[1]))
    
@app.on_message(filters.command(['urldecode']))
async def urldecode(c: Client, m: Message):
    await m.reply_text(unquote(m.text.split(None, 1)[1]))


URLENCODE_HANDLER = CommandHandler("urlencode", urlencode)
URLDECODE_HANDLER = CommandHandler("urldecode", urldecode)

dispatcher.add_handler(URLENCODE_HANDLER)
dispatcher.add_handler(URLDECODE_HANDLER)
