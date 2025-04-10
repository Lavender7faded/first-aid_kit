import schedule
import time
from datetime import datetime, timedelta, date

from app.routes import app
from app.models import Medicine, Alert
from app import db

def check_alerts():
    with app.app_context():
        today = date.today()
        deadline = today + timedelta(days=7)

        # # Тестові ліки з минулим терміном придатності
        # expired_meds = Medicine(name='ExpiredMed', quantity=5, expiration_date=today - timedelta(days=1))
        # db.session.add(expired_meds)
        # db.session.commit()

        # Перевірка ліків, термін придатності яких минув
        expired = Medicine.query.filter(Medicine.expiration_date < today).all()

        # Перевірка ліків, термін придатності яких наближається
        expiring = Medicine.query.filter(
            Medicine.expiration_date <= deadline,
            Medicine.expiration_date >= today
        ).all()

        low_quantity = Medicine.query.filter(Medicine.quantity <= 3).all()

        # Додаємо сповіщення для прострочених ліків
        for m in expired:
            message = f"⚠️ {m.name} прострочено! Термін придатності: {m.expiration_date.strftime('%Y-%m-%d')}"
            print(message)
            db.session.add(Alert(message=message))

        # Додаємо сповіщення для ліків, термін придатності яких наближається
        for m in expiring:
            message = f"⚠️ {m.name} скоро зіпсується! Термін придатності: {m.expiration_date.strftime('%Y-%m-%d')}"
            print(message)
            db.session.add(Alert(message=message))

        # Додаємо сповіщення для ліків з низькою кількістю
        for m in low_quantity:
            message = f"⚠️ {m.name} має лише {m.quantity} шт. залишилось. Це нижче мінімального порогу!"
            print(message)
            db.session.add(Alert(message=message))

        db.session.commit()

        if not expired and not expiring and not low_quantity:
            print("✅ Усі ліки в нормі.")


# Run daily at 09:00
schedule.every().day.at("09:00").do(check_alerts)

if __name__ == "__main__":
    print("📅 Scheduler started...")
    # check_alerts()
    while True:
        schedule.run_pending()
        time.sleep(60)

