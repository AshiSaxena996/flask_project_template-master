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
    name= db.Column(db.String(120)) 
    age= db.Column(db.Integer)
    phone= db.Column(db.Integer)
    city= db.Column(db.String(64))
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
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String())
    
    def __repr__(self):
        return self.name
    
class Likes_Cuisine(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey(User.id))
    cuisine_id= db.Column(db.Integer, db.ForeignKey(Cuisine.id))

    def __repr__(self):
        return self.id



class Locality(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(64), nullable=False)
    city= db.Column(db.String(64), nullable=False)
    

    def __repr__(self):
        return self.name

class Restaurant(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    address= address= db.Column(db.String, nullable=False)
    locality_id= db.Column(db.Integer, db.ForeignKey(Locality.id))
    phone= db.Column(db.String, nullable=True)
    delivery= db.Column(db.Boolean, nullable= True)
    booking= db.Column(db.Boolean, nullable=True)
    url= db.Column(db.String, nullable=False)
    

    def __repr__(self):
        return self.name

class Rating(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    rest_id= db.Column(db.Integer, db.ForeignKey(Restaurant.id))
    cuisine_id= db.Column(db.Integer, db.ForeignKey(Cuisine.id))
    rating= db.Column(db.Integer)
    username= db.Column(db.String(64), db.ForeignKey(User.username))
    date_posted=  db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return self.rating

class Has_Cuisine(db.Model):
    id=  db.Column(db.Integer, primary_key=True)
    rest_id= db.Column(db.Integer, db.ForeignKey(Restaurant.id))
    cuisine_id= db.Column(db.Integer, db.ForeignKey(Cuisine.id))

    def __repr__(self):
        return self.rating
    

class Has_Rating(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    rest_id= db.Column(db.Integer, db.ForeignKey(Restaurant.id))
    cuisine_id= db.Column(db.Integer, db.ForeignKey(Cuisine.id))
    rating= db.Column(db.Integer)
    rating_count= db.Column(db.Integer)

    def __repr__(self):
        return f"{self.rating} & {self.rating_count}"








