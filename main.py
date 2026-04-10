import os
import threading
import asyncio

# === YAHI HAI ASLI FIX ===
# Render ka naya Python 3.14 bina Event Loop ke Pyrogram ko import nahi hone deta.
# Isliye hum import se pehle hi zabardasti ek naya loop bana rahe hain.
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# =========================

from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. DUMMY WEB SERVER (Render ke liye) ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is perfectly running on Render!")
        
    def log_message(self, format, *args):
        pass

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, DummyHandler)
    print(f"🌐 Web Server started on port {port}")
    httpd.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()


# --- 2. AAPKA TELEGRAM BOT CODE ---
API_ID = 33603340
API_HASH = "0f1a7f670519f9e44d0d7fdb6aa8efba"
BOT_TOKEN = "7874642792:AAF08vl1-qcMUHOIUZrL5IwJS1A7zoD5ucw"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

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


@app.on_message(filters.command("acceptall") & filters.admin)
async def approve_all_requests(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("Saari pending requests approve ho rahi hain... thoda wait karein.")
    try:
        await client.approve_all_chat_join_requests(chat_id)
        await msg.edit_text("✅ Sabhi pending requests ko successfully channel members bana diya gaya hai!")
    except Exception as e:
        await msg.edit_text(f"❌ Error aaya: {e}")

# Bot ko Start karna
print("🚀 BOT IS STARTING NOW...")
app.run()
