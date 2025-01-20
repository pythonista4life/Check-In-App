from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from extensions.extensions import limiter
from config.config import get_config
from extensions.db import init_db
from extensions.jwt_config import init_jwt
from extensions.mail import init_mail
from resources.questions import blp as QuestionsBlueprint
from resources.users import blp as UsersBlueprint
from resources.friendships import blp as FriendshipsBlueprint

load_dotenv("secrets.env")


# Creates our app with specified configurations, extensions, blueprints
def create_app(db_url=None):
    app = Flask(__name__)

    # Load app configurations
    app.config.from_mapping(get_config())

    # Initialize extensions
    init_db(app)
    init_jwt(app)
    init_mail(app)

    limiter.init_app(app)

    # Register blueprints
    api = Api(app)
    api.register_blueprint(QuestionsBlueprint)
    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(FriendshipsBlueprint)

    return app
