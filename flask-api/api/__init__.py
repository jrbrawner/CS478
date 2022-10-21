"""Initialize app."""
from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from flask_security import SQLAlchemyUserDatastore, Security
from api.models.Users import User, Role
from api.models.db import db


PROFILE_PICS = "api/static/profile-pics"
UPLOADS = "api/uploads"

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
login_manager = LoginManager()

security = Security()


def create_app(config):
    """Construct the core app object."""
    app = Flask(__name__)

    if config == "dev":
        # Application Configuration
        app.config.from_object("config.DevConfig")
        app.config["PROFILE_PICS"] = PROFILE_PICS
        app.config["UPLOADS"] = UPLOADS
        app.config["MESSAGES_PER_PAGE"] = 10

    if config == "test":
        app.config.from_object("config.TestConfig")
    else:
        # change to prod for deployment
        app.config.from_object("config.DevConfig")

    # authentication
    app.config["LOGIN_DISABLED"] = True
    
    # Initialize Plugins
    db.init_app(app)
    security_ctx = security.init_app(app, user_datastore)

    @security_ctx.context_processor
    def security_context_processor():
        return abort(404)

    # Set up logging
    logging.basicConfig(
        filename="record.log",
        level=logging.DEBUG,
        format=f"%(asctime)s %(levelname)s %(name)s : %(message)s",
        filemode="w+",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    with app.app_context():

        from .routes.auth import auth_bp
        from .routes.app import app_bp
        from .routes.post import post_bp
        from .routes.friends import friend_bp
        from .routes.message import message_bp
        from .routes.profile import profile_bp

        # Register Blueprints

        app.register_blueprint(auth_bp)
        app.register_blueprint(app_bp)
        app.register_blueprint(post_bp)
        app.register_blueprint(friend_bp)
        app.register_blueprint(message_bp)
        app.register_blueprint(profile_bp)
        # Create Database Models
        db.create_all()

        # Compile static assets
        
        return app
