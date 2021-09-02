from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import Integer
from werkzeug.security import safe_str_cmp

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    is_admin = db.Column (db.Boolean, unique=False, nullable=False)
    
    def __init__(self, name, password, is_active, is_admin):
       self.user_name = name
       self.password = password
       self.is_active = is_active
       self.is_admin = is_admin
       
    def __repr__(self):
        return '<User %r>' % self.user_name 

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "is_active": self.is_active, 
            "is_admin": self.is_admin
        }

    def check_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))

class Customer(db.Model):

    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(40), unique=False, nullable=False)
    avatar_url = db.Column(db.String(300), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    def __init__(self, name, surname, avatar_url, user_id):
       
       self.name = name
       self.surname = surname
       self.avatar_url = avatar_url
       self.user_id = user_id.id

    def __repr__(self):
        return '<Customer %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "avatar_url": self.avatar_url,
            "created_by": self.user_id,
            "created": self.created_at,
        }
    
    #Method file name of avatar

    def avatar_public(self):
        if self.avatar_url is None:
            return None
        file_name = self.avatar_url.split("/")
        [public_id, extension] = file_name[-1].split(".")
        return public_id

class Modifications(db.Model):    
    __tablename__ = 'modifications'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    modification_date = db.Column(db.DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    def __init__(self, customer_id, user_id):
       
       self.customer_id = customer_id
       self.modified_by = user_id
       
    def __repr__(self):
        return '<Modifications %r>' % self.modification_date 

    def serialize(self):
        return {
            "id": self.id,
            "customer": self.customer_id,
            "user": self.modified_by,
            "date_of_modification": self.modification_date
        }