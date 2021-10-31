import os
from pyrogram import Client, filters
from pyrogram.types import Message, User, InlineKeyboardButton, InlineKeyboardMarkup
from bot import app



@app.on_message(filters.new_chat_members)
async def welcome(bot,message):
	chatid = message.chat.id
	markup = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Contact me ⚙', url='https://telegram.me/OdierBambi')
        ]]
    )
	await bot.send_message(text=f"Selamat Datang {message.from_user.mention} to {message.chat.username} ,  Happy to have here", chat_id=chatid, reply_markup=markup)
	
@app.on_message(filters.left_chat_member)
async def goodbye(bot,message):
	chatid= message.chat.id
	await bot.send_message(text=f"Selamat jalan ,  {message.from_user.mention} , Semoga harimu menyenangkan😁",chat_id=chatid)
