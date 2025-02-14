from flask_login import UserMixin
from application_name.extensions import db  # ensure you import the db instance

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) 
    # For SQLite, SQLAlchemy will emulate Enum with a CHECK constraint.
    status = db.Column(db.Enum('activo', 'pendiente', 'deshabilitado', name='status'), 
                       nullable=False, default='deshabilitado')
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    secondLastname = db.Column(db.String(120), nullable=True)
    # Foreign Key: User to Role
    roleId = db.Column(db.Integer, db.ForeignKey('role.roleId'), nullable=False)
    # Foreign Key: User to AgentDetail (one-to-one)
    agentDetailId = db.Column(db.Integer, db.ForeignKey('agent_detail.agentDetailId'), unique=True, nullable=True)
   
    quotation = db.relationship('Quotation', back_populates='user', lazy=True)
    
    # Relationship: User to AgentDetail (one-to-one)
    agentDetail = db.relationship('AgentDetail', back_populates='user', uselist=False, lazy=True)
        
    def get_id(self):
        try:
            return str(self.userId)
        except AttributeError:
            raise NotImplementedError("No `userId` attribute - override `get_id`")
    
    def serialize(self):
        return {
            "userId": self.userId,
            "email": self.email,
            "status": self.status,
            "name": self.name,
            "lastname": self.lastname,
            "secondLastname": self.secondLastname,
            "agentId": self.agentDetail.serialize() if self.agentDetailId else None,
            "roleId": self.roleId
        }
