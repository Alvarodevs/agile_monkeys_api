from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    #users = db.relationship('User', backref='user', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    # customers = db.relationship('Customer', backref='user', lazy=True)
    # admin = db.relationship(db.Integer, db.ForeignKey('admin.id'), nullable=False)


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(40), unique=False, nullable=False)
    avatar_url = db.Column(db.String(200), unique=False, nullable=True)
    created_at = db.Column(db.String(15), unique=False, nullable=False)
    modified_at = db.Column(db.String(15), unique=False, nullable=False)
    #user_id = db.relationship(db.Integer, db.ForeignKey('user.id'), nullable=False) nullable not recognize

    def __init__(self, name, surname, avatar_url, user_id, created_at, modified_at):
       self.name = name
       self.surname = surname
       self.avatar_url = avatar_url
       self.user_id = user_id
       self.created_at = created_at
       self.modified_at = modified_at

    def __repr__(self):
        return '<Customer %r>' % self.name 

