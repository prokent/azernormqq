# user_bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from models import User, Recruiter, Message, engine
from sqlalchemy.orm import sessionmaker
from token_all import YOUR_USER_BOT_TOKEN
import logging

# Настройки логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = YOUR_USER_BOT_TOKEN
Session = sessionmaker(bind=engine)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    session = Session()

    db_user = session.query(User).filter_by(telegram_id=user.id).first()
    if not db_user:
        db_user = User(telegram_id=user.id)
        session.add(db_user)
        session.commit()

    await update.message.reply_text("Здравствуйте! Ожидайте, пока рекрутер с вами свяжется.")
    logging.info(f"User {user.id} started. Notifying recruiters.")

    recruiter = session.query(Recruiter).filter_by(available=True).first()

    if recruiter:
        await context.bot.send_message(
            chat_id=recruiter.telegram_id,
            text=f"Новый пользователь ожидает вашего ответа. ID пользователя: {user.id}"
        )
        logging.info(f"Notified recruiter {recruiter.telegram_id} about user {user.id}")

        db_message = Message(user_id=db_user.id, content="Ожидает ответа рекрутера", recruiter_id=None)
        session.add(db_message)
        session.commit()

        recruiter.available = False
        session.commit()
    else:
        await update.message.reply_text("К сожалению, сейчас нет свободных рекрутеров.")
        logging.info("No available recruiters.")

    session.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    user = update.message.from_user

    session = Session()
    db_user = session.query(User).filter_by(telegram_id=user.id).first()
    if db_user:
        db_message = Message(user_id=db_user.id, content=message, recruiter_id=None)
        session.add(db_message)
        session.commit()
        logging.info(f"User {user.id} sent a message.")
    else:
        logging.info(f"User {user.id} not found.")

    session.close()

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("User bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
