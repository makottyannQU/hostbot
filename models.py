from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as SA


class SQLAlchemy(SA):
    def apply_pool_defaults(self, app, options):
        SA.apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True


db = SQLAlchemy()


def now():
    return datetime.now().timestamp()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(37), nullable=False, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    status=db.Column(db.Integer, nullable=False, default=1)

class Profile(db.Model):
    __tablename__ = 'profile'
    user_id = db.Column(db.String(37), nullable=False, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    couse = db.Column(db.Text, nullable=False)
    club = db.Column(db.Text, nullable=False)

class Order(db.Model):
    __tablename__ = 'order'
    user_id = db.Column(db.String(37), nullable=False, primary_key=True)
    date = db.Column(db.Integer, nullable=False, primary_key=True)
    meal_id=db.Column(db.String(37), nullable=False,primary_key=True)
    status=db.Column(db.Integer, nullable=False, default=1)
    size=db.Column(db.Integer, nullable=False, default=1)
    number=db.Column(db.Integer, nullable=False, default=1)
    timestamp=db.Column(db.Integer, nullable=False, default=now())


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.String(37), nullable=False, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    s_price=db.Column(db.Integer, nullable=True)
    m_price=db.Column(db.Integer, nullable=True)
    l_price=db.Column(db.Integer, nullable=True)


class Menu(db.Model):
    __tablename__ = 'menu'
    date = db.Column(db.Integer, nullable=False, primary_key=True)
    meal_id = db.Column(db.String(37), nullable=False, primary_key=True)
    s_stock=db.Column(db.Integer, nullable=True)
    m_stock=db.Column(db.Integer, nullable=True)
    l_stock=db.Column(db.Integer, nullable=True)
    timestamp=db.Column(db.Integer, nullable=False, default=now())