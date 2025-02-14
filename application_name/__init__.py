import os
from flask import Flask
from flask_migrate import upgrade
from config import get_config
from database import init_db
from flask_cors import CORS
from application_name.extensions import setup_logging
from application_name.error_handlers import register_error_handlers
from application_name.middleware import register_middlewares

def create_app():
    env = os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    
    app.config.from_object(get_config(env))

    # Initialize database and migrations
    init_db(app)

    # Run migrations automatically if database is empty
    with app.app_context():
        try:
            upgrade()
            app.logger.info("Database migrated successfully.")
        except Exception as e:
            app.logger.error(f"Database migration failed: {e}")

    setup_logging(app)
    
    # Configure CORS
    cors_origins = app.config.get("CORS_ORIGINS")
    if cors_origins and cors_origins != ["*"]:
        CORS(app, origins=cors_origins, supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", True))
    else:
        CORS(app, supports_credentials=True)

    register_error_handlers(app)
    register_middlewares(app)

    from application_name.blueprints import auth_bp, user_bp


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")

    return app
