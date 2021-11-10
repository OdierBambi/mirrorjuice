from search_engine_parser import GoogleSearch
from pyrogram import filters
from pyrogram.types import Message
from bot import app


@app.on_message(filters.command(["google"]))
async def gsearch(client, message):
    query = message.text.split(None, 1)[1]
    process = await message.repy_text(f"**Googling** for `{query}` ...")
    if message.reply_to_message:
        query = message.reply_to_message
    if not query:
        await message.reply_text("Give a query or reply to a message to google!")
        return
    try:
        g_search = GoogleSearch()
        gresults = await g_search.async_search(query)
    except Exception as e:
        await message.reply(e)
        return
    output = ""
    for i in range:
        try:
            title = gresults["titles"][i].replace("\n", " ")
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            output += f"[{title}]({link})\n"
            output += f"`{desc}`\n\n"
        except (IndexError, KeyError):
            break
    output = f"**Google Search:**\n`{query}`\n\n**Results:**\n{output}"
    await process.edit(text=output, caption=query,
                                       disable_web_page_preview=True)



