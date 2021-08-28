from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='user', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    customers = db.relationship('Customer', backref='user', lazy=True)
    admin_id = db.relationship(db.Integer, db.ForeignKey('admin.id'))

    def __init__(self, name, password, is_active):
       self.user_name = name
       self.password = password
       self.is_active = is_active
       
    def __repr__(self):
        return '<User %r>' % self.user_name 

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "is_active": self.is_active
        }

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(40), unique=False, nullable=False)
    avatar_url = db.Column(db.String(200), unique=False, nullable=True)
    created_at = db.Column(DateTime(), default=datetime.now())
    modified_at = db.Column(DateTime(), default=datetime.now())
    user_id = db.relationship(db.Integer, db.ForeignKey('user.id'))
    user_name = db. relationship(db.String, db.ForeignKey('user.name')) 
    
    def __init__(self, name, surname, avatar_url, user_id, created_at, modified_at):
       self.name = name
       self.surname = surname
       self.avatar_url = avatar_url
       self.user_id = user_id
       self.created_at = created_at
       self.modified_at = modified_at

    def __repr__(self):
        return '<Customer %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "avatar_url": self.avatar_url,
            "created": self.created_at,
            "last_modified": self.modified_at,
            "modified_by": [self.user_id, self.user_name]
        }


