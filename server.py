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

START_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Create an appeal", url="https://t.me/aniwatchappealbot?start=appeal"),
        ]
    ]
) 

VOTE_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="ACCEPT", callback_data="vote1"),
            InlineKeyboardButton(text="DENY", callback_data="vote2")
        ],
        [
            InlineKeyboardButton(text="🔨15d", callback_data="vote3"),
            InlineKeyboardButton(text="🔨20d", callback_data="vote4"),
            InlineKeyboardButton(text="🔨25d", callback_data="vote5")
        ],
        [
            InlineKeyboardButton(text="MANUALLY REVIEW", callback_data="vote6"),
        ]
    ]
)

@app.on_message(filters.command("send"))
async def start(bot, cmd: Message):
    mfg_id=cmd.id
    apx_id=-1001811950874
    post_1 = f"""**Chats | Unban Appeal Guidelines**

Users who wish to make an Unban Appeal for their AniWatch Account may go through these Guidelines.

**This Guide Consists Of:**

･❱ Crafting an Unban Appeal
･❱ Valid Appeals
･❱ Staff Contact
･❱ Waiting Period
･❱ Unban
･❱ Respect Staff Judgement
･❱ Important"""
    
    post_2 = f"""**1. Creating an unban appeal**

__Users are to follow the said format while creating an unban Appeal. We do not accept appeals for mutes.__"""
    post_3 = f"""**Appeal Format**

**AniWatch Profile Link -**

• Visit the Community Page > Myzone. Hold/Tap your username and copy link.

**Date of Ban:**

• Click the notification icon and enter the date stated in the notification.

**Reason for Ban:**

• The reason shall be stated in the Notification as well, please attach a screenshot of the notification with the appeal.

**Appeal:**

• Submit Valid Appeals, make sure your appeal is of meaning and follows the guidelines and the format.

`Make sure to read through everything and provide the correct details stated in the embed below.`"""
    post_4 = f"""**2. Valid Appeals**

• __If your appeal is of no meaning, inappropriate or doesn't follow the appeal format, then it may get rejected on the spot by the Staff without any consideration.__

• __To show an apologetic nature for the actions done and construct a statement that states: Such shall not be repeated in the future, and if seen repeated, the user agrees to be banned permanently.__

• __The decision may change depending on the offenses done by the account. <b>Make sure you provide the <u>correct link to your AniWatch Profile</u>, and other details mentioned in the embed.</b>__

• __Appeals for 24 hours, 48hours, or 72 hours Mute are not accepted.__

• __Appeals for alternative accounts are not accepted.__

• __Attempting to get your friend's punishment lifted will get you the same punishment, if they want to appeal they will have to follow these steps.__"""
    post_5 = f"""**3. Staff Contact**

• __Once you are prepared to create an appeal, you may react to the <b><u>Button</b></u> connected to this embed.__

• __The <b>@AniWatchAppealBot</b> bot shall DM you, you may now select the <u>APPEAL</u> form placed in the bot embed and <u>follow the instructions</u> that has been stated throughout the procedures accordingly.__

• __<b>DO NOT spam or conduct any similar actions using the appeal system, it may result in your appeal being rejected without even being considered and be result to moderative actions at certain cases.</b>__"""
    post_6 = f"""**4. Waiting period**

• __You are to await the judgment for the least of <b><u>7 Days</b></u> in respect to the reviewal process by the Community Mods & Community Admins. Once you have submitted the Appeal, @AniWatchAppealBot will notify you whether if the Appeal is accepted or rejected.__

• __In the event that you have not received a response from the designated appeal field with which you have created the appeal, it is advisable to initiate a "Direct Message" with a Community Mod to follow up. However, if you continue to encounter a lack of response, it is probable that your appeal has been declined.__"""
    post_7 = f"""
Appeal stuff
**5. Unban**

• __If your appeal has been accepted by the staff team, a Community Mod or perhaps a Community Admin shall DM you stating your wait period for an unban. If your account is still banned after the wait period, you may kindly remind the designated <b>Community Staff</b> to unban your account by DMing them.__"""
    post_8 = f"""**6. Respect Staff Judgement**

• __The staff judgements are at all times respective towards the appeals and the user is to obey the decisions made.__

• __If the user is to not accept the judgment and seen requesting constantly for an unban, before the time allocated, the punishment shall be extended to a much prolonged period of time.__"""
    post_9 = f"""**⚠️ Important ⚠️**

**This is a public warning to everyone wanting to Appeal their ban on** `AniWatch`. Once you make an appeal, you agree with the `AniWatch Community Guidelines`.

• __Do note that appeals in an attempt at an unban for the second time due to the repeating of a major rulebreak after an initial unban shall not in any case be accepted or considered.__

• __Thus you are strictly warned to not repeat any of a rulebreak after an unban as another appeal from the same user at another time is considered to be unauthentic and therefore nulled.__"""
    await cmd.reply_photo(photo="https://te.legra.ph/file/be7367d62fc78ca9b0668.jpg", caption=post_1)
    await cmd.reply_text(post_2)
    await cmd.reply_text(post_3)
    await cmd.reply_text(post_4)
# Define a function to handle the /start command
@app.on_message(filters.command("start") & filters.private)
async def start(bot, cmd: Message):
    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/start":
        await cmd.reply_text("**Hey! I am an appeal bot serving for aniwatch.to. Click the below button & follow the instructions to make an appeal for your banned account.**", reply_markup=START_MARKUP)
    elif cmd.text.split("_", 1)[0] == "/start user":
        user_id = cmd.from_user.id
        user_states[user_id] = 'send_link'
        xc_id=int(usr_cmd.split("_")[-1])
        userxd = await app.get_users(xc_id)
        usrc = userxd.mention()
        tlu = await app.send_message(user_id, f"**Send me the message you want me to forward to** {usrc}\n USER ID: {xc_id}")
        
    elif usr_cmd == "/start appeal":
        user_id = cmd.from_user.id
        user_states[user_id] = 'waiting_link'
        user_messages[user_id] = []  # Initialize an empty list for user messages
        await app.send_message(user_id, "State your **AniWatch profile link.**")

# Define a function to handle user messages
@app.on_message(filters.text)
async def handle_message(bot, update):
    user_id = update.from_user.id
    mention = update.from_user.mention()
    un = f"@{update.from_user.username}"
    if user_id in user_states:
        state = user_states[user_id]
        if state == 'send_link':
            ert = update.id
            taku = int(ert) - 1
            tax = await app.get_messages(user_id, taku)
            usm = tax.text.split("\n")[1].split(": ")[1]
            wru = int(usm)
            await app.copy_message(
                chat_id=wru,
                from_chat_id=user_id,
                message_id=ert
            )
        if state == 'waiting_link':
            if "http" in update.text:
                user_messages[user_id].append(f"<b>AniWatch Profile Link:</b> {update.text}")
                user_states[user_id] = 'waiting_punishment_date'
                await app.send_message(user_id, text="Mention the <b>date of your punishment.</b> \n\n(Note: Number of characters for this query must **not exceed** the limit of **15**)")
            else:
                await app.send_message(user_id, "Send a valid link.")
        if state == 'waiting_punishment_date':
            if len(update.text) <= 15:
                if any(char.isdigit() for char in update.text):
                    user_messages[user_id].append(f"<b>Date of punishment:</b> {update.text}")
                    user_states[user_id] = 'waiting_appeal'
                    await app.send_message(user_id, "**You may now proceed to construct your appeal and send it to me.**\n\n(Note: Number of characters for this query **must exceed 301** else appeal will be ignored.)")
                else:
                    await app.send_message(user_id, "Date must contain numeral. Please send **Date of punishment** again in the below format.\n\n xx/xx/xxxx or xx-xx-xxxx")
            else: 
                await app.send_message(user_id, "Characters must not exceed above 15 for this query. Send your **Date of punishment** again within 15 characters.")
        if state == 'waiting_appeal':
            if len(update.text) > 301:
                user_messages[user_id].append(f"<b>Appeal:</b> {update.text}")
                await app.send_message(user_id, "Your appeal has been received and is now under review.")
                combined_message = "\n".join(user_messages[user_id])  # Combine user messages
                ch_id = -1001894461368
                apl = await app.send_message(ch_id, text=f"<b>User:</b> {mention}\n<b>User ID:</b> <code>{user_id}</code>\n<b>Username:</b>{un}\n━━━━━━━━━━━━━━━━━━━━━━\n{combined_message}\n━━━━━━━━━━━━━━━━━━━━━━\n<b>Status</b>: ⚠️ | To be reviewed", reply_markup=VOTE_MARKUP, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
                await apl.reply_text("💬**REMARK**")
                await asyncio.sleep(2)
                await app.send_sticker(ch_id,"CAACAgUAAxkBAAEU_9FkRrLoli952oqIMVFPftW12xYLRwACGgADQ3PJEsT69_t2KrvBLwQ")
                del user_states[user_id]
                del user_messages[user_id]
            else:
                apl = await app.send_message(user_id, "Your appeal has been ignored due to number character being less than 301. Send your **appeal again** with minimum of **301 characters.**")
def get_vote_buttons(a,b,c,d,e,f):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=f"ACCEPT {a}", callback_data="vote1"),
                InlineKeyboardButton(text=f"DENY {b}", callback_data="vote2")
            ],
            [
                InlineKeyboardButton(text=f"🔨15d {c}", callback_data="vote3"),
                InlineKeyboardButton(text=f"🔨20d {d}", callback_data="vote4"),
                InlineKeyboardButton(text=f"🔨25d {e}", callback_data="vote5"),
            ],
            [
                InlineKeyboardButton(text=f"MANUALLY REVIEW  {f}", callback_data="vote6"),
            ]
        ]
    )
    return buttons

    
@app.on_callback_query(filters.regex("vote"))
async def votes_(_, query: CallbackQuery):
    try:
        id = query.message.id
        user = query.from_user.id
        
        men = query.from_user.mention()
        chx_id = -1001894461368
        jar = await app.get_messages(chx_id, id)
        print(jar)
        lmx = jar.text
        usid = jar.text.split("\n")[1].split(": ")[1]
        print(usid)
        vote = int(query.data.replace("vote", "").strip())
        is_vote = await is_voted(id, user)
        if is_vote == 1:
            return await query.answer(f"Appeal has already been reviewed.")
        x = query.message.reply_markup
        a = ""
        b = ""
        c = ""
        d = ""
        e = ""
        f = ""
        for row in x.inline_keyboard:
            for button in row:
                if button.text.startswith('ACCEPT'):
                    a_str = button.text[7:].strip()
                    if a_str:
                        a = int(a_str)
                elif button.text.startswith('DENY'):
                    b_str = button.text[5:].strip()
                    if b_str:
                        b = int(b_str)
        if vote == 1:
            a = "(✅)"
            buttons = get_vote_buttons(a, b, c, d, e, f)
            await query.message.edit_reply_markup(reply_markup=buttons)
            await app.send_message(chat_id=usid, text="Your appeal has been accepted. Your account has now been unbanned.")
            acx = lmx.replace("⚠️ | To be reviewed", f"✅ | Appeal accepted by {men}")
            await query.message.edit_text(text=acx, reply_markup=buttons, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        elif vote == 2:
            b = "(✅)"
            buttons = get_vote_buttons(a, b, c, d , e, f)
            await query.message.edit_reply_markup(reply_markup=buttons)
            await app.send_message(chat_id=usid, text="Your appeal has been denied.")
            denx =  lmx.replace("⚠️ | To be reviewed", f"✅ | Appeal rejected by {men}") 
            await query.message.edit_text(text=denx, reply_markup=buttons, disable_web_page_preview=True)
        elif vote == 3:
            c = "(✅)"
            buttons = get_vote_buttons(a, b, c, d , e, f)
            await query.message.edit_reply_markup(reply_markup=buttons)
            await app.send_message(chat_id=usid, text="Your appeal has been accepted. However, after reviewing your actions it has been decided that your account will only be unbanned after a period of 15 days.")
            denx =  lmx.replace("⚠️ | To be reviewed", f"✅ | Appeal accepted by {men} | unban after 15 days")
            await query.message.edit_text(text=denx, reply_markup=buttons, disable_web_page_preview=True)
        elif vote == 4:
            d = "(✅)"
            buttons = get_vote_buttons(a, b, c, d , e, f)
            await query.message.edit_reply_markup(reply_markup=buttons)
            await app.send_message(chat_id=usid, text="Your appeal has been accepted. However, after reviewing your actions it has been decided that your account will only be unbanned after a period of 20 days.")
            denx =  lmx.replace("⚠️ | To be reviewed",f"✅ | Appeal accepted by {men} | unban after 20 days")
            await query.message.edit_text(text=denx, reply_markup=buttons, disable_web_page_preview=True)
        elif vote == 5:
            e = "(✅)"
            buttons = get_vote_buttons(a, b, c, d , e, f)
            await query.message.edit_reply_markup(reply_markup=buttons)
            await app.send_message(chat_id=usid, text="Your appeal has been accepted. However, after reviewing your actions it has been decided that your account will only be unbanned after a period of 25 days.")
            denx =  lmx.replace("⚠️ | To be reviewed", f"✅ | Appeal accepted by {men} | unban after 25 days") 
            await query.message.edit_text(text=denx, reply_markup=buttons, disable_web_page_preview=True)
        elif vote == 6:
            f = "(✅)"
            buttons = get_vote_buttons(a, b, c, d , e, f)
            await query.answer(url=f"t.me/AniWatchAppealBot?start=user_{usid}")
            await query.answer()
            await query.message.edit_reply_markup(reply_markup=buttons)
            denx =  lmx.replace("⚠️ | To be reviewed", f"✅ | Appeal accepted by {men} | manually reviewed") 
            await query.message.edit_text(text=denx, reply_markup=buttons, disable_web_page_preview=True)
        await save_vote(id, user)
    except Exception as e:
        print(e)
app.start()
print("Powered by aniwatch.to")
idle()

