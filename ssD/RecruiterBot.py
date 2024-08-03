# recruiter_bot.py

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from models import Recruiter, engine
from sqlalchemy.orm import sessionmaker
import logging

# Настройки логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = YOUR_ADMIN_BOT_TOKEN
Session = sessionmaker(bind=engine)

async def add_recruiter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        recruiter_name = ' '.join(context.args)
        session = Session()

        # Проверка на существование рекрутера
        existing_recruiter = session.query(Recruiter).filter_by(name=recruiter_name).first()
        if existing_recruiter:
            await update.message.reply_text(f"Рекрутер с именем {recruiter_name} уже существует.")
            session.close()
            return

        # Добавление рекрутера в базу данных
        new_recruiter = Recruiter(name=recruiter_name, telegram_id=update.message.from_user.id)
        session.add(new_recruiter)
        session.commit()
        session.close()

        await update.message.reply_text(f"Рекрутер {recruiter_name} успешно добавлен в базу данных.")
    else:
        await update.message.reply_text("Пожалуйста, укажите имя рекрутера. Пример: /add_recruiter Иван Иванов")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("add_recruiter", add_recruiter))

    logging.info("Recruiter bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
