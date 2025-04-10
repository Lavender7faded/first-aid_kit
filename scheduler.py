import schedule
import time
from datetime import datetime, timedelta, date

from app.routes import app
from app.models import Medicine, Alert
from app import db, mail

from flask_mail import Message

def send_alert_email(message):
    msg = Message(
        subject="⚠️ Pharmacy Alert", 
        recipients=["ann.kh18@gmail.com"]  # Ваша реальна email-адреса
    )
    
    # Оформлення листа у HTML
    msg.html = f"""
    <html>
        <body>
            <p style="font-size: 16px; color: #333; font-weight: normal;">{message}</p>
            <hr>
            <p style="font-size: 14px; color: #888; font-style: italic;">This is an automated message from the First-aid kit.</p>
        </body>
    </html>
    """
    mail.send(msg)

def check_alerts():
    with app.app_context():
        today = date.today()
        deadline = today + timedelta(days=7)

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
            send_alert_email(message)

        # Додаємо сповіщення для ліків, термін придатності яких наближається
        for m in expiring:
            message = f"⚠️ {m.name} скоро зіпсується! Термін придатності: {m.expiration_date.strftime('%Y-%m-%d')}"
            print(message)
            db.session.add(Alert(message=message))
            send_alert_email(message)

        # Додаємо сповіщення для ліків з низькою кількістю
        for m in low_quantity:
            message = f"⚠️ {m.name} має лише {m.quantity} шт. залишилось. Це нижче мінімального порогу!"
            print(message)
            db.session.add(Alert(message=message))
            send_alert_email(message)

        db.session.commit()

        if not expired and not expiring and not low_quantity:
            print("✅ Усі ліки в нормі.")


# Run daily at 09:00
schedule.every().day.at("09:00").do(check_alerts)

if __name__ == "__main__":
    print("📅 Scheduler started...")
    check_alerts()
    while True:
        schedule.run_pending()
        time.sleep(60)
