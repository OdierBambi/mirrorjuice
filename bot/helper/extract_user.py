from pyrogram.types import Message
import logging
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from imdb import IMDb
import asyncio
import re
import os
from datetime import datetime
from typing import List


async def get_poster(query, bulk=False, id=False):
    if not id:
        # https://t.me/GetTGLink/4183
        pattern = re.compile(r"^(([a-zA-Z\s])*)?\s?([1-2]\d\d\d)?", re.IGNORECASE)
        match = pattern.match(query)
        year = None
        if match:
            title = match.group(1)
            year = match.group(3)
        else:
            title = query
        movieid = IMDb.search_movie(title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered=list(filter(lambda k: str(k.get('year')) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid=list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = int(query)
    movie = IMDb.get_movie(movieid)
    title = movie.get('title')
    genres = ", ".join(movie.get("genres")) if movie.get("genres") else None
    rating = str(movie.get("rating"))
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    poster = movie.get('full-size cover url')
    plot = movie.get('plot')
    if plot and len(plot) > 0:
        plot = plot[0]
    if plot and len(plot) > 800:
        plot = plot[0:800] + "..."
    return {
        'title': title,
        'year': date,
        'genres': genres,
        'poster': poster,
        'plot': plot,
        'rating': rating,
        'url':f'https://www.imdb.com/title/tt{movieid}'
     }



def last_online(from_user):
    time = ""
    if from_user.is_bot:
        time += "🤖 Bot :("
    elif from_user.status == 'recently':
        time += "Recently"
    elif from_user.status == 'within_week':
        time += "Within the last week"
    elif from_user.status == 'within_month':
        time += "Within the last month"
    elif from_user.status == 'long_time_ago':
        time += "A long time ago :("
    elif from_user.status == 'online':
        time += "Currently Online"
    elif from_user.status == 'offline':
        time += datetime.fromtimestamp(from_user.last_online_date).strftime("%a, %d %b %Y, %H:%M:%S")
    return time



def extract_user(message: Message) -> (int, str):
    """extracts the user from a message"""
    user_id = None
    user_first_name = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name

    elif len(message.command) > 1:
        if (
            len(message.entities) > 1 and
            message.entities[1].type == "text_mention"
        ):
            # 0: is the command used
            # 1: should be the user specified
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id

        try:
            user_id = int(user_id)
        except ValueError:
            print("menipu ")

    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name

    return (user_id, user_first_name)



def get_file_id(msg: Message):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj
