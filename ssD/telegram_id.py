from models import Recruiter, engine
from sqlalchemy.orm import sessionmaker
from token_all import YOUR_ADMIN_BOT_TOKEN

Session = sessionmaker(bind=engine)
session = Session()

# Замените 'USER_TELEGRAM_ID' на реальный ID
user_telegram_id = 5433647570
recruiter_name = "Serum"

new_recruiter = Recruiter(name=recruiter_name, telegram_id=user_telegram_id)
session.add(new_recruiter)
session.commit()

session.close()
