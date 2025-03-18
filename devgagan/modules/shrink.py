from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.errors import UserNotParticipant
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

# ✅ চেক করবে ইউজার সব চ্যানেলে জয়েন করেছে কিনা
async def is_subscribed(bot, user_id, channels):
    for channel in channels:
        try:
            await bot.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return False  # ✅ যদি একটিতেও না থাকে তাহলে False রিটার্ন করবে
        except Exception:
            return False  # ✅ অন্য কোনো সমস্যা হলে False রিটার্ন করবে
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
@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    subscribed = await is_subscribed(client, user_id, AUTH_CHANNEL)

    if not subscribed:
        btn = []
        for channel in AUTH_CHANNEL:
            chat = await client.get_chat(channel)
            btn.append([InlineKeyboardButton(f"✇ Join {chat.title} ✇", url=chat.invite_link)])
        btn.append([InlineKeyboardButton("🔄 Refresh", callback_data="refresh_check")])

        # ✅ বাধ্যতামূলক চ্যানেল জয়েন করতে বলবে
        sent_msg = await message.reply_photo(
            photo="https://i.ibb.co/WvQdtkyB/photo-2025-03-01-11-42-50-7482697636613455884.jpg",
            caption=(
                f"<b>👋 Hello {message.from_user.mention},\n\n"
                "If you want to use me, you must first join our updates channel. "
                "Click on \"✇ Join Our Updates Channel ✇\" button. Then click on the \"Request to Join\" button. "
                "After joining, click on \"Refresh\" button.</b>"
            ),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return  # ✅ ফোর্স সাবস্ক্রিপশন ব্যতীত আর কিছুই চলবে না

    # ✅ ইউজার যদি সব চ্যানেলে জয়েন করে থাকে তাহলে বাকি প্রসেস চলবে
    chat_id = "Prime_Botz"
    msg = await client.get_messages(chat_id, 42)

    image_url = "https://i.postimg.cc/SQVw7HCz/photo-2025-03-17-09-39-48-7482710873702662152.jpg"
    join_button = InlineKeyboardButton("Join Channel", url="https://t.me/Prime_Botz")
    premium = InlineKeyboardButton("Get Premium", url="https://t.me/Ig_1Venom")

    keyboard = InlineKeyboardMarkup([
        [join_button],
        [premium]
    ])

    await message.reply_photo(
        image_url,
        caption=(
            "**Hi 👋 Welcome**\n\n"
            "**✳️ I can save posts from Channels or Groups where forwarding is off.**\n"
            "**✳️ Simply send the post link of a public channel.**\n"
            "**✳️ For private channels, You'll Have To Login. Send /help to know more.**"
        ),
        reply_markup=keyboard
    )
    return  # ✅ সব ঠিক থাকলে বাকি মেসেজ চলবে

# ✅ রিফ্রেশ বাটনের ফাংশন
@app.on_callback_query(filters.regex("refresh_check"))  
async def refresh_callback(client: Client, query: CallbackQuery):  
    user_id = query.from_user.id  
    subscribed = await is_subscribed(client, user_id, AUTH_CHANNEL)  

    if subscribed:
        # ✅ যদি ইউজার চ্যানেলে জয়েন থাকে, তাহলে পুরাতন মেসেজ ডিলিট করে নতুন মেসেজ দেবে
        await query.message.delete()  
        await query.message.reply_text(
            "✅ Thank you for joining! Now you can use me.\n\nIf you face any problem, type /help"
        )
    else:
        # ❌ যদি ইউজার জয়েন না করে থাকে, তাহলে পপ-আপ দেখাবে
        await query.answer("❌ You have not joined yet. Please join first, then refresh.", show_alert=True)

# ✅ যেকোনো কমান্ড, টেক্সট, মিডিয়া পাঠানোর সময় ফোর্স চেক করবে
@app.on_message(filters.text | filters.command | filters.media)
async def force_subscription_check(client, message):
    user_id = message.from_user.id
    subscribed = await is_subscribed(client, user_id, AUTH_CHANNEL)

    if not subscribed:
        btn = []
        for channel in AUTH_CHANNEL:
            chat = await client.get_chat(channel)
            btn.append([InlineKeyboardButton(f"✇ Join {chat.title} ✇", url=chat.invite_link)])
        btn.append([InlineKeyboardButton("🔄 Refresh", callback_data="refresh_check")])

        # ✅ বাধ্যতামূলক চ্যানেল জয়েন করতে বলবে
        sent_msg = await message.reply_photo(
            photo="https://i.ibb.co/WvQdtkyB/photo-2025-03-01-11-42-50-7482697636613455884.jpg",
            caption=(
                f"<b>👋 Hello {message.from_user.mention},\n\n"
                "If you want to use me, you must first join our updates channel. "
                "Click on \"✇ Join Our Updates Channel ✇\" button. Then click on the \"Request to Join\" button. "
                "After joining, click on \"Refresh\" button.</b>"
            ),
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return  # ✅ ফোর্স সাবস্ক্রিপশন ব্যতীত আর কিছুই চলবে না

    # ✅ ইউজার যদি চ্যানেলে জয়েন করে থাকে তাহলে বট তার স্বাভাবিক নিয়মে চলবে
    await app.process_message(message)
