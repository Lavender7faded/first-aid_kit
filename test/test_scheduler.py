from datetime import date, timedelta

from app import app, db
from app.models import Medicine, Alert
from scheduler import check_alerts

def setup_function():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

def teardown_function():
    with app.app_context():
        db.drop_all()

def test_alerts_created_for_low_quantity_and_expiry():
    with app.app_context():
        # Створимо ліки з низькою кількістю та терміном
        med1 = Medicine(name='TestMed1', quantity=2, expiration_date=date.today() + timedelta(days=5))
        med2 = Medicine(name='TestMed2', quantity=10, expiration_date=date.today() + timedelta(days=20))
        med3 = Medicine(name='TestMed3', quantity=1, expiration_date=date.today() + timedelta(days=1))
        db.session.add_all([med1, med2, med3])
        db.session.commit()

        # Викликаємо перевірку
        check_alerts()

        # Має бути 2 або більше сповіщень
        alerts = Alert.query.all()
        assert len(alerts) >= 2

        messages = [a.message for a in alerts]
        assert any('TestMed1' in msg for msg in messages)
        assert any('TestMed3' in msg for msg in messages)
