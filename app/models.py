from flask_login import UserMixin
from passlib.hash import bcrypt_sha256

from . import db, login


@login.user_loader
def load_user(uid):
    return User.query.get(uid)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(), index=True, unique=True)
    password_hash = db.Column(db.String())

    score = db.Column(db.Integer())
    code = db.Column(db.String())
    default_data = db.Column(db.String())
    last_exception = db.Column(db.String())

    is_admin = db.Column(db.Boolean())

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = bcrypt_sha256.hash(password)

    def check_password(self, password):
        return bcrypt_sha256.verify(password, self.password_hash)
