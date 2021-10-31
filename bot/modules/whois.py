from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os

from bot import app, dispatcher
from telegram.ext import CommandHandler


@app.on_message(filters.command(['whois']))
async def whois(client, message):
    await message.reply(
        f"""        
<b>First name</b>: {message.from_user.first_name}
<b>Last name</b>: {message.from_user.last_name}
<b>Username</b>: {message.from_user.username}
<b>User id</b>: <code>{message.from_user.id}</code>
<b>Phone number</b>: {message.from_user.phone_number}
<b>Language</b>: {message.from_user.language_code}
<b>Status</b>: {message.from_user.status}
<b>Bio</b>: <code>{message.from_chat.bio}</code>
<b>Data center id</b>: {message.from_user.dc_id}"""
)

WHOIS_HANDLER = CommandHandler("whois", whois)

dispatcher.add_handler(WHOIS_HANDLER)
