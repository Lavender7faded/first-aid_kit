import schedule
import time
from datetime import datetime, timedelta

from app.routes import app
from app.models import Medicine, Alert
from app import db

def check_alerts():
    with app.app_context():
        today = datetime.today().date()
        deadline = today + timedelta(days=7)

        expiring = Medicine.query.filter(
            Medicine.expiration_date <= deadline,
            Medicine.expiration_date >= today
        ).all()

        low_quantity = Medicine.query.filter(
            Medicine.quantity <= 3
        ).all()

        for m in expiring:
            message = f"{m.name} expires on {m.expiration_date}"
            print(f"⚠️ {message}")
            db.session.add(Alert(message=message))

        for m in low_quantity:
            message = f"{m.name} has only {m.quantity} left"
            print(f"⚠️ {message}")
            db.session.add(Alert(message=message))

        db.session.commit()

        if not expiring and not low_quantity:
            print("✅ All medicines are OK.")


# Run daily at 09:00
schedule.every().day.at("09:00").do(check_alerts)

if __name__ == "__main__":
    print("📅 Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)

