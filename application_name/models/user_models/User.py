from mongoengine import Document, StringField, IntField
from flask_login import UserMixin

class User(Document, UserMixin):
    # MongoEngine Document fields
    email = StringField(required=True, unique=True, max_length=120)
    password = StringField(required=True, max_length=120)
    status = StringField(default='deshabilitado', choices=('activo', 'pendiente', 'deshabilitado'))
    name = StringField(required=True, max_length=120)
    lastname = StringField(required=True, max_length=120)
    secondLastname = StringField(max_length=120)
    roleId = IntField(default=1)

    # Convert the auto-generated _id (ObjectId) to a string for Flask-Login
    def get_id(self):
        return str(self.id)

    # Serialize for JSON responses
    def serialize(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "status": self.status,
            "name": self.name,
            "lastname": self.lastname,
            "secondLastname": self.secondLastname,
            "roleId": self.roleId,
        }
