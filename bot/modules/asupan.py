import httpx

from pyrogram import Client, filters
from pyrogram.types import Message

from bot import app

@app.on_message(filters.command(["chika"]))
async def chika(c: Client, m: Message):
     http = httpx.AsyncClient(http2=True)
     r = await http.get("https://api-tede.herokuapp.com/api/chika")
     response = r.json()
     await m.reply_video(response["url"])



@app.on_message(filters.command(["wibu"]))
async def wibu(c: Client, m: Message):
     http = httpx.AsyncClient(http2=True)
     r = await http.get("https://api-tede.herokuapp.com/api/asupan/wibu")
     wib = r.json()
     await m.reply_video(wib["url"])
