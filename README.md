🏥 Домашня Аптечка (Home Pharmacy)

Цей проєкт допомагає керувати домашньою аптечкою, відстежувати терміни придатності ліків та кількість важливих препаратів.

✨ Функціонал

🗃️ Ведення списку ліків (назва, опис, термін придатності, кількість).

🔔 Сповіщення про закінчення терміну придатності.

🔄 CRUD-операції (додавання, оновлення, видалення ліків).

📊 API для взаємодії з базою даних.

👉 Як встановити та запустити проєкт?

1. Встановлення Python та MySQL

Перед початком переконайся, що у тебе встановлено:

✅ Python 3.10+

✅ MySQL Server 8.0+

Перевір версії:

python --version
mysql --version

2. Клонування репозиторію

git clone https://github.com/твій-нікнейм/first-aid-kit.git
cd first-aid-kit

3. Налаштування віртуального середовища

python -m venv venv
source venv/Scripts/activate  # Git Bash
venv\Scripts\activate  # Windows CMD

Встановлення залежностей:

pip install -r requirements.txt

4. Налаштування MySQL

Запусти MySQL у терміналі:

mysql -u root -p

Створи базу даних:

CREATE DATABASE pharmacy_db;

5. Виконання міграцій

flask db upgrade

6. Запуск проєкту

python run.py

Відкрий у браузері:

http://127.0.0.1:5000/

📚 Технічні деталі

Мова: Python 3.10+

Фреймворк: Flask

База даних: MySQL

ORM: SQLAlchemy + Flask-Migrate

Стек: Flask, SQLAlchemy, Bootstrap (пізніше)

🏆 Автори

Anna Khishchenko - головний розробник 💻
chat GPT — головний консультант та помічник 🧠