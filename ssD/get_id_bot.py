from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
from token_all import YOUR_ADMIN_BOT_TOKEN

# Настройки логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен вашего бота
YOUR_BOT_TOKEN = YOUR_ADMIN_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    logging.info(f"Received /start command from user ID: {user_id}")
    await update.message.reply_text(f"Ваш Telegram ID: {user_id}")

def main():
    application = Application.builder().token(YOUR_BOT_TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    logging.info("Bot is running...")

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
