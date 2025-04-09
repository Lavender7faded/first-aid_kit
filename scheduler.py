import schedule
import time
from datetime import datetime, timedelta

from app.routes import app
from app.models import Medicine
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

        if expiring or low_quantity:
            print("⚠️ Alerts detected:")
            for m in expiring:
                print(f"  • {m.name} expires on {m.expiration_date}")
            for m in low_quantity:
                print(f"  • {m.name} has only {m.quantity} left")
        else:
            print("✅ All medicines are OK.")

# Run daily at 09:00
schedule.every().day.at("09:00").do(check_alerts)

if __name__ == "__main__":
    print("📅 Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)

