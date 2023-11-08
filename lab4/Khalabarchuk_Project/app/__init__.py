from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def enumerate_filter(iterable):
    return enumerate(iterable)


app = Flask(__name__)
app.secret_key = b"secret"

app.jinja_env.filters['enumerate'] = enumerate_filter
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app import views
