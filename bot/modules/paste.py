import httpx

from pyrogram import Client, filters
from pyrogram.types import Message, User, InlineKeyboardButton, InlineKeyboardMarkup
from bot import app, dispatcher
from telegram.ext import CommandHandler


@app.on_message(filters.command(['paste']))
async def hastebin(c: Client, m: Message):
    if m.reply_to_message:
        if m.reply_to_message.document:
            tfile = m.reply_to_message
            to_file = await tfile.download()
            with open(to_file, "rb") as fd:
                mean = fd.read().decode("UTF-8")
        if m.reply_to_message.text:
            mean = m.reply_to_message.text
        
        http = httpx.AsyncClient(http2=True)
        url = "https://hastebin.com/documents"
        r = await http.post(url, data=mean.encode("UTF-8"))
        url = f"https://hastebin.com/{r.json()['key']}"
        markup = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Klik disini ⚙', url=url)
        ]]
    )
        await m.reply_photo('https://telegra.ph/file/035a463a52268420f6a0c.jpg', caption=f"Request paste by {m.from_user.mention}", reply_markup=markup)
    else:
        await m.reply_text("reply_to_document_or_text")


PASTE_HANDLER = CommandHandler("paste", hastebin)

dispatcher.add_handler(PASTE_HANDLER)
