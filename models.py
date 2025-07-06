from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# A simple User class for Flask-Login without a database table
class User(UserMixin):
    def __init__(self, id):
        self.id = id

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(256), nullable=True) # New column for the image URL