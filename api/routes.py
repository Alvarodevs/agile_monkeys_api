from os import name
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from api.models import db, Admin, User, Customer
from datetime import datetime
import cloudinary
import cloudinary.uploader
import json
api = Blueprint('api', __name__)

# #ROUTES ADMIN
# @api.route("/")
# def index():
#     return data

#Importing seed customer data
# with open('api\data\seed_new_customer.json') as f:
#     data = json.load(f)

#####       ADMIN SECTION           ######
def current_admin(identity):                        
    return Admin.query.get(identity['id'])              #-----> SE PIDE ID, PERO DEVUELVE USER-NAME

@api.route("/admin_sign_up", methods=["POST"])   #-----> ¿AUTHENTICATION OAUTH?
def admin_sign_up():    
    body = request.get_json(force=True)
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    new_admin = Admin(user_name, password)
    db.session.add(new_admin)
    db.session.commit()
    access_token = create_access_token(identity=new_admin.serialize())
    return jsonify(user=new_admin.serialize(), accessToken=access_token)

@api.route("/admin", methods=["GET"]) ### DONE LIST ADMIN
def get_admins():
    admin = Admin.query.all()
    admins = list(map(lambda admin: admin.serialize(), admin))
    return jsonify(admins), 200

#####       USERS SECTION           ######

@api.route("/users", methods=["GET"]) ### DONE LIST USERS
@jwt_required()
def handle_users():
    admin = current_admin(get_jwt_identity())
    user = User.query.all()
    users = list(map(lambda user: user.serialize(), user))
    return jsonify(users), 200

@api.route("/users_sign_up", methods=["POST"]) ### DONE CREATE USERS  --> ANTES ERA IF..ELSE FILTRANDO SI 
@jwt_required()                                                         # USER_NAME CONTIENE "ADMIN"    
def create_user():
    admin = current_admin(get_jwt_identity())
    body = request.get_json(force=True)
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    is_active = body.get("is_active", None)

    new_user = User(user_name, password, is_active, admin)
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity=new_user.serialize())
    return jsonify(user=new_user.serialize(), accessToken=access_token)
    
    
@api.route("/user/<int:id>", methods=["GET", "DELETE"]) ### DONE DELETE USERS
@jwt_required()
def handle_one_user(id):
    admin = current_admin(get_jwt_identity())
    if request.method == "GET":
        user = User.query.get(id)
        return jsonify(user.serialize()), 200
    else:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.serialize()), 200               #--->ERROR: BASE QUERY NO PERMITE SERIALIZE

@api.route("/user/<int:id>", methods=["PUT"]) #UPDATE USERS OK
@jwt_required()
def update_user(id):
    admin = current_admin(get_jwt_identity())
    updated_user = User.query.get_or_404(id) 
    body_json = request.get_json()
    user_name = body_json.get("user_name", None)
    password = body_json.get("password", None)
    is_active = body_json.get("is_active", None)

    updated_user.user_name = user_name
    updated_user.password = password
    updated_user.is_active = is_active

    db.session.commit()
    return jsonify(updated_user.serialize()), 200

@api.route("/login", methods=["POST"]) ### DONE LOGIN USERS & ADMIN
def sign_in():
    status = "NOP"
    body = request.get_json()
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    
    if "admin" not in user_name:    # WOULD CHANGE THIS LINE FOR ADMIN TO TYPE ANY NAME NOT CONTAINING "ADMIN"
        user = User.query.filter_by(user_name=user_name).one_or_none()
        if not user or not user.check_password(password):
            return jsonify({"status": status, "msg": "Are you sure folk? Please, try again."}), 401
        status = "OK"
        access_token = create_access_token(identity=user.serialize())
        return jsonify(status = status, user=user.serialize(), accessToken=access_token)

    if "admin" in user_name: 
        ### IN CASE MORE ADMINS ADDED: --> admin = Admin.query.filter_by(user_name=user_name).one_or_none() <--
        admin = Admin.query.filter_by(user_name=user_name).one_or_none()
        if not admin or not admin.check_password(password):
            return jsonify({"status": status, "msg": "Are you the real admin? Please, try again."}), 401
        status = "OK"   
        access_token = create_access_token(identity=admin.serialize())
        return jsonify(status = status, admin=admin.serialize(), accessToken=access_token)    

######       CUSTOMERS SECTION           ######

def current_user(identity):
  return User.query.get(identity["id"])

    ###GETTING LIST OF CUSTOMERS FROM USER###
@api.route("/customers", methods=["GET"])
@jwt_required()
def list_all_customers():
    user = current_user(get_jwt_identity())
    print(user)
    customer = Customer.query.all()
    customers = list(map(lambda customer: customer.serialize(), customer))
    return jsonify(customers), 200
    
#     ###GETTING SINGLE CUSTOMER INFO FROM USER###
@api.route("/customer/<int:id>", methods=["GET"])
@jwt_required()
def handle_customer(id):
    user = current_user(get_jwt_identity())
    customer = Customer.query.get(id)
    return (customer.serialize()), 200

#    ###CREATING NEW CUSTOMER && UPDATING CUSTOMER FROM USER###
@api.route("/customer", methods=["POST", "PUT"])
@jwt_required()
def create_customer():
    user = current_user(get_jwt_identity())
    if request.method == "POST":
        body_json = request.get_json()
        name = body_json.get('name', None)
        surname = body_json.get('surname', None)
        
        #Received binary file in body_json & storing in cloudinary --> Cloudinary store OK
        avatar_cloudinary = cloudinary.uploader.upload(body_json.get("avatar_url"), public_id = "agile_monkeys/avatar_image")
        avatar_url = avatar_cloudinary["secure_url"]
        customer = Customer(name, surname, avatar_url, user)
        print("AVATAR", avatar_url)
        db.session.add(customer)
        db.session.commit()
        return (customer.serialize()), 200

    ###UPDATING NEW CUSTOMER FROM USER###
# def update_customer():
#     user = current_user(get_jwt_identity())
#     if request.method == "PUT":
#         body_json = request.get_json()
#         name = body_json.get("name", None)
#         surname = body_json.get("surname", None)
#         avatar_url = cloudinary.uploader.uploa(body_json.get("avatar_url", None))

#         if user.avatar_url is not None:
#             cloudinary.uploader.destroy(Customer.avatar_public())
#     


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


