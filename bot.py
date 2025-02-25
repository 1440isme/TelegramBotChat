import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lấy Token từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Cấu hình Google Gemini AI
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

BOT_NAME = "1440 Support"
BOT_CREATOR = "Trương Công Bình"

# Khởi tạo bot Telegram
bot_app = Application.builder().token(TELEGRAM_TOKEN).build()

# Hàm xử lý tin nhắn từ người dùng
async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower().strip()

    if user_message in ["bạn là ai", "mày là ai", "bot là ai", "bạn tên gì", "mày tên gì", "bot tên gì"]:
        bot_reply = f"🤖 Tôi là {BOT_NAME}, được {BOT_CREATOR} tạo ra để hỗ trợ bạn."
    else:
        try:
            response = model.generate_content(user_message)
            bot_reply = response.text if response else "❌ Lỗi khi xử lý yêu cầu."
        except Exception as e:
            logger.error(f"Lỗi AI: {e}")
            bot_reply = "❌ Lỗi xử lý AI."

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


async def run_bot():
    await bot_app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())  # Cách chạy đúng trên Python 3.12
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(run_bot())  # Dùng task nếu loop đã chạy
        else:
            raise