import os
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)

# Lấy API Key từ biến môi trường (bảo mật hơn)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not TELEGRAM_TOKEN or not GENAI_API_KEY:
    raise ValueError("❌ Thiếu API Token! Hãy đặt biến môi trường TELEGRAM_TOKEN và GENAI_API_KEY.")

# Cấu hình Gemini AI
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

BOT_NAME = "1440 Support"
BOT_CREATOR = "Trương Công Bình"

# Hàm chat xử lý tin nhắn
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower().strip()
    if user_message in ["bạn là ai", "mày là ai", "bot là ai"]:
        bot_reply = f"🤖 Tôi là {BOT_NAME}, được {BOT_CREATOR} tạo ra để hỗ trợ bạn."
    else:
        response = model.generate_content(user_message)
        bot_reply = response.text if response else "❌ Tôi chưa có câu trả lời."

    await update.message.reply_text(bot_reply)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = f"🎉 Xin chào! Tôi là {BOT_NAME}, được tạo bởi {BOT_CREATOR}. Nhập /help để xem hướng dẫn."
    await update.message.reply_text(message)

# Lệnh /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "📌 Danh sách lệnh:\n"
        "/start - Giới thiệu bot\n"
        "/help - Xem danh sách lệnh\n"
        "/about - Thông tin về bot\n"
        "Hãy nhắn tin để tôi giúp bạn! 😊"
    )
    await update.message.reply_text(message)

# Lệnh /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = f"ℹ️ Tôi là {BOT_NAME}, được phát triển bởi {BOT_CREATOR} để hỗ trợ bạn."
    await update.message.reply_text(message)

# Hàm khởi động bot
async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot đang chạy...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
