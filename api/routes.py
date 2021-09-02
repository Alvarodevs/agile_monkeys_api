from os import name
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from api.models import  db, Modifications, User, Customer
import cloudinary
import cloudinary.uploader

api = Blueprint('api', __name__)


#####       ADMIN SECTION           ######
# def current_admin(identity):                        
#     return Admin.query.get(identity['id'])

# @api.route("/admin_sign_up", methods=["POST"])   #-----> future OAUTH AUTHENTICATION
# def admin_sign_up():    
#     body = request.get_json(force=True)
#     user_name = body.get("user_name", None)
#     password = body.get("password", None)
#     new_admin = Admin(user_name, password)
#     db.session.add(new_admin)
#     db.session.commit()
#     access_token = create_access_token(identity=new_admin.serialize())
#     return jsonify(user=new_admin.serialize(), accessToken=access_token)

# @api.route("/admin", methods=["GET"]) ### DONE LIST ADMIN
# def get_admins():
#     admin = Admin.query.all()
#     admins = list(map(lambda admin: admin.serialize(), admin))
#     return jsonify(admins), 200

#####       USERS SECTION           ######

@api.route("/users_sign_up", methods=["POST"]) #---OK                                                             
def create_user():
    body = request.get_json(force=True)
    user_name = body.get("user_name", None)
    password = body.get("password")
    is_active = body.get("is_active", None)
    is_admin = body.get("is_admin")

    if len(password) < 8:
        return "Password is too short, try again."

    elif len(user_name) < 4:
        return "User name is too short, try again."

    else:
        new_user = User(user_name, password, is_active, is_admin)
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.serialize())
        return jsonify(user=new_user.serialize(), accessToken=access_token)


@api.route("/users", methods=["GET"]) #---OK
@jwt_required()
def handle_users():
    user = current_user(get_jwt_identity())
    if user.is_admin == True:
        user = User.query.all()
        users = list(map(lambda user: user.serialize(), user))
        return jsonify(users), 200
    else: 
        return jsonify("You are not allowed my friend.")


@api.route("/user/<int:id>", methods=["GET", "DELETE"]) #---OK
@jwt_required()
def handle_one_user(id):
    admin = current_user(get_jwt_identity())
    if admin.is_admin == True:
        if request.method == "GET":
            user = User.query.get_or_404(id)
            return jsonify(user.serialize()), 200
        else:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify(user.serialize()), 200
    else:
        return jsonify("Sorry folk, this is just for admins.")

@api.route("/user/<int:id>", methods=["PUT"]) #---OK
@jwt_required()
def update_user(id):
    user = current_user(get_jwt_identity())
    if user.is_admin == True:
        user_up_to_date = User.query.get_or_404(id) 
        body_json = request.get_json()
        user_name = body_json.get("user_name", None)
        password = body_json.get("password")
        is_active = body_json.get("is_active", None)
        is_admin = body_json.get("is_admin", None)

        user_up_to_date.user_name = user_name
        user_up_to_date.password = password
        user_up_to_date.is_active = is_active
        user_up_to_date.is_admin = is_admin

        db.session.commit()
        return jsonify(user_up_to_date.serialize()), 200

    else:
        return jsonify("Sorry folk, this is just for admins.")

@api.route("/login", methods=["POST"]) 
def sign_in():
    status = "NOP"
    body = request.get_json()
    user_name = body.get("user_name", None)
    password = body.get("password", None)
    
    user = User.query.filter_by(user_name=user_name).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({"status": status, "msg": "Are you sure folk? Please, try again."}), 401
    status = "OK"
    access_token = create_access_token(identity=user.serialize())
    return jsonify(status = status, user=user.serialize(), accessToken=access_token)

######       CUSTOMERS SECTION           ######

def current_user(identity):
  return User.query.get(identity["id"])

    ###CREATING NEW CUSTOMER###
@api.route("/customer", methods=["POST"])
@jwt_required()
def create_customer():
    user = current_user(get_jwt_identity())
    if request.method == "POST":
        body_json = request.get_json()
        name = body_json.get('name', None)
        surname = body_json.get('surname', None)

        #Received binary file in body_json & storing in cloudinary --> Cloudinary store OK
        avatar_cloudinary = cloudinary.uploader.upload(body_json.get("avatar_url"), folder = "agile_monkeys")
        avatar_url = avatar_cloudinary["secure_url"]
        
        customer = Customer(name, surname, avatar_url, user)
        db.session.add(customer)
        db.session.commit()
        return (customer.serialize()), 200

    ###GETTING LIST OF ALL CUSTOMERS###

@api.route("/customers", methods=["GET"])
@jwt_required()
def list_all_customers():
    user = current_user(get_jwt_identity())
    customer = Customer.query.all()
    customers = list(map(lambda customer: customer.serialize(), customer))
    return jsonify(customers), 200

    ###GETTING SINGLE CUSTOMER###

@api.route("/customer/<int:id>", methods=["GET"])
@jwt_required()
def handle_customer(id):
    user = current_user(get_jwt_identity())
    customer = Customer.query.get(id)
    return (customer.serialize()), 200

    
    ###UPDATING NEW CUSTOMER FROM USER###

@api.route("/customer/<int:id>", methods=["PUT", "POST"]) 
@jwt_required()   
def update_customer(id):
    user = current_user(get_jwt_identity())
    customer_up_to_date = Customer.query.get_or_404(id)
    
    body_json = request.get_json()
    name = body_json.get("name", None)
    surname = body_json.get("surname", None)
    avatar_url = cloudinary.uploader.upload(body_json.get("avatar_url"), public_id = "agile_monkeys/avatar_image") 
    user_id = user.id

    if avatar_url is not None:
        cloudinary.uploader.destroy(customer_up_to_date.avatar_public())
    
    customer_up_to_date.name = name
    customer_up_to_date.surname = surname
    customer_up_to_date.avatar_url = avatar_url["url"]
    customer_up_to_date.user_id = user_id

    modification = Modifications(customer_up_to_date.id, user.id)
    db.session.add(modification)
    db.session.commit()

    return jsonify(customer_up_to_date.serialize(), modification.serialize()), 200
    
    ##DELETING CUSTOMER FROM USER###
@api.route("/customer/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_customer(id):
    user = current_user(get_jwt_identity())
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()

    return (customer.serialize()), 200