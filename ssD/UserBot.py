from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from models import User, Recruiter, Message, engine
from sqlalchemy.orm import sessionmaker
from token_all import YOUR_USER_BOT_TOKEN

TELEGRAM_TOKEN = YOUR_USER_BOT_TOKEN
Session = sessionmaker(bind=engine)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.message:
            chat_id = update.effective_chat.id
            user = update.message.from_user
            session = Session()

            # Добавление пользователя в базу данных, если его там нет
            db_user = session.query(User).filter_by(telegram_id=user.id).first()
            if not db_user:
                db_user = User(telegram_id=user.id)
                session.add(db_user)
                session.commit()

            # Выбор свободного рекрутера
            recruiter = session.query(Recruiter).filter_by(available=True).first()

            if recruiter:
                if recruiter.telegram_id:
                    await context.bot.send_message(chat_id=chat_id, text=f"Ваш персональный рекрутёр: {recruiter.name}")

                    # Отправка уведомления рекрутеру через его бот
                    recruiter_bot = Application.builder().token(recruiter.telegram_id).build()
                    await recruiter_bot.bot.send_message(
                        chat_id=recruiter.telegram_id,
                        text=f"Новый пользователь ожидает вашего ответа. ID пользователя: {user.id}"
                    )

                    # Сохранение сообщения пользователя для дальнейшей обработки
                    db_message = Message(user_id=db_user.id, content="Пользователь начал разговор.")
                    session.add(db_message)
                    session.commit()

                    recruiter.available = False
                    session.commit()
                else:
                    await context.bot.send_message(chat_id=chat_id, text="Рекрутер не имеет корректного telegram_id.")
            else:
                await context.bot.send_message(chat_id=chat_id, text="К сожалению, сейчас нет свободных рекрутеров.")

            session.close()
        else:
            print("Update does not contain a message or chat_id.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = update.message.text
        user = update.message.from_user

        session = Session()
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if db_user:
            # Сохранение сообщения пользователя для последующей обработки рекрутерами
            db_message = Message(user_id=db_user.id, content=message)
            session.add(db_message)
            session.commit()

        session.close()
    except Exception as e:
        print(f"An error occurred while handling message: {e}")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
