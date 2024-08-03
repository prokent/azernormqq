from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from models import Recruiter, User, Message, engine
from sqlalchemy.orm import sessionmaker
from token_all import YOUR_ADMIN_BOT_TOKEN

TELEGRAM_TOKEN = YOUR_ADMIN_BOT_TOKEN
Session = sessionmaker(bind=engine)


async def handle_recruiter_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    recruiter_id = update.message.from_user.id

    session = Session()

    # Найти сообщение пользователя, которому рекрутер еще не ответил
    db_message = session.query(Message).filter_by(recruiter_id=None).first()

    if db_message:
        # Отправка сообщения пользователю
        await context.bot.send_message(
            chat_id=db_message.user_id,
            text=message_text
        )

        # Обновление записи сообщения, чтобы указать, что рекрутер ответил
        db_message.recruiter_id = recruiter_id
        session.commit()
    else:
        # Если нет сообщений от пользователей, можно отправить сообщение рекрутеру
        await update.message.reply_text("В данный момент нет сообщений от пользователей.")

    session.close()


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчик сообщений рекрутера
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_recruiter_message))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
