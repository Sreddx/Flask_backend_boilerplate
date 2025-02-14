import os
from flask import Flask
from config import get_config
from database import init_db  # Now references our new MongoEngine-based init_db
from flask_cors import CORS
from application_name.extensions import setup_logging
from application_name.error_handlers import register_error_handlers
from application_name.middleware import register_middlewares
from application_name.extensions import jwt, login_manager, bcrypt

def create_app():
    env = os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    # Initialize MongoEngine
    init_db(app)

    setup_logging(app)

    # Setup extensions
    jwt.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Configure CORS
    cors_origins = app.config.get("CORS_ORIGINS")
    if cors_origins and cors_origins != ["*"]:
        CORS(app, origins=cors_origins, supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", True))
    else:
        CORS(app, supports_credentials=True)

    register_error_handlers(app)
    register_middlewares(app)

    # Example: import your blueprints
    from application_name.blueprints import auth_bp, user_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")

    return app
