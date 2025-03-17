# 🏥 Домашня Аптечка (First-aid kit)

Цей проєкт допомагає керувати домашньою аптечкою, відстежувати терміни придатності ліків та кількість важливих препаратів.

## ✨ Функціонал
- 🗃️ Ведення списку ліків (назва, опис, термін придатності, кількість).
- 🔔 Сповіщення про закінчення терміну придатності.
- 🔄 CRUD-операції (додавання, оновлення, видалення ліків).
- 📊 API для взаємодії з базою даних.

---

## 👉 Як встановити та запустити проєкт?

### 1. Встановлення Python та MySQL
Перед початком переконайся, що у тебе встановлено:
- ✅ [Python 3.10+](https://www.python.org/downloads/)
- ✅ [MySQL Server 8.0+](https://dev.mysql.com/downloads/installer/)

**Перевір версії:**
```bash
python --version
mysql --version
```

---

### 2. Клонування репозиторію
```bash
git clone https://github.com/твій-нікнейм/first-aid-kit.git
cd first-aid-kit
```

---

### 3. Налаштування віртуального середовища
```bash
python -m venv venv
source venv/Scripts/activate  # Git Bash
venv\Scripts\activate  # Windows CMD
```

**Встановлення залежностей:**
```bash
pip install -r requirements.txt
```

---

### 4. Налаштування MySQL
1. **Запусти MySQL у терміналі**:
   ```bash
   mysql -u root -p
   ```
2. **Створи базу даних**:
   ```sql
   CREATE DATABASE pharmacy_db;
   ```

---

### 5. Виконання міграцій
```bash
flask db upgrade
```

---

### 6. Запуск проєкту
```bash
python run.py
```
Відкрий у браузері:
```
http://127.0.0.1:5000/
```

---

## 📚 Технічні деталі
- **Мова**: Python 3.10+
- **Фреймворк**: Flask
- **База даних**: MySQL
- **ORM**: SQLAlchemy + Flask-Migrate
- **Стек**: Flask, SQLAlchemy, Bootstrap (пізніше)

---

## 🏆 Автори
- **Anna Khishchenko** - головний розробник 💻
- **ChatGPT** - помічник у розробці та підтримці 🛠️
