import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # MongoDB connection string
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/development_db')

    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    CORS_SUPPORTS_CREDENTIALS = True

    # Required environment variables for all environments
    REQUIRED_ENV_VARS = ['SECRET_KEY', 'JWT_SECRET_KEY']

    def __init__(self):
        missing = [var for var in self.REQUIRED_ENV_VARS if not os.environ.get(var)]
        if missing:
            raise RuntimeError("Missing required environment variables: " + ", ".join(missing))


class DevelopmentConfig(Config):
    DEBUG = True
    # Optionally override the default MONGO_URI
    MONGO_URI = os.environ.get('DEV_MONGO_URI', 'mongodb://localhost:27017/development_db')


class QAConfig(Config):
    DEBUG = True
    TESTING = True
    REQUIRED_ENV_VARS = Config.REQUIRED_ENV_VARS + ['QA_MONGO_URI']

    def __init__(self):
        super().__init__()
        db_url = os.environ.get('QA_MONGO_URI')
        if not db_url:
            raise RuntimeError("Missing required environment variable: QA_MONGO_URI for QA environment.")
        self.MONGO_URI = db_url


class ProductionConfig(Config):
    DEBUG = False
    REQUIRED_ENV_VARS = Config.REQUIRED_ENV_VARS + ['MONGO_URI']

    def __init__(self):
        super().__init__()
        db_url = os.environ.get('MONGO_URI')
        if not db_url:
            raise RuntimeError("Missing required environment variable: MONGO_URI for production environment.")
        self.MONGO_URI = db_url


class TestingConfig(Config):
    TESTING = True
    # For tests, we might have a special test DB
    MONGO_URI = os.environ.get('TEST_MONGO_URI', 'mongodb://localhost:27017/testing_db')


def get_config(env_name):
    config_mapping = {
        'development': DevelopmentConfig,
        'qa': QAConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    return config_mapping.get(env_name, Config)()
