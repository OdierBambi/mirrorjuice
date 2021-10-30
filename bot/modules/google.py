from search_engine_parser import GoogleSearch
from bot import app, dispatcher, Message
from telegram.ext import CommandHandler


@app.on_message(filters.command(['google']))
async def gsearch(message: Message):
    query = message.filtered_input_str
    await message.edit(f"**Googling** for `{query}` ...")
    flags = message.flags
    page = int(flags.get('-p', 1))
    limit = int(flags.get('-l', 5))
    if message.reply_to_message:
        query = message.reply_to_message.text
    if not query:
        await message.err("Give a query or reply to a message to google!")
        return
    try:
        g_search = GoogleSearch()
        gresults = await g_search.async_search(query, page)
    except Exception as e:
        await message.err(e)
        return
    output = ""
    for i in range(limit):
        try:
            title = gresults["titles"][i].replace("\n", " ")
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            output += f"[{title}]({link})\n"
            output += f"`{desc}`\n\n"
        except (IndexError, KeyError):
            break
    output = f"**Google Search:**\n`{query}`\n\n**Results:**\n{output}"
    await message.edit_or_send_as_file(text=output, caption=query,
                                       disable_web_page_preview=True)


GOOGLE_HANDLER = CommandHandler("google", gsearch)

dispatcher.add_handler(GOOGLE_HANDLER)
