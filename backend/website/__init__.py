import redis
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from flask_mail import Mail
from flask_caching import Cache

db = SQLAlchemy()
DB_NAME = "project.db"

ACCESS_EXPIRES = timedelta(days=30)

# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["SECRET_KEY"] = "supersecretkasdfliasgafudbi2134rlisdjkbf"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "my-super-secret-salt-to-create-jwt-keep-this-secret-shh"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
cache = Cache(app)

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

db.init_app(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '21f1006542@ds.study.iitm.ac.in'
app.config['MAIL_DEFAULT_SENDER'] = '21f1006542@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'urfmnlhmxoygmwhf'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    """Return validation errors as JSON"""
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

CORS(app)

with app.app_context():
    db.create_all()

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def create_database(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print("DB Created")

# initialize celery
import tasks
from tasks.tasks import *

from .views import views
from accounts.auth import auth
from accounts.api.auth import auth_api
from shows.views import show
from shows.api.shows import show_api
from venue.views import venue
from venue.api.venue import venue_api
from ticket.views import ticket
from ticket.api.ticket import ticket_api
from accounts.models import User

app.register_blueprint(views)
app.register_blueprint(auth)
app.register_blueprint(auth_api)
app.register_blueprint(venue)
app.register_blueprint(venue_api)
app.register_blueprint(show)
app.register_blueprint(show_api)
app.register_blueprint(ticket)
app.register_blueprint(ticket_api)


with app.app_context():
    # create an admin user if not exists
    admin = User.query.filter_by(email="admin@admin.com").first()
    if not admin:
        admin = User(
            email="admin@admin.com",
            password="admin",
            name="admin",
            dob="2000-01-01",
            phone="1234567890",
            is_admin=True,
        )
        print("admin created")
        db.session.add(admin)
        db.session.commit()
    print("admin exists")
            
def create_app():
    return app
