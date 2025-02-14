import os
from datetime import timedelta

class Config:
    # General settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Fallback for non‑critical environments: this value may be overridden in child classes.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///development.db')
    
    # Optional settings (for example, for CORS)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    CORS_SUPPORTS_CREDENTIALS = True

    # Base required env variables (for all environments)
    REQUIRED_ENV_VARS = ['SECRET_KEY', 'JWT_SECRET_KEY']
    
    def __init__(self):
        # Validate required variables for all environments
        missing = [var for var in self.REQUIRED_ENV_VARS if not os.environ.get(var)]
        if missing:
            raise RuntimeError("Missing required environment variables: " + ", ".join(missing))

class DevelopmentConfig(Config):
    DEBUG = True
    # Allow developers to override the DB URL; fallback to a file-based SQLite.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///development.db')

class QAConfig(Config):
    DEBUG = True
    TESTING = True
    # QA must provide a QA_DATABASE_URL; no fallback here.
    REQUIRED_ENV_VARS = Config.REQUIRED_ENV_VARS + ['QA_DATABASE_URL']
    
    def __init__(self):
        super().__init__()
        db_url = os.environ.get('QA_DATABASE_URL')
        if not db_url:
            raise RuntimeError("Missing required environment variable: QA_DATABASE_URL for QA environment.")
        self.SQLALCHEMY_DATABASE_URI = db_url

class ProductionConfig(Config):
    DEBUG = False
    # Production must have DATABASE_URL provided; no fallback allowed.
    REQUIRED_ENV_VARS = Config.REQUIRED_ENV_VARS + ['DATABASE_URL']
    
    def __init__(self):
        super().__init__()
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise RuntimeError("Missing required environment variable: DATABASE_URL for production environment.")
        self.SQLALCHEMY_DATABASE_URI = db_url

class TestingConfig(Config):
    TESTING = True
    # For tests, fallback to a testing SQLite if not provided.
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///testing.db')

def get_config(env_name):
    """
    Returns the appropriate configuration class based on the environment name.
    """
    config_mapping = {
        'development': DevelopmentConfig,
        'qa': QAConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    # Default to Config if env_name doesn't match.
    return config_mapping.get(env_name, Config)()