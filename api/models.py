from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
from werkzeug.security import safe_str_cmp


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

    def check_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))

class Customer(db.Model):

    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(40), unique=False, nullable=False)
    avatar_url = db.Column(db.String(200), unique=False, nullable=True)
    created_at = db.Column(DateTime(), default=datetime.now())
    modified_at = db.Column(DateTime(), default=datetime.now()) #Date must be set from POST method
    modified_by = db.Column(db.Integer)
    user_id = db.relationship(db.Integer, db.ForeignKey('user.id'))

    
    def __init__(self, name, surname, avatar_url, user, created_at, modified_at):
       self.name = name
       self.surname = surname
       self.avatar_url = avatar_url
       self.user = user
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
            "avatar_public_id": self.avatar_public(),
            "created": self.created_at,
            "created_by": self.user,
            "last_modified": self.modified_at,
            "modified_by": self.modified_by
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


