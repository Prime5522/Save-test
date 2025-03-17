# ---------------------------------------------------
# File Name: start.py
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

from pyrogram import filters
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import subscribe
import asyncio
from devgagan.core.func import *
from pyrogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, 
    BotCommand, InputMediaPhoto  # ✅ নতুন Import করা হয়েছে
)
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf

QR_IMAGE_URL = "https://i.ibb.co/dZN26Kx/photo-2024-09-23-02-57-05-7482607940516446216.jpg"

@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("freez", "🧊 Remove all expired user"),
        BotCommand("status", "⟳ Refresh Payment status"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("stats", "📊 Get stats of the bot"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "🥺 Terms and conditions"),
        BotCommand("speedtest", "🚅 Speed of server"),
        BotCommand("lock", "🔒 Protect channel from extraction"),
        BotCommand("gcast", "⚡ Broadcast message to bot users"),
        BotCommand("help", "❓ If you're a noob, still!"),
        BotCommand("cancel", "🚫 Cancel batch process")
    ])
 
    await message.reply("✅ Commands configured successfully!")
 
 
 
 
help_pages = [
    (
        "📝 **Read Bot Commands & Features **:\n\n"
     """** This is a very Powerful And Advanced Content Saver Bot\n
     Using This Bot Can You Save Content from The Pivate Or Pubic Channels and Groups Where Copying and forwarding Is off.\n
    → For Public Channels You Can Just Send Me The link.\n
    → But for Private Channels You'll Have to Login Your Telegram Account(Make Sure to Logout from The Bot After Your Job is Done)\n**
"""       
        "1. **/batch**\n"
        "> Bulk extraction for posts (After login)\n\n"
        "2. **/cancel**\n"
        "> Cancel ongoing batch process\n\n"
        "3. **/login**\n"
        "> Log into the bot for private channel access\n\n"
        "4. **/logout**\n"
        "> Logout from the bot\n\n"
        "5. **/myplan**\n"
        "> Get details about your plans\n\n"
        "6. **/plan**\n"
        "> Check premium plans\n\n"
        "7. **/transfer userID**\n"
        "> Transfer premium to your beloved major purpose for resellers (Premium members only)\n\n"
        "8. **/session**\n"
        "> Generate Pyrogram V2 session\n\n"
       
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "9. **/terms**\n"
        "> Terms and conditions\n\n"
        "10. **/speedtest**\n"
        "> Test the server speed (not available in v3)\n\n"
        "11. **/settings**\n"
        "> 1. SETCHATID : To directly upload in channel or group or user's dm use it with -100[chatID]\n"
        "> 2. SETRENAME : To add custom rename tag or username of your channels\n"
        "> 3. CAPTION : To add custom caption\n"
        "> 4. REPLACEWORDS : Can be used for words in deleted set via REMOVE WORDS\n"
        "> 5. RESET : To set the things back to default\n\n"
        "> You can set CUSTOM THUMBNAIL, SESSION-based login, etc. from settings\n\n"
    )
]
 
 
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return
 
     
    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")
 
     
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)
 
     
    keyboard = InlineKeyboardMarkup([buttons])
 
     
    await message.delete()
 
     
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )
 
 
@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
 
     
    await send_or_edit_help_page(client, message, 0)
 
 
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
 
    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1
 
     
    await send_or_edit_help_page(client, callback_query.message, page_number)
 
     
    await callback_query.answer()
 
 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
 
@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "** → Wᴇ ᴀʀᴇ ɴᴏᴛ ʀᴇsᴘᴏɴsɪʙʟᴇ ғᴏʀ ᴜsᴇʀ ᴅᴇᴇᴅs, ᴀɴᴅ ᴡᴇ ᴅᴏ ɴᴏᴛ ᴘʀᴏᴍᴏᴛᴇ ᴄᴏᴘʏʀɪɢʜᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ. Iғ ᴀɴʏ ᴜsᴇʀ ᴇɴɢᴀɢᴇs ɪɴ sᴜᴄʜ ᴀᴄᴛɪᴠɪᴛɪᴇs, ᴛʜᴇɴ ʜᴇ/sʜᴇ ɪs sᴏʟᴇʟʏ ʀᴇsᴘᴏɴsɪʙʟᴇ \n\n**"
        "** → Uᴘᴏɴ ᴘᴜʀᴄʜᴀsᴇ, ᴡᴇ ᴅᴏ ɴᴏᴛ ɢᴜᴀʀᴀɴᴛᴇᴇ ᴛʜᴇ ᴜᴘᴛɪᴍᴇ, ᴅᴏᴡɴᴛɪᴍᴇ, Oғ Bᴏᴛ \n\n **"
        "** → Aᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ᴀɴᴅ ʙᴀɴɴɪɴɢ ᴏғ ᴜsᴇʀs ᴀʀᴇ ᴀᴛ ᴏᴜʀ ᴅɪsᴄʀᴇᴛɪᴏɴ; ᴡᴇ ʀᴇsᴇʀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʙᴀɴ ᴏʀ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜsᴇʀs ᴀᴛ ᴀɴʏ ᴛɪᴍᴇ ** "
        
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Purchase Premium", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url="https://t.me/Prime_Bots_Support_RoBot")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)
 

PLAN_TEXT = (
    """> **🎖️ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ :**


╭━━━━━━━━━━╮
❏ ₹ 20 ৳ - 1 ᴡᴇᴇᴋ
❏ ₹ 35 ৳ - 2 ᴡᴇᴇᴋ
❏ ₹ 50 ৳ - 1 ᴍᴏɴᴛʜs
❏ ₹ 130 ৳ - 3 ᴍᴏɴᴛʜs
❏ ₹ 250 ৳ - 6 ᴍᴏɴᴛʜs
╰━━━━━━━━━━╯


╭━━━━━━━━━━╮
❏ 1 $ - 1 ᴍᴏɴᴛʜs
❏ 2 $ - 3 ᴍᴏɴᴛʜs
❏ 4 $ - 6 ᴍᴏɴᴛʜs
╰━━━━━━━━━━╯

💵 𝗔𝗡𝗬 𝗖𝗢𝗨𝗡𝗧𝗥𝗬 𝗔𝗟𝗟 𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗠𝗘𝗧𝗛𝗢𝗗 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘. যদি বিকাশ বা 𝗤𝗥 কোড ছাড়া অথবা অন্য কিছু মাধ্যমে\n পেমেন্ট করতে চাইলে অথবা আরো কিছু জানার থাকলে\n𝗖𝗢𝗡𝗡𝗘𝗖𝗧 𝗔𝗗𝗠𝗜𝗡 ➠ <a href=https://t.me/Prime_Admin_Support_ProBot >𝐌𝐑.𝐏𝐑𝐈𝐌𝐄</a> 

 
**⛽️ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan**

🏷️ <a href='https://t.me/Prime_Admin_Support_ProBot'>ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴏꜰ</a>

**‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.**
**‼️ ɢɪᴠᴇ ᴜꜱ ꜱᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴘʀᴇᴍɪᴜᴍ ʟɪꜱᴛ.**

📜 **Terms And Conditions Applied**"""
)

BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
        [InlineKeyboardButton("💬 Contact Admin", url="https://t.me/Prime_Bots_Support_RoBot")],
    ]
)

@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    await message.reply_photo(
        photo=QR_IMAGE_URL,
        caption=PLAN_TEXT,
        reply_markup=BUTTONS
    )


@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=QR_IMAGE_URL,
            caption=PLAN_TEXT
        ),
        reply_markup=BUTTONS
 )
 
@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
     "> 📜 **Terms and Conditions** 📜\n\n"
        "** → Wᴇ ᴀʀᴇ ɴᴏᴛ ʀᴇsᴘᴏɴsɪʙʟᴇ ғᴏʀ ᴜsᴇʀ ᴅᴇᴇᴅs, ᴀɴᴅ ᴡᴇ ᴅᴏ ɴᴏᴛ ᴘʀᴏᴍᴏᴛᴇ ᴄᴏᴘʏʀɪɢʜᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ. Iғ ᴀɴʏ ᴜsᴇʀ ᴇɴɢᴀɢᴇs ɪɴ sᴜᴄʜ ᴀᴄᴛɪᴠɪᴛɪᴇs, ᴛʜᴇɴ ʜᴇ/sʜᴇ ɪs sᴏʟᴇʟʏ ʀᴇsᴘᴏɴsɪʙʟᴇ \n\n**"
        "** → Uᴘᴏɴ ᴘᴜʀᴄʜᴀsᴇ, ᴡᴇ ᴅᴏ ɴᴏᴛ ɢᴜᴀʀᴀɴᴛᴇᴇ ᴛʜᴇ ᴜᴘᴛɪᴍᴇ, ᴅᴏᴡɴᴛɪᴍᴇ, Oғ Bᴏᴛ \n\n **"
        "** → Aᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ᴀɴᴅ ʙᴀɴɴɪɴɢ ᴏғ ᴜsᴇʀs ᴀʀᴇ ᴀᴛ ᴏᴜʀ ᴅɪsᴄʀᴇᴛɪᴏɴ; ᴡᴇ ʀᴇsᴇʀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʙᴀɴ ᴏʀ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜsᴇʀs ᴀᴛ ᴀɴʏ ᴛɪᴍᴇ **"
           
     
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Buy Premium", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Admin", url="https://t.me/Prime_Bots_Support_RoBot")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
 
 
