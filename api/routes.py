from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api.models import db, Admin, User, Customer
import json
api = Blueprint('api', __name__)

#Importing seed customer data
with open('api\data\seed_new_customer.json') as f:
    data = json.load(f)

#ROUTES ADMIN
@api.route("/")
def index():
    return data

#ADMIN HANDLING USERS
@api.route("/admin", methods=["GET"])
def handle_users():
    user = User.query.all()
    users = list(map(lambda user: user.serialize()))
    return jsonify(users), 200

@api.route("/admin", methods=["POST"])
def create_user():
    body = request.get_json()
    user_name = body.get("user_name", None)
    password = body.get("password", None)

    new_user = User(user_name=user_name)  
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity=new_user.serialize())

    return jsonify(user=new_user.serialize(), accesToken=access_token)

#USER HANDLING CUSTOMERS
@api.route("/user", methods=["GET"])
def list_of_all_customers():
    customer = Customer.query.all()
    customers = list(map(lambda customer: customer.serialize()))
    return {customers}, 200

# def single_customer_info():
#         pass

# def create_customer():
#         pass    

# def update_customer():
#         pass

# def delete_customer():
#         pass


