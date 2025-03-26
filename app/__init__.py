from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Підключення до MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:h5s%4L%PeYXC@localhost/pharmacy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models  # Імпортуємо маршрути та моделі