import os
import logging
import google.generativeai as genai
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import nest_asyncio
nest_asyncio.apply()


# Lấy Token từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Cấu hình Google Gemini AI
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

BOT_NAME = "1440 Support"
BOT_CREATOR = "Trương Công Bình"

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo bot Telegram
bot_app = Application.builder().token(TELEGRAM_TOKEN).build()

# Hàm xử lý tin nhắn từ người dùng
async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower().strip()

    if user_message in ["bạn là ai", "mày là ai", "bot là ai"]:
        bot_reply = f"🤖 Tôi là {BOT_NAME}, được {BOT_CREATOR} tạo ra để hỗ trợ bạn."
    else:
        response = model.generate_content(user_message)
        bot_reply = response.text if response else "❌ Lỗi khi xử lý yêu cầu."

    await update.message.reply_text(bot_reply)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"🎉 Xin chào! Tôi là {BOT_NAME}, do {BOT_CREATOR} phát triển.")

async def help_command(update: Update, context: CallbackContext) -> None:
    message = (
        "📌 Danh sách lệnh:\n"
        "/start - Giới thiệu bot\n"
        "/help - Hướng dẫn sử dụng\n"
        "/about - Thông tin về bot"
    )
    await update.message.reply_text(message)

async def about(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"ℹ️ Tôi là {BOT_NAME}, chatbot của {BOT_CREATOR}.")

# Thêm handler cho bot
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("help", help_command))
bot_app.add_handler(CommandHandler("about", about))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=f"https://your-render-url/{TELEGRAM_TOKEN}"
    )

if __name__ == "__main__":
    from threading import Thread
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
