from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram import enums
from pyrogram.errors import *
import random
import asyncio
import requests
import string
import aiohttp
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AUTH_CHANNEL, AD_API, LOG_GROUP  

# Importing from devgagan module
from devgagan import app
from devgagan.core.func import *  
from devgagan.core.get_func import get_msg  # Added get_msg function

tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

# ✅ চেক করবে ইউজার সব চ্যানেলে জয়েন করেছে কিনা
async def is_subscribed(bot, user_id, channels):
    for channel in channels:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            if chat_member.status in ["kicked", "banned"]:
                return False  # ✅ ব্যান থাকলে False রিটার্ন করবে
        except UserNotParticipant:
            return False  # ✅ ইউজার যদি না থাকে তাহলে False রিটার্ন করবে
        except ChatAdminRequired:
            continue  # ✅ যদি বট অ্যাডমিন না হয়, তাহলে স্কিপ করবে
        except Exception as e:
            print(f"Error in checking subscription: {e}")  # ✅ লগ রাখা হবে
            continue
    return True  # ✅ যদি সবগুলো চ্যানেলে জয়েন থাকে তাহলে True রিটার্ন করবে

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
 
# ✅ স্টার্ট কমান্ড (ফোর্স সাবস্ক্রিপশন বাধ্যতামূলক)
@app.on_message(filters.command(["start"]))  # সঠিক
async def start_command(client, message):
    user_id = message.from_user.id

    # Ensure AUTH_CHANNEL is a list
    if isinstance(AUTH_CHANNEL, str):
        AUTH_CHANNELS = [AUTH_CHANNEL]
    else:
        AUTH_CHANNELS = AUTH_CHANNEL

    # Check subscription
    subscribed = await is_subscribed(client, user_id, AUTH_CHANNELS)

    if not subscribed:
        btn = []
        for channel in AUTH_CHANNELS:
            try:
                chat = await client.get_chat(channel)
                invite_link = chat.invite_link or await client.export_chat_invite_link(channel)
                btn.append([InlineKeyboardButton(f"✇ Join {chat.title} ✇", url=invite_link)])
            except Exception as e:
                print(f"Error: {e}")

        btn.append([InlineKeyboardButton("🔄 Refresh", callback_data="refresh_check")])

        # Force subscription message
        await message.reply_photo(
            photo="https://i.ibb.co/WvQdtkyB/photo-2025-03-01-11-42-50-7482697636613455884.jpg",
            caption=(
                f"👋 Hello {message.from_user.mention},\n\n"
                "If you want to use me, you must first join our updates channel. "
                "Click on \"✇ Join Our Updates Channel ✇\" button. Then click on the \"Request to Join\" button. "
                "After joining, click on \"Refresh\" button."
            ),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return  

    # If subscribed, send the start message
    image_url = "https://i.ibb.co/Fb3dtYMF/photo-2025-03-20-12-41-28-7483870948664279044.jpg" #https://i.postimg.cc/SQVw7HCz/photo-2025-03-17-09-39-48-7482710873702662152.jpg
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✪ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ ✪", url="https://t.me/Prime_Support_group"), 
         InlineKeyboardButton("〄 ᴍᴏᴠɪᴇ ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/PRIMECINEZONE")],
        [InlineKeyboardButton("〆 ʜᴇʟᴘ 〆", callback_data="help"), 
         InlineKeyboardButton("〆 ᴀʙᴏᴜᴛ 〆", callback_data="about")],
        [InlineKeyboardButton("〄 ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ 〄", url="https://t.me/PrimeXBots")],
        [InlineKeyboardButton("✧ ᴄʀᴇᴀᴛᴏʀ ✧", url="https://t.me/Prime_Nayem")]
    ])

    await message.reply_photo(
        image_url,
        caption=(
        "🚀 **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ꜱᴀᴠᴇ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ ᴘʀɪᴍᴇʙᴏᴛ!**\n\n"
        "🔹 **ɪ ᴄᴀɴ ꜱᴀᴠᴇ ᴀɴᴅ ʀᴇᴛʀɪᴇᴠᴇ ᴘᴏꜱᴛꜱ** ꜰʀᴏᴍ ᴄʜᴀɴɴᴇʟꜱ ᴏʀ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ꜰᴏʀᴡᴀʀᴅɪɴɢ ɪꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ.\n"
        "🔹 **ꜱɪᴍᴘʟʏ ꜱᴇɴᴅ ᴍᴇ ᴀ ᴘᴏꜱᴛ ʟɪɴᴋ** ꜰʀᴏᴍ ᴀɴʏ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟ, ᴀɴᴅ ɪ'ʟʟ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ.\n"
        "🔹 **ꜰᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ**, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ **ʟᴏɢ ɪɴ** ᴛᴏ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ. (**help** ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ)\n\n"
        "🎯 **ᴡʜʏ ᴄʜᴏᴏꜱᴇ ᴍᴇ?**\n"
        "✅ **ᴀᴅᴠᴀɴᴄᴇᴅ ᴘᴏꜱᴛ ꜱᴇᴀʀᴄʜɪɴɢ & ꜰɪʟᴛᴇʀɪɴɢ**\n"
        "✅ **ᴡᴏʀᴋꜱ ꜰᴏʀ ʙᴏᴛʜ ᴘᴜʙʟɪᴄ & ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ**\n"
        "✅ **ꜰᴀꜱᴛ & ᴀᴄᴄᴜʀᴀᴛᴇ ʀᴇꜱᴜʟᴛꜱ**\n"
        "✅ **ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ**\n\n"
        "🔗 **ꜱᴛᴀʀᴛ ʙʏ ꜱᴇɴᴅɪɴɢ ᴀ ᴘᴏꜱᴛ ʟɪɴᴋ ɴᴏᴡ!**\n\n"
        "✨ **ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ:** **@PrimeXBots 🔥**"
    ),
    reply_markup=keyboard
    )
# ✅ হেল্প বাটন ফাংশন

@app.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query):
    help_text = """📝 **Read Bot Commands & Features:**

This is a very Powerful And Advanced Content Saver Bot

Using This Bot Can You Save Content from The Private Or Public Channels and Groups Where Copying and Forwarding Is off.

→ For Public Channels You Can Just Send Me The link.

→ But for Private Channels You'll Have to Login Your Telegram Account(Make Sure to Logout from The Bot After Your Job is Done)

1. /batch - Bulk extraction for posts (After login)
2. /cancel - Cancel ongoing batch process
3. /login - Log into the bot for private channel access
4. /logout - Logout from the bot
5. /myplan - Get details about your plans
6. /plan - Check premium plans
7. /transfer userID - Transfer premium to your beloved major purpose for resellers (Premium members only)
8. /session - Generate Pyrogram V2 session
9. /terms - Terms and conditions
10. /speedtest - Test the server speed (not available in v3)
11. /settings - Manage various settings.
You can set CUSTOM THUMBNAIL, SESSION-based login, etc. from settings."""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✪ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ ✪", url="https://t.me/Prime_Support_group")],
        [InlineKeyboardButton("⬅️ Back to Home", url="https://t.me/Save_Restricted_Content_PrimeBot?start=start")]
    ])

    await callback_query.message.edit_text(help_text, reply_markup=keyboard)

 
# ✅ এবাউট বাটন ফাংশন
@app.on_callback_query(filters.regex("about"))
async def about_callback(client, callback_query): 
    about_text = """
<b>⍟───[ <a href="https://t.me/PrimeXBots">ᴍy ᴅᴇᴛᴀɪʟꜱ ʙy ᴘʀɪᴍᴇXʙᴏᴛs</a> ]───⍟</b>

‣ <b>ᴍʏ ɴᴀᴍᴇ</b> : <a href="https://t.me/Save_Restricted_Content_PrimeBot">@Save_Restricted_Content_PrimeBot</a>  
‣ <b>ᴍʏ ʙᴇsᴛ ғʀɪᴇɴᴅ</b> : <a href="tg://settings">ᴛʜɪs ᴘᴇʀsᴏɴ</a>  
‣ <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ</b> : <a href="https://t.me/Prime_Nayem">ᴍʀ.ᴘʀɪᴍᴇ</a>  
‣ <b>ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ</b> : <a href="https://t.me/PrimeXBots">ᴘʀɪᴍᴇXʙᴏᴛꜱ</a>  
‣ <b>ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ</b> : <a href="https://t.me/PrimeCineZone">Pʀɪᴍᴇ Cɪɴᴇᴢᴏɴᴇ</a>  
‣ <b>ѕᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ</b> : <a href="https://t.me/Prime_Support_group">ᴘʀɪᴍᴇ X ѕᴜᴘᴘᴏʀᴛ</a>  
‣ <b>ᴅᴀᴛᴀ ʙᴀsᴇ</b> : <a href="https://www.mongodb.com/">ᴍᴏɴɢᴏ ᴅʙ</a>  
‣ <b>ʙᴏᴛ sᴇʀᴠᴇʀ</b> : <a href="https://heroku.com">ʜᴇʀᴏᴋᴜ</a>  
‣ <b>ʙᴜɪʟᴅ sᴛᴀᴛᴜs</b> : <code>ᴠ2.7.1 [sᴛᴀʙʟᴇ]</code>
"""

    keyboardn = InlineKeyboardMarkup([
        [InlineKeyboardButton("✪ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ ✪", url="https://t.me/Prime_Botz_Support")],
        [InlineKeyboardButton("〆 ʜᴇʟᴘ 〆", callback_data="help")]
    ])
 
    await callback_query.message.edit_text(
        about_text,
        reply_markup=keyboardn,
        parse_mode=enums.ParseMode.HTML
    )

# ✅ রিফ্রেশ বাটনের ফাংশন
@app.on_callback_query(filters.regex("refresh_check"))  
async def refresh_callback(client: Client, query: CallbackQuery):  
    user_id = query.from_user.id  
    subscribed = await is_subscribed(client, user_id, AUTH_CHANNEL)  

    if subscribed:
        # ✅ যদি ইউজার চ্যানেলে জয়েন থাকে, তাহলে পুরাতন মেসেজ ডিলিট করে নতুন মেসেজ দেবে
        await query.message.delete()  
        await query.message.reply_text(
            "✅ Thank You For Joining! Now You Can Use Me."
        )
    else:
        # ❌ যদি ইউজার জয়েন না করে থাকে, তাহলে পপ-আপ দেখাবে
        await query.answer("❌ You have not joined yet. Please join first, then refresh.", show_alert=True)



