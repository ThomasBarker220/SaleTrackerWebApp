from flask import app
from saleWA import db, login_manager
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin
import jwt

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin): #create classes for database, each class is like a table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #have to have at least default image
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #relationship to Post model, pass in as string, backref allows us to use the author attribute to get user who made the post, lazy=True means SQLAlchemy loads data as necessary in one go

    def get_reset_token(self, expired_sec=1800):
        s = jwt.encode({'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=expired_sec), 'user_id':self.id},
                       app.config['SECRET_KEY'], algorithm='HS256')
        return s
    
    @staticmethod #don't expect self parameter as an arugment
    def verify_reset_token(token):
        try:
            s = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = s['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self): #returns printable representation of the object as a string
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

class Post(db.Model): # this is just from video walkthrough, will probably need to change/check and make sure this is how it should run
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #using lowercase user here because we're referencing table name

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# class Item(db.Model): # this is just from video walkthrough, will probably need to change/check and make sure this is how it should run
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False)
#     price = db.Column(db.Integer, nullable=False)