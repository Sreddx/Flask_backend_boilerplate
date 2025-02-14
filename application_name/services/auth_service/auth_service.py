from application_name.database import db
from application_name.models.user_models import User
from flask_jwt_extended import create_access_token

def register_user(user_data):
    if not user_data:
        return None, "Registration data is required.", 400
    try:
        new_user = User(
            email=user_data['email'],
            password=user_data['password'],  # In production, hash the password!
            name=user_data['name'],
            lastname=user_data['lastname'],
            secondLastname=user_data.get('secondLastname'),
            roleId=user_data.get('roleId', 1)  # Default role id.
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, None, 201
    except Exception as e:
        db.session.rollback()
        return None, f"Error registering user: {str(e)}", 500

def login_user(login_data):
    if not login_data:
        return None, "Login data is required.", 400
    try:
        # For demonstration: simple check. In production, use hashed passwords.
        user = User.query.filter_by(email=login_data['email']).first()
        if not user or user.password != login_data['password']:
            return None, "Invalid credentials.", 401
        # Create a JWT access token using the userId as identity.
        access_token = create_access_token(identity=user.userId)
        return access_token, None, 200
    except Exception as e:
        return None, f"Error logging in user: {str(e)}", 500

def logout_user():
    # Implement token revocation/blacklisting if needed.
    # Typically, logout is handled client side.
    return True, None, 200

def reset_password(email, new_password):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return None, "User not found", 404
        # In production, hash the new password.
        user.password = new_password
        db.session.commit()
        return user, None, 200
    except Exception as e:
        db.session.rollback()
        return None, f"Error resetting password: {str(e)}", 500
