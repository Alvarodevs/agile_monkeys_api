from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import Integer
from werkzeug.security import safe_str_cmp


db = SQLAlchemy()

class Admin(db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='admin', lazy=True, primaryjoin="Admin.id == User.admin_id")

    def __init__(self, name, password):
       self.user_name = name
       self.password = password

    def __repr__(self):
        return '<Admin %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "users_created": self.users
        }

    def check_admin_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))


modifications = db.Table('modifications',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True),
    db.Column('modified_at', db.DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
)

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    customers = db.relationship('Customer', secondary='modifications', backref=db.backref('user'), lazy=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, name, password, is_active, admin):
       self.user_name = name
       self.password = password
       self.is_active = is_active
       self.admin_id = admin.id
       
    def __repr__(self):
        return '<User %r>' % self.user_name 

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "is_active": self.is_active
        }

    def check_user_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))

class Customer(db.Model):

    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(40), unique=False, nullable=False)
    avatar_url = db.Column(db.String(300), unique=False, nullable=True)
    users = db.relationship('User', secondary='modifications', backref=db.backref('customer'), lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    def __init__(self, name, surname, avatar_url, user_id):
       
       self.name = name
       self.surname = surname
       self.avatar_url = avatar_url
       self.user_id_creator = user_id.id


    def __repr__(self):
        return '<Customer %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "avatar_url": self.avatar_url,
            "created": self.created_at,
            "created_by": self.users,
        }
    
    #Storing file name of avatar

    def avatar_public(self):
        if self.avatar_url is None:
            return None
        file_name = self.avatar_url.split("/")
        [public_id, extension] = file_name[-1].split(".")
        return public_id

    def get_customer_list(self):
        return {
            "id": self.id,
            "name": self.name,

        }

# class Modifications(db.Model):    
#     __tablename__ = 'modifications'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) #<----------
#     modification_date = db.Column(db.DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
#     user = db.relationship(User, backref=backref('modifications', cascade='all, delete_orphan'))
#     customer = db.relationship(Customer, backref=backref('modifications', cascade='all, delete_orphan'))
