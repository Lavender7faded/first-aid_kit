# test_scheduler.py  (один‑единственный файл)

import pytest
from datetime import date, timedelta
from unittest.mock import patch

from app import create_app, db
from app.models import Medicine, Alert
from scheduler import check_alerts


# ---------- фикстуры -------------------------------------------------
@pytest.fixture(scope='session')
def app():
    """Один Flask‑приложение на всю тест‑сессию."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # быстро и безопасно
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


@pytest.fixture(scope='session')
def setup_db(app):
    """Создаём таблицы один раз, удаляем в конце сессии."""
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


@pytest.fixture(autouse=True)
def clean_tables(setup_db, app):
    """Перед КАЖДЫМ тестом чистим данные, но не трогаем схему."""
    with app.app_context():
        for model in (Alert, Medicine):
            db.session.query(model).delete()
        db.session.commit()


# ---------- сами тесты ----------------------------------------------
def test_check_alerts_for_expired_medicines(app):
    with app.app_context():
        expired = Medicine(
            name='ExpiredMed',
            quantity=5,
            expiration_date=date.today() - timedelta(days=1)
        )
        db.session.add(expired)
        db.session.commit()

        check_alerts()

        alert = Alert.query.first()
        assert alert                              # запись создана
        assert "прострочено" in alert.message     # нужный текст
        assert expired.name in alert.message      # есть название


def test_send_email(app):
    with patch('scheduler.send_alert_email') as mock_send:
        with app.app_context():
            expired = Medicine(
                name='ExpiredMed',
                quantity=5,
                expiration_date=date.today() - timedelta(days=1)
            )
            db.session.add(expired)
            db.session.commit()

            check_alerts()

            expected = (
                f"⚠️ {expired.name} прострочено! "
                f"Термін придатності: {expired.expiration_date}"
            )
            mock_send.assert_called_once_with(expected)
