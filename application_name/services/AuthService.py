from flask_jwt_extended import create_access_token
from application_name.models import User

class AuthService:
    def register_user(self, user_data):
        """
        Creates a new User document and saves it to MongoDB.
        """
        if not user_data:
            return None, "Registration data is required.", 400
        try:
            new_user = User(
                email=user_data['email'],
                password=user_data['password'],  # In production, store a hashed password.
                name=user_data['name'],
                lastname=user_data['lastname'],
                secondLastname=user_data.get('secondLastname'),
                roleId=user_data.get('roleId', 1)
            )
            new_user.save()
            return new_user, None, 201
        except Exception as e:
            return None, f"Error registering user: {str(e)}", 500

    def login_user(self, login_data):
        """
        Authenticates a user and creates a JWT token.
        """
        if not login_data:
            return None, "Login data is required.", 400
        try:
            user = User.objects(email=login_data['email']).first()
            if not user or user.password != login_data['password']:
                return None, "Invalid credentials.", 401
            
            token = create_access_token(identity=str(user.id))
            return token, None, 200
        except Exception as e:
            return None, f"Error logging in user: {str(e)}", 500

    def reset_password(self, email, new_password):
        """
        Resets the password for a user identified by email.
        """
        if not email or not new_password:
            return None, "Email and new password are required.", 400
        try:
            user = User.objects(email=email).first()
            if not user:
                return None, "User not found.", 404
            user.password = new_password  # In production, hash the password.
            user.save()
            return user, None, 200
        except Exception as e:
            return None, f"Error resetting password: {str(e)}", 500

    def change_password(self, user_id, current_password, new_password):
        """
        Changes a user's password after validating the current password.
        """
        if not current_password or not new_password:
            return None, "Both current and new password are required.", 400
        try:
            user = User.objects(id=user_id).first()
            if not user:
                return None, "User not found.", 404
            if user.password != current_password:
                return None, "Current password is incorrect.", 401
            user.password = new_password  # In production, hash the new password.
            user.save()
            return user, None, 200
        except Exception as e:
            return None, f"Error changing password: {str(e)}", 500

    def forgot_password(self, email):
        """
        Processes a forgot-password request.
        In production, this would generate a reset token and send an email.
        """
        if not email:
            return None, "Email is required.", 400
        try:
            user = User.objects(email=email).first()
            if not user:
                return None, "User not found.", 404
            # Simulate sending a reset password email.
            return {"message": "Password reset email sent."}, None, 200
        except Exception as e:
            return None, f"Error processing forgot password: {str(e)}", 500

    def verify_email(self, token):
        """
        Verifies a user's email based on a token.
        In production, decode the token and update the user's verification status.
        """
        if not token:
            return None, "Verification token is required.", 400
        try:
            # Simulate email verification logic.
            return {"message": "Email verified successfully."}, None, 200
        except Exception as e:
            return None, f"Error verifying email: {str(e)}", 500
