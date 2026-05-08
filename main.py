import json
import os
import requests
import asyncio
from io import BytesIO
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, ChatJoinRequestHandler,
    CommandHandler
)

# ================= 🔐 SECRET CONFIGURATION 🔐 =================
# Token ko environment variable se uthaya ja raha hai security ke liye
BOT_TOKEN = os.getenv("BOT_TOKEN") 
BOT_USERNAME = "ADITYA_TRADERS_BOT"
ADMIN_ID = 7303219901 

# Baki saari details wesi ki wesi hain
VIP_CHANNEL_URL = "https://t.me/+Ros9SMvSf7tjYzY1"
REG_LINK = "https://yaarwin.org/#/register?invitationCode=67827139232"
APK_URL = "https://raw.githubusercontent.com/loda26616-a11y/Idk/121c33384333968420a69aeb74726b448cd2409f/ADITYA%20NUMBER%20PANEL.apk"
WELCOME_IMAGE_URL = "https://kommodo.ai/i/TWuoP7QT7CBfjDFN5Dtd"

USERS_FILE = "users_aditya.json"
APK_CACHE = None

# ================= 📂 DATABASE LOGIC 📂 =================
def load_users():
    if not os.path.exists(USERS_FILE): return []
    try:
        with open(USERS_FILE, "r") as f: return json.load(f)
    except: return []

def save_users(users):
    with open(USERS_FILE, "w") as f: json.dump(users, f, indent=2)

def add_user(user):
    users = load_users()
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id, 
            "username": user.username, 
            "first_name": user.first_name, 
            "joined_at": datetime.now().isoformat()
        })
        save_users(users)

# ================= ⚡ STABILITY & MEDIA ⚡ =================
def fetch_apk():
    global APK_CACHE
    try:
        print("📥 ✅ Fetching Aditya Premium APK...")
        res = requests.get(APK_URL, timeout=120)
        res.raise_for_status()
        APK_CACHE = res.content
        print("🌟 ✅ APK Cached in RAM!")
    except Exception as e:
        print(f"❌ APK Error: {e}")

async def send_fast_media(user_id, context):
    try:
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("👑 JOIN VIP CHANNEL 🔥", url=VIP_CHANNEL_URL)]])
        
        photo_msg = context.bot.send_photo(
            chat_id=user_id,
            photo=WELCOME_IMAGE_URL,
            caption="🚀 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗔𝗗𝗜𝗧𝗬𝗔 𝗧𝗥𝗔𝗗𝗘𝗥𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧 🚀\n\n✅ Your Request Received! Download Hack Below ⬇️",
            reply_markup=btn
        )

        if APK_CACHE:
            file = BytesIO(APK_CACHE)
            file.name = "ADITYA_NUMBER_PANEL.apk"
            caption_text = (
                "💰 MAA KSM NUMBER HACK WIN 👑\n\n"
                "💯 REGISTER LINK 💸\n"
                f"{REG_LINK}\n\n"
                "💥 DM FOR VIP CHANNEL 📈\n"
                "⏩ @ADDI_XO\n"
                "⏩ @ADDI_XO\n\n"
                "🌟 POWERED BY ADITYA TRADERS ✅"
            )
            apk_msg = context.bot.send_document(
                chat_id=user_id,
                document=file,
                caption=caption_text,
                reply_markup=btn
            )
            await asyncio.gather(photo_msg, apk_msg)
    except Exception as e:
        print(f"⚠️ Media Error: {e}")

# ================= 🤖 HANDLERS 🤖 =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user)
    try:
        if context.args and context.args[0] == "apk":
            await send_fast_media(user.id, context)
        else:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔥 GET PREMIUM APK 💰", url=f"https://t.me/{BOT_USERNAME}?start=apk")]])
            await update.message.reply_text(f"🌟 Hello {user.first_name}!\n💯 Welcome to ADITYA TRADERS.", reply_markup=btn)
    except: pass

async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Auto-Approve band hai as per instructions
    user = update.chat_join_request.from_user
    add_user(user)
    await send_fast_media(user.id, context)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    users = load_users()
    await update.message.reply_text(f"📈 **STATISTICS** 📈\n\n👑 Total Users: {len(users)}\n✅ Status: Running 24/7")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or not update.message.reply_to_message:
        return
    users = load_users()
    msg = update.message.reply_to_message
    sent = 0
    status = await update.message.reply_text("💥 **Broadcasting...**")
    for u in users:
        try:
            await msg.copy(chat_id=u["id"])
            sent += 1
            await asyncio.sleep(0.05)
        except: continue
    await status.edit_text(f"✅ Sent to {sent} users.")

# ================= 🚀 RUNNER 🚀 =================
def main():
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN not found in environment variables!")
        return
    
    fetch_apk()
    app = ApplicationBuilder().token(BOT_TOKEN).connect_timeout(40).read_timeout(40).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(ChatJoinRequestHandler(join_request))

    print(f"🚀 @{BOT_USERNAME} IS NOW STABLE AND RUNNING!")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
