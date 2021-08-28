from os import name
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api.models import db, Admin, User, Customer
#from cloudinary import 
import json
api = Blueprint('api', __name__)

# #ROUTES ADMIN
# @api.route("/")
# def index():
#     return data

#Importing seed customer data
with open('api\data\seed_new_customer.json') as f:
    data = json.load(f)

#####       ADMIN SECTION           ######


 
#####       USERS SECTION           ######
@api.route("/users", methods=["GET"])
def handle_users():
    user = User.query.all()
    users = list(map(lambda user: user.serialize()))
    return jsonify(users), 200

@api.route("/sign_up", methods=["POST"])
def create_user():
    body = request.get_json()
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    is_active = True

    new_user = User(user_name=user_name, password=password, is_active=is_active)  
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity=new_user.serialize())

    return jsonify(user=new_user.serialize(), accesToken=access_token)

# @api.route("/login")
# def sign_in():
#     status = "NOP"
#     body = request.get_json()
#     user_name = body.get("user_name", None)
#     password = body.get("password", None)
    
#     if user_name is not "admin":
#         user = User.query.filter_by(user_name=user_name).one_or_none()
#         if not user or not user.check_password(password):
#             return jsonify({"status": status, "msg": "Are you sure folk? Please, try again."}), 401
#         status = "OK"
#         access_token = create_access_token(identity=user.serialize())
#         return jsonify(status = status, user=user.serialize(), accessToken=access_token)

#     else: 
#         admin = Admin.query.filter_by(user_name=user_name).one_or_none()
#         if not admin.check_password(password):
#             return jsonify({"status": "NOP", "msg": "Are you the real admin? Please, try again."}), 401
#         status = "OK"   
#         access_token = create_access_token(identity=admin.serialize())
#         return jsonify(status = status, admin=admin.serialize(), accessToken=access_token)    

# #####       CUSTOMERS SECTION           ######

# def current_user(identity):
#   return User.query.get(identity["id"])

#     ###GETTING LIST OF CUSTOMERS FROM USER###
# @api.route("/customers", methods=["GET"])
# def list_of_all_customers():
#     customer = Customer.query.all()
#     customers = list(map(lambda customer: customer.serialize()))
#     return {customers}, 200

#     ###GETTING SINGLE CUSTOMER INFO FROM USER###
# @api.route("/customer/<int:id>", methods=["GET"])
# @jwt_required()

# def handle_customer(id):
#     user = current_user(get_jwt_identity())
#     customer = Customer.query.get(id)
#     return { customer.serialize() }, 200

#    ###CREATING NEW CUSTOMER && UPDATING CUSTOMER FROM USER###
# @api.route("/new_customer", methods=["POST", "PUT"])
# @jwt_required()
# def create_customer():
#     user = current_user(get_jwt_identity())
#     body_json = request.get_json()
#     new_customer = Customer(name=body_json["name"], surname=body_json["surname"], avatar_url=body_json["avatar_url"])

#     db.session.add(new_customer)
#     db.session.commit()
#     print(new_customer)

#     return { new_customer.serialize()}, 200

# def update_customer():
#     user = current_user(get_jwt_identity())
#     if request.method == "PUT":
#         body_json = request.get_json()
#         name = body_json.get("name", None)
#         surname = body_json.get("surname", None)
#         avatar_url = cloudinary.uploader.uploa(body_json.get("avatar_url", None))

#         if user.avatar_url is not None:
#             cloudinary.uploader.destroy(Customer.avatar_public())
#     ###UPDATING NEW CUSTOMER FROM USER###
# #@api.route("/")
# # def update_customer():
# #         pass

#     ###DELETING CUSTOMER FROM USER###
# @api.route("/customer/<int:id>", methods=["DELETE"])
# @jwt_required()
# def delete_customer(id):
#     user = current_user(get_jwt_identity())
#     customer = Customer.query.get(id)

#     db.session.delete(customer)
#     db.session.commit()

#     return { customer.serialize() }, 200


