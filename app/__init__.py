from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql

pymysql.install_as_MySQLdb()


app = Flask(__name__, template_folder='../templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:h5s%4L%PeYXC@localhost/pharmacy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'super-secret-kit' 

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def register_routes():
    from app import routes

register_routes()