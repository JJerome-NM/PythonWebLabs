from flask_login import UserMixin

from app import db, bcrypt, login_manager


class AuthUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    avatar_image = db.Column(db.String(30), nullable=True, default="default.png")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password=password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    @login_manager.user_loader
    def user_loader(user_id: int)   :
        return AuthUser.query.get(user_id)