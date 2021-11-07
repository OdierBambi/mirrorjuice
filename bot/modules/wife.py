import httpx

from pyrogram import Client, filters
from pyrogram.types import Message

from bot import app

@app.on_message(filters.command(['wife']))
async def waifu(c: Client, m: Message):
     http = httpx.AsyncClient(http2=True)
     r = await http.get("https://api.waifu.pics/sfw/waifu")
     rj = r.json()
     await m.reply_photo(rj["url"], caption=f"Ini waifumu 😉 {m.from_user.mention}")


@app.on_message(filters.command(['nwife']))
async def waifu(c: Client, m: Message):
     http = httpx.AsyncClient(http2=True)
     r = await http.get("https://api.waifu.pics/nsfw/waifu")
     rj = r.json()
     await m.reply_photo(rj["url"], caption=f"Ini waifumu 🤤 {m.from_user.mention}")

@app.on_message(filters.command(['nwife']))
async def waifu(c: Client, m: Message):
     http = httpx.AsyncClient(http2=True)
     r = await http.get("https://api.waifu.pics/nsfw/waifu")
     rj = r.json()
     await m.reply_photo(rj["url"], caption=f"Ini waifumu 🤤 {m.from_user.mention}")
