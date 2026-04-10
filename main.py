import os
import sys
import traceback
import asyncio

# === PYTHON 3.14 FIX (Ye Render ke naye Python ko handle karega) ===
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# ====================================================================

from aiohttp import web
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 33603340
API_HASH = "0f1a7f670519f9e44d0d7fdb6aa8efba"
BOT_TOKEN = "7874642792:AAF08vl1-qcMUHOIUZrL5IwJS1A7zoD5ucw"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# --- /start Command aur Button ---
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    bot = await client.get_me()
    add_link = f"https://t.me/{bot.username}?startchannel=true&admin=invite_users"
    
    text = (
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "Main ek **Auto Request Approver Bot** hoon.\n"
        "Main aapke channel ki saari pending join requests ko ek second mein accept kar sakta hoon.\n\n"
        "🚀 **Kaise Use Karein:**\n"
        "1. Neeche diye button par click karein.\n"
        "2. Apna Channel select karein.\n"
        "3. Mujhe **Admin** banayein.\n"
        "4. Channel mein aakar `/acceptall` type karein.\n"
    )
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("➕ Add Bot To Channel ➕", url=add_link)]])
    await message.reply_text(text, reply_markup=keyboard)


# --- /acceptall Command ---
@app.on_message(filters.command("acceptall") & filters.admin)
async def approve_all_requests(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("Saari pending requests approve ho rahi hain... thoda wait karein.")
    try:
        await client.approve_all_chat_join_requests(chat_id)
        await msg.edit_text("✅ Sabhi pending requests ko successfully channel members bana diya gaya hai!")
    except Exception as e:
        await msg.edit_text(f"❌ Error aaya: {e}")


# --- Web Server (Sabse pehle ye chalega taaki Render khush rahe) ---
async def web_server():
    async def handle(request):
        return web.Response(text="Bot is running smoothly on Render!")
    webapp = web.Application()
    webapp.router.add_get('/', handle)
    runner = web.AppRunner(webapp)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Web Server started on port {port}", flush=True)


# --- Main Logic ---
async def main():
    # 1. Pehle server start hoga taaki Render crash na kare
    print("⏳ Web Server Start ho raha hai...", flush=True)
    await web_server()
    
    # 2. Phir Telegram connect hoga
    print("⏳ Telegram se connect ho raha hai...", flush=True)
    await app.start()
    
    print("🎉 BOT IS LIVE NOW! SAB PERFECT HAI!", flush=True)
    await idle()
    await app.stop()


if __name__ == "__main__":
    print("🚀 Script Start Hui...", flush=True)
    try:
        # loop.run_until_complete use kiya hai taaki naya loop na banaye
        loop.run_until_complete(main())
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}", flush=True)
        traceback.print_exc()
