from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import os
from flask_mail import Mail
from app.config import Config 

pymysql.install_as_MySQLdb()

# Завантажуємо змінні середовища з .env


# Ініціалізація Flask додатку
app = Flask(__name__, template_folder='../templates')

# Налаштування конфігурації через клас Config
app.config.from_object(Config)

# Ініціалізація Mail
mail = Mail(app)

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

# Ініціалізація міграцій
migrate = Migrate(app, db)

def create_app():
    return app

def register_routes():
    from app import routes

register_routes()

print(os.getenv('SQLALCHEMY_DATABASE_URI'))