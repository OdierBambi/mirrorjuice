from bot import app, dispatcher
from pyrogram import Client, filters
from telegram.ext import CommandHandler


@app.on_message(filters.command(['ginfo']))
def ginfo(client, message):
    id = message.from_user.id
    if id!=825664681 or id!=sudos:
        message.reply_text("Only Sudos or Owner can execute this command")
        return
    txt=message.text
    text = txt.split(" ", 1)
    chat_id=text[1]
    message = f"<b>Chat Name:</b> {app.get_chat(chat_id)}"
    message += f"<b>Total Members:</b> {app.get_chat_members_count(chat_id)}"
    message += f"<b>Photo:</b> {app.get_profile_photos(chat_id, limit=1)}"
    message += f"<b>Link:</b> {app.get_chat_invite_link(chat_id)}"
    try:
        message += f"<b>Pinned Message:</b> {app.get_dialogs(chat_id, pinned_only=True)}"
        message += f"<b>Chat Admins:</b> {app.get_chat_members(chat_id, filter="administrators")}"
    except TelegramError as e:
        return 
    message.reply_text(message)

GINFO_HANDLER = CommandHandler("ginfo", ginfo)

dispatcher.add_handler(GINFO_HANDLER)
