from application_name.database import db  # Adjust import path as necessary
from application_name.models.user_models import User
from flask_jwt_extended import get_jwt_identity

def get_user_by_email(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return None, "User not found", 404
        return user, None, 200
    except Exception as e:
        return None, f"Error getting user by email: {str(e)}", 500

def get_user_from_jwt():
    user_id = get_jwt_identity()
    user = User.query.filter_by(userId=user_id).first()
    if not user:
        raise Exception("User not found")
    return user

def create_defined_role_user(user_data):
    if not user_data:
        return None, "User data is required to create a new user.", 400
    try:
        new_user = User(
            email=user_data['email'],
            password=user_data['password'],
            name=user_data['name'],
            lastname=user_data['lastname'],
            secondLastname=user_data.get('secondLastname'),
            agentDetailId=user_data.get('agentDetailId'),
            roleId=user_data['roleId']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, None, 201
    except Exception as e:
        db.session.rollback()
        return None, f"Error creating user: {str(e)}", 500

def create_user(user_data):
    if not user_data:
        return None, "User data is required to create a new user.", 400
    try:
        new_user = User(
            email=user_data['email'],
            password=user_data['password'],
            name=user_data['name'],
            lastname=user_data['lastname'],
            secondLastname=user_data.get('secondLastname'),
            agentDetailId=None,
            roleId=1  # Default role id for standard users.
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, None, 201
    except Exception as e:
        db.session.rollback()
        return None, f"Error creating user: {str(e)}", 500

def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return None, "User not found", 404
        return user, None, 200
    except Exception as e:
        return None, f"Error retrieving user: {str(e)}", 500

def update_user(user_id, user_data):
    user = User.query.get(user_id)
    if not user:
        return None, "User not found", 404
    try:
        user.email = user_data.get('email', user.email)
        user.password = user_data.get('password', user.password)
        user.status = user_data.get('status', user.status)
        user.name = user_data.get('name', user.name)
        user.lastname = user_data.get('lastname', user.lastname)
        user.secondLastname = user_data.get('secondLastname', user.secondLastname)
        user.roleId = user_data.get('roleId', user.roleId)
        db.session.commit()
        return user, None, 200
    except Exception as e:
        db.session.rollback()
        return None, f"Error updating user: {str(e)}", 500

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None, "User not found", 404
    try:
        db.session.delete(user)
        db.session.commit()
        return user, None, 200
    except Exception as e:
        db.session.rollback()
        return None, f"Error deleting user: {str(e)}", 500

def save_user_info(user, user_data):
    try:
        user.email = user_data.get('email', user.email)
        user.password = user_data.get('password', user.password)
        user.status = user_data.get('status', user.status)
        user.name = user_data.get('name', user.name)
        user.lastname = user_data.get('lastname', user.lastname)
        user.secondLastname = user_data.get('secondLastname', user.secondLastname)
        user.roleId = user_data.get('roleId', user.roleId)
        user.agentDetailId = user_data.get('agentDetailId', user.agentDetailId)
        db.session.commit()
        return user, None, 200
    except Exception as e:
        db.session.rollback()
        return None, f"Error updating user info: {str(e)}", 500
