from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, index=True, default=datetime.now)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    city = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return self.name


class Locality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return self.name


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zomato_url = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String)
    area = db.Column(db.String)
    rating = db.Column(db.Float)
    rating_count = db.Column(db.Float)
    telephone = db.Column(db.String)
    cuisine = db.Column(db.String)
    cost_for_two = db.Column(db.Float)
    address = db.Column(db.String)
    online_order = db.Column(db.Boolean)
    table_reservation = db.Column(db.Boolean)
    delivery_only = db.Column(db.Boolean)
    famous_food = db.Column(db.String)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):
        return self.name


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rest_id = db.Column(db.Integer, db.ForeignKey(Restaurant.id))
    rating = db.Column(db.Integer)
    username = db.Column(db.String(64), db.ForeignKey(User.username))
    date_posted = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return self.rating
