from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Create the SQLAlchemy db instance
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app and configure migrations.
    """
    db.init_app(app)
    migrate = Migrate(app, db)

    # If using SQLite in development, auto-create tables if they don’t exist
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        with app.app_context():
            db.create_all()
