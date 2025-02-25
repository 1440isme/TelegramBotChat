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

# Kiểm tra API key trước khi chạy
if not TELEGRAM_TOKEN or not GENAI_API_KEY:
    raise ValueError("❌ Thiếu API Token! Hãy đặt biến môi trường TELEGRAM_TOKEN và GENAI_API_KEY.")

# Cấu hình Gemini AI
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Thông tin bot
BOT_NAME = "1440 Support"
BOT_CREATOR = "Trương Công Bình"

# Xử lý tin nhắn người dùng
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower().strip()

    # Kiểm tra câu hỏi về bot
    if user_message in ["bạn là ai", "mày là ai", "bot là ai"]:
        bot_reply = f"🤖 Tôi là {BOT_NAME}, được {BOT_CREATOR} tạo ra để hỗ trợ bạn."
    else:
        # Gọi Google Gemini API
        response = model.generate_content(user_message)
        bot_reply = response.text if response else "❌ Xin lỗi, tôi không thể trả lời ngay bây giờ."

    # Gửi phản hồi
    await update.message.reply_text(bot_reply)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = f"🎉 Xin chào! Tôi là {BOT_NAME}, được tạo bởi {BOT_CREATOR}. Hãy nhập /help để xem danh sách lệnh!"
    await update.message.reply_text(message)

# Lệnh /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "📌 Danh sách lệnh:\n"
        "/start - Giới thiệu bot\n"
        "/help - Xem danh sách lệnh\n"
        "/about - Thông tin về bot\n"
        "Bạn có thể gửi bất kỳ tin nhắn nào, tôi sẽ cố gắng giúp bạn! 😊"
    )
    await update.message.reply_text(message)

# Lệnh /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = f"ℹ️ Tôi là {BOT_NAME}, một chatbot thông minh do {BOT_CREATOR} phát triển. Tôi có thể trả lời câu hỏi, hỗ trợ tìm kiếm và nhiều thứ khác!"
    await update.message.reply_text(message)

# Hàm khởi động bot
async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Thêm lệnh
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot đang chạy...")
    await app.run_polling()

# Chạy bot an toàn với asyncio trên Python 3.12
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
        else:
            raise
