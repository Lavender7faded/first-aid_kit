from app import app, db
import pytest

# ✅ 1. Базовий тест
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_add_medicine(client):
    response = client.post('/medicines', json={
        "name": "Тестовий препарат",
        "expiration_date": "2025-12-31",
        "quantity": 5,
        "description": "Тестовий опис"
    })
    response_json = response.get_json()
    assert response.status_code == 201
    assert "Препарат успішно додано" in response_json["message"]

# 📥 2. Перегляд усіх ліків (GET /medicines)
def test_get_medicines(client):
    # Спочатку додаємо препарат
    client.post('/medicines', json={
        "name": "Ібупрофен",
        "expiration_date": "2025-11-01",
        "quantity": 8,
        "description": "Жарознижувальне"
    })
    
    # Отримуємо список
    response = client.get('/medicines')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert any(med['name'] == "Ібупрофен" for med in data)

# ✏️ 3. Оновлення (PUT /medicines/<id>)
def test_update_medicine(client):
    # Створення
    post_resp = client.post('/medicines', json={
        "name": "Анальгін",
        "expiration_date": "2025-10-10",
        "quantity": 3,
        "description": ""
    })
    med_id = post_resp.get_json()['id']

    # Оновлення
    put_resp = client.put(f'/medicines/{med_id}', json={
        "quantity": 7
    })

    assert put_resp.status_code == 200
    assert "Ліки успішно оновлено" in put_resp.get_json()["message"]

    # Перевірка
    get_resp = client.get(f'/medicines/{med_id}')
    assert get_resp.get_json()['quantity'] == 7

# ❌ 4. Видалення (DELETE /medicines/<id>)
def test_delete_medicine(client):
    # Створення
    post_resp = client.post('/medicines', json={
        "name": "Но-шпа",
        "expiration_date": "2026-01-01",
        "quantity": 4,
        "description": ""
    })
    med_id = post_resp.get_json()['id']

    # Видалення
    del_resp = client.delete(f'/medicines/{med_id}')
    assert del_resp.status_code == 200
    assert "Ліки видалено успішно" in del_resp.get_json()["message"]

    # Перевірка, що ліки більше не існують
    get_resp = client.get(f'/medicines/{med_id}')
    assert get_resp.status_code == 404

# ❌ 5. Порожнє ім’я (POST)
def test_post_empty_name(client):
    response = client.post('/medicines', json={
        "name": "",
        "expiration_date": "2025-12-31",
        "quantity": 5,
        "description": "Без назви"
    })
    assert response.status_code == 400
    assert "Ім’я препарату має бути текстом" in response.get_json()["errors"]

# ❌ 6. Назва — число
def test_post_numeric_name(client):
    response = client.post('/medicines', json={
        "name": "1234",
        "expiration_date": "2025-12-31",
        "quantity": 5,
        "description": "Цифрова назва"
    })
    assert response.status_code == 400
    assert "Назва не може бути числом" in response.get_json()["errors"]

# ❌ 7. Неправильний формат дати
def test_post_invalid_date(client):
    response = client.post('/medicines', json={
        "name": "Валідол",
        "expiration_date": "31-12-2025",
        "quantity": 5,
        "description": "Невірна дата"
    })
    assert response.status_code == 400
    assert "Невірний формат дати (очікується YYYY-MM-DD)" in response.get_json()["errors"]

# ❌ 8. GET неіснуючого ID
def test_get_nonexistent(client):
    response = client.get('/medicines/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert "Ліки не знайдено" in data.get("error", "")

# ❌ 9. Відсутній name:
def test_post_missing_name(client):
    response = client.post('/medicines', json={
        "expiration_date": "2025-12-31",
        "quantity": 5,
        "description": "Без імені"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Поле 'name' обов’язкове" in data.get("errors", [])

# ❌ 10. Відсутній expiration_date:
def test_post_missing_expiration_date(client):
    response = client.post('/medicines', json={
        "name": "Амізон",
        "quantity": 5,
        "description": "Без дати"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Поле 'expiration_date' обов’язкове" in data.get("errors", [])

# ❌ 11. Відсутній quantity:
def test_post_missing_quantity(client):
    response = client.post('/medicines', json={
        "name": "Антигрипін",
        "expiration_date": "2025-12-31",
        "description": "Без кількості"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Поле 'quantity' обов’язкове" in data.get("errors", [])

# ❌ 12. quantity — не число:
def test_post_quantity_not_number(client):
    response = client.post('/medicines', json={
        "name": "Цитрамон",
        "expiration_date": "2025-12-31",
        "quantity": "багато",
        "description": "Некоректна кількість"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Кількість має бути числом" in data.get("errors", [])

# ❌ 13. quantity — 0:
def test_post_quantity_zero(client):
    response = client.post('/medicines', json={
        "name": "Цитрамон",
        "expiration_date": "2025-12-31",
        "quantity": 0,
        "description": "Нульова кількість"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Кількість не може бути нульовою" in data.get("errors", [])

# ❌ 14. quantity — від’ємне значення:
def test_post_quantity_negative(client):
    response = client.post('/medicines', json={
        "name": "Цитрамон",
        "expiration_date": "2025-12-31",
        "quantity": -5,
        "description": "Від’ємна кількість"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Кількість не може бути від’ємною" in data.get("errors", [])

# ✏️ 15. Порожній опис (має бути дозволено):
def test_post_empty_description(client):
    response = client.post('/medicines', json={
        "name": "Тест без опису",
        "expiration_date": "2025-12-31",
        "quantity": 1,
        "description": ""
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data

# ✏️ 16. Велика кількість:
def test_post_large_quantity(client):
    response = client.post('/medicines', json={
        "name": "Тест велика кількість",
        "expiration_date": "2025-12-31",
        "quantity": 999999,
        "description": "Має працювати"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data

# ✏️ 17. Дублі (ті ж назва/дата):
def test_post_duplicate(client):
    payload = {
        "name": "Дубль",
        "expiration_date": "2025-12-31",
        "quantity": 3,
        "description": "Перше додавання"
    }

    first = client.post('/medicines', json=payload)
    second = client.post('/medicines', json=payload)

    assert first.status_code == 201
    assert second.status_code == 201  # наразі дублі дозволені
