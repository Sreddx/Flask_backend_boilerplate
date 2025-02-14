# from flask_login import LoginManager
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
import logging


def setup_logging(app):
    """
    Setup logging configuration based on the app's configuration.
    """
    log_level = app.config.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=log_level,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    app.logger.info(f"Logging is set at {log_level} level.")
    
# login_manager = LoginManager()
# bcrypt = Bcrypt()
# jwt = JWTManager()