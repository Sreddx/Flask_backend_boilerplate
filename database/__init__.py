
from mongoengine import connect

def init_db(app):
    """
    Initialize MongoEngine with the Flask app config.
    """
    # This uses the MONGO_URI from your app.config
    connect(host=app.config['MONGO_URI'])
