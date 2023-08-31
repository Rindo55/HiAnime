from pyrogram import Client, idle, filters, enums
from db import is_voted, save_vote
import time
from SafoneAPI import SafoneAPI
import os
import asyncio
from html_telegraph_poster.upload_images import upload_image
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from jikanpy import Jikan
import signal
from io import BytesIO
import sys
import random
import base64
import aiohttp
import requests
from html_telegraph_poster import TelegraphPoster
api_id = 3845818
api_hash = "95937bcf6bc0938f263fc7ad96959c6d"
bot_token = "6428443845:AAF9usGZRMRPPMuOfcjClNypt3N_p2_gUZc"
app = Client("anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
user_states = {}
async def timeout_message(chat_id):
    await asyncio.sleep(300)
    await app.send_message(chat_id, "Beep Boop! 5 minutes up, no response has been received. Your appeal has timed out. If you'd like to submit the appeal, please click [here](https://t.me/aniwatchappealbot?start=appeal).")

async def timeoutz_message(chat_id):
    await asyncio.sleep(500)
    await app.send_message(chat_id, "Beep Boop! 5 minutes up, no response has been received. Your appeal has timed out. If you'd like to submit the appeal, please click [here](https://t.me/aniwatchappealbot?start=appeal).")
user_states = {}
user_messages = {}

VOTE_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="✅ACCEPT", callback_data="vote1"),
            InlineKeyboardButton(text="❌DENY", callback_data="vote2")
        ]
    ]
)

# Define a function to handle the /start command
@app.on_message(filters.regex('/start appeal'))
def start(bot, update):
    user_id = update.from_user.id
    user_states[user_id] = 'waiting_link'
    user_messages[user_id] = []  # Initialize an empty list for user messages
    app.send_message(user_id, "State your **AniWatch profile link.**")

# Define a function to handle user messages
@app.on_message(filters.text)
async def handle_message(bot, update):
    user_id = update.from_user.id
    mention = update.from_user.mention()
    un = f"@{update.from_user.username}"
    if user_id in user_states:
        state = user_states[user_id]
        
        if state == 'waiting_link':
            if "http" in update.text:
                user_messages[user_id].append(f"**AniWatch Profile Link:** {update.text}")
                user_states[user_id] = 'waiting_punishment_date'
                await app.send_message(user_id, text="Mention the **date of your punishment.** \n\n(Note: Number of characters for this query must **not exceed** the limit of **15**)")
            else:
                await app.send_message(user_id, "Send a valid link.")
        if state == 'waiting_punishment_date':
            if len(update.text) <= 15:
                if any(char.isdigit() for char in update.text):
                    user_messages[user_id].append(f"**Date of punishment:** {update.text}")
                    user_states[user_id] = 'waiting_appeal'
                    await app.send_message(user_id, "**You may now proceed to construct your appeal and send it to me.**\n\n(Note: Number of characters for this query **must exceed 301** else appeal will be ignored.)")
                else:
                    await app.send_message(user_id, "Date must contain numeral. Please send **Date of punishment** again in the below format.\n\n xx/xx/xxxx or xx-xx-xxxx")
            else: 
                await app.send_message(user_id, "Characters must not exceed above 15 for this query. Send your **Date of punishment** again within 15 characters.")
        if state == 'waiting_appeal':
            if len(update.text) > 301:
                user_messages[user_id].append(f"**Appeal:** {update.text}")
                await app.send_message(user_id, "Your appeal has been received and is now under review.")
                combined_message = "\n".join(user_messages[user_id])  # Combine user messages
                ch_id = -1001894461368
                apl = await app.send_message(ch_id, text=f"**User:** {mention}\n**User ID:** {user_id}\n**User Name:** {un}\n\n{combined_message}", reply_markup=VOTE_MARKUP)
                await apl.reply_text("💬**REMARK**")
                await asyncio.sleep(2)
                await app.send_sticker(ch_id,"CAACAgUAAxkBAAEU_9FkRrLoli952oqIMVFPftW12xYLRwACGgADQ3PJEsT69_t2KrvBLwQ")
                del user_states[user_id]
                del user_messages[user_id]
            else:
                apl = await app.send_message(user_id, "Your appeal has been ignored due number character being less than 301. Send your **appeal again** with minimum of **301 characters.**")
def get_vote_buttons(a,b):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=f"✅ACCEPT ({a})", callback_data="vote1"),
                InlineKeyboardButton(text=f"❌DENY ({b})", callback_data="vote2")
            ]
        ]
    )
    return buttons

    
@app.on_callback_query(filters.regex("vote"))
async def votes_(_, query: CallbackQuery):
    try:
        id = query.message.id
        user = query.from_user.id
        chx_id = -1001894461368
        jar = await app.get_messages(chx_id, id)
        print(jar)
        usid = jar.text.split("\n")[1].split(": ")[1]
        print(usid)
        vote = int(query.data.replace("vote", "").strip())
        is_vote = await is_voted(id, user)
        if is_vote == 1:
            return await query.answer("Decision has already been made.")
        await query.answer()
        x = query.message.reply_markup
        a = 0
        b = 0
        for row in x.inline_keyboard:
            for button in row:
                if button.text.startswith('✅ACCEPT'):
                    a_str = button.text[8:].strip()
                    if a_str:
                        a = int(a_str)
                elif button.text.startswith('❌DENY'):
                    b_str = button.text[6:].strip()
                    if b_str:
                        b = int(b_str)
        if vote == 1:
            a = a + 1
            buttons = get_vote_buttons(a, b)
            await query.message.edit_reply_markup(reply_markup=buttons)
            await app.send_message(chat_id=usid, text="Your appeal has been accepted.")
        elif vote == 2:
            b = b + 1
            buttons = get_vote_buttons(a, b)
            await query.message.edit_reply_markup(reply_markup=buttons)
            await query.message.reply_text(chat_id=usid, text="Your appeal has been denied.")
        await save_vote(id, user)
    except Exception as e:
        print(e)
app.start()
print("Powered by aniwatch.to")
idle()

