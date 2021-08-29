from os import name
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from api.models import db, Admin, Users, Customer
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
with open('api\data\seed_new_customer.json') as f:
    data = json.load(f)

#####       ADMIN SECTION           ######
def current_admin(identity):
    admin = Admin.query.get(identity["id"])

#####       USERS SECTION           ######
@api.route("/users", methods=["GET"]) ### DONE
@jwt_required()
def handle_users():
    admin = current_admin(get_jwt_identity())
    user = Users.query.all()
    users = list(map(lambda user: user.serialize(), user))
    return jsonify(users), 200

@api.route("/users_sign_up", methods=["POST"]) ### DONE
@jwt_required()
def create_user():
    admin = current_admin(get_jwt_identity())
    body = request.get_json(force=True)
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    is_active = True

    if not user_name == "admin":
        new_user = Users(user_name, password, is_active) 
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.serialize())
        return jsonify(user=new_user.serialize(), accessToken=access_token)
    else:
        new_admin = Admin(user_name, password)
        db.session.add(new_admin)
        db.session.commit()
        access_token = create_access_token(identity=new_admin.serialize())
        return jsonify(user=new_admin.serialize(), accessToken=access_token)
    

@api.route("/login", methods=["POST"]) ### DONE
def sign_in():
    status = "NOP"
    body = request.get_json()
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    
    if not "admin" in user_name:
        user = Users.query.filter_by(user_name=user_name).one_or_none()
        if not user or not user.check_password(password):
            return jsonify({"status": status, "msg": "Are you sure folk? Please, try again."}), 401
        status = "OK"
        access_token = create_access_token(identity=user.serialize())
        return jsonify(status = status, user=user.serialize(), accessToken=access_token)

    else: 
        ### IN CASE MORE ADMINS ADDED: --> admin = Admin.query.filter_by(user_name=user_name).one_or_none() <--
        admin = Admin.query.filter_by(id='1').first()
        if not admin.check_password(password):
            return jsonify({"status": "NOP", "msg": "Are you the real admin? Please, try again."}), 401
        status = "OK"   
        access_token = create_access_token(identity=admin.serialize())
        return jsonify(status = status, admin=admin.serialize(), accessToken=access_token)    

######       CUSTOMERS SECTION           ######

def current_user(identity):
  return Users.query.get(identity["id"])

    ###GETTING LIST OF CUSTOMERS FROM USER###
@api.route("/customers", methods=["GET"])
@jwt_required()
def list_of_all_customers():
    user = current_user(get_jwt_identity())
    customer = Customer.query.all()
    customers = list(map(lambda customer: customer.serialize()))
    return {customers}, 200
    

#     ###GETTING SINGLE CUSTOMER INFO FROM USER###
@api.route("/customer/<int:id>", methods=["GET"])
@jwt_required()
def handle_customer(id):
    user = current_user(get_jwt_identity())
    customer = Customer.query.get(id)
    return { customer.serialize() }, 200

#    ###CREATING NEW CUSTOMER && UPDATING CUSTOMER FROM USER###
@api.route("/customer", methods=["POST", "PUT"])
@jwt_required()
def create_customer():
    user = current_user(get_jwt_identity())
    if request.method == "POST":
        body_json = request.get_json()
        created_at = datetime.now()
        #Received binary file in body_json & storing in cloudinary --> Cloudinary OK
        avatar_cloudinary = cloudinary.uploader.upload(body_json["avatar_url"], public_id = "agile_monkeys/avatar_image")

        customer = Customer(name=body_json["name"], surname=body_json["surname"], avatar_url=avatar_cloudinary["secure_url"], user_id_creator=user, created_at=created_at)


        print("AVATAR", avatar_cloudinary['secure_url'])
        db.session.add(customer)
        db.session.commit()
    

    return { customer.serialize()}, 200

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


