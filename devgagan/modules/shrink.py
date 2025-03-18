 
# ---------------------------------------------------
# File Name: shrink.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import *
import random
import requests
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AUTH_CHANNEL, AD_API, LOG_GROUP  
 
 
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f"✇ Join {chat.title} ✇", url=chat.invite_link)]) #✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇
        except Exception as e:
            pass
    return btn

async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)
 
 
 
Param = {}
 
 
async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
 
 
async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
 
     
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()   
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None
 
 
async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None
 

@app.on_message(filters.command("start"))
async def token_handler(client, message):
    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message, AUTH_CHANNEL)
            if btn:
                username = (await client.get_me()).username
                if len(message.command) > 1:
                    btn.append([InlineKeyboardButton("🔄 Refresh", callback_data="refresh_check")])
                else:
                    btn.append([InlineKeyboardButton("🔄 Refresh ♻️", callback_data="refresh_check")])

                await message.reply_photo(
                    photo="https://i.ibb.co/WvQdtkyB/photo-2025-03-01-11-42-50-7482697636613455884.jpg",  # Replace with your image link
                    caption=(
                        f"<b>👋 Hello {message.from_user.mention},\n\n"
                        "If you want to use me, you must first join our updates channel. "
                        "Click on \"✇ Join Our Updates Channel ✇\" button. Then click on the \"Request to Join\" button. "
                        "After joining, click on \"Try Again\" button.</b>"
                    ),
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return  # ✅ Return added here to stop further execution if not subscribed
        except Exception as e:
            print(e)
            return  # ✅ Return added to prevent further execution in case of exception

    # ✅ Handle the /start command when user is subscribed
    join = await subscribe(client, message)
    if join == 1:
        return  # ✅ যদি ইউজার সাবস্ক্রাইব না করে, তাহলে কিছুই হবে না

    chat_id = "Prime_Botz"
    msg = await client.get_messages(chat_id, 42)

    user_id = message.chat.id
    if len(message.command) <= 1:
        image_url = "https://i.postimg.cc/SQVw7HCz/photo-2025-03-17-09-39-48-7482710873702662152.jpg"
        join_button = InlineKeyboardButton("Join Channel", url="https://t.me/Prime_Botz")
        premium = InlineKeyboardButton("Get Premium", url="https://t.me/Ig_1Venom")

        keyboard = InlineKeyboardMarkup([
            [join_button],
            [premium]
        ])

        await message.reply_photo(
            image_url,  # ✅ সরাসরি URL ব্যবহার করা হয়েছে
            caption=(
                "**Hi 👋 Welcome**\n\n"
                "**✳️ I can save posts from Channels or Groups where forwarding is off.**\n"
                "**✳️ Simply send the post link of a public channel.**\n"
                "**✳️ For private channels, You'll Have To Login. Send /help to know more.**"
            ),
            reply_markup=keyboard
)
        return  # ✅ Return added at the end to ensure proper flow
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
 
     
    if param:
        if user_id in Param and Param[user_id] == param:
             
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=20),
            })
            del Param[user_id]   
            await message.reply("✅ You have been verified successfully! Enjoy your session for next 20 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return
 

@app.on_callback_query(filters.regex("refresh_check"))  
async def refresh_callback(client: Client, query: CallbackQuery):  
    user_id = query.from_user.id  
    subscribed = await is_subscribed(client, user_id, AUTH_CHANNEL)  

    if subscribed:  
        await query.answer("✅ Thank you for joining! Now You Can Use Me if you face any problem then click to /help", show_alert=True)  
    else:  
        await query.answer("❌ You have not joined yet. Please join first, then refresh.", show_alert=True)
     
