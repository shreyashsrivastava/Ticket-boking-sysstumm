from accounts.api.schema import CreateUserSchema, LoginUserSchema
from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from accounts.models import User
# from website import db, jwt_redis_blocklist, ACCESS_EXPIRES
from website import db, ACCESS_EXPIRES
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError


auth_api = Blueprint("auth_api", __name__, url_prefix="/auth")

@auth_api.route("/api/signup", methods=["POST"])
@use_args(CreateUserSchema(), location="json")
def signup(args):
    args['password'] = generate_password_hash(args['password'])
    try:
        new_user = User(**args)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": "User created"}), 201
    except IntegrityError:
        return jsonify({"error": "User already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_api.route("/api/login", methods=["POST"])
@use_args(LoginUserSchema(), location="json")
def login(args):
    user = User.query.filter_by(email=args['email']).first()
    if user:
        if user.is_admin == True:
            return jsonify({"error": "Login using admin login!"}), 400
        if check_password_hash(user.password, args['password']):
            access_token = create_access_token(identity=user.email)
            print(access_token)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 400
    else:
        return jsonify({"error": "Email does not exist"}), 400
    
@auth_api.route("/api/admin/login", methods=["POST"])
@use_args(LoginUserSchema(), location="json")
def adminLogin(args):
    user = User.query.filter_by(email=args['email']).first()
    if user:
        if user.is_admin == True:
            if check_password_hash(user.password, args['password']):
                access_token = create_access_token(identity=user.email)
                return jsonify({"access_token": access_token, "is_admin": True}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 400
        else:
            return jsonify({"error": "This is only for admin"}), 400
    else:
        return jsonify({"error": "Email does not exist"}), 400
    
@auth_api.route("/api/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt()["jti"]
    print(jti)
    # jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")