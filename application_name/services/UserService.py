from application_name.models import User

class UserService:
    def update_user(self, user_id, user_data):
        """
        Updates an existing User document in MongoDB.
        """
        if not user_data:
            return None, "User data is required.", 400
        try:
            user = User.objects(id=user_id).first()
            if not user:
                return None, "User not found.", 404

            user.update(
                email=user_data.get('email', user.email),
                password=user_data.get('password', user.password),
                status=user_data.get('status', user.status),
                name=user_data.get('name', user.name),
                lastname=user_data.get('lastname', user.lastname),
                secondLastname=user_data.get('secondLastname', user.secondLastname),
                roleId=user_data.get('roleId', user.roleId)
            )
            user.reload()  # Refresh the document with updated data
            return user, None, 200
        except Exception as e:
            return None, f"Error updating user: {str(e)}", 500

    def delete_user(self, user_id):
        """
        Deletes a User document from MongoDB.
        """
        try:
            user = User.objects(id=user_id).first()
            if not user:
                return None, "User not found.", 404
            user.delete()
            return user, None, 200
        except Exception as e:
            return None, f"Error deleting user: {str(e)}", 500
    
    def get_user_by_id(self, user_id):
        """
        Retrieves a User document by its ID.
        """
        try:
            user = User.objects(id=user_id).first()
            if not user:
                return None, "User not found.", 404
            return user, None, 200
        except Exception as e:
            return None, f"Error retrieving user: {str(e)}", 500
    
    def get_user_by_email(self, email):
        """
        Retrieves a User document by its email.
        """
        try:
            user = User.objects(email=email).first()
            if not user:
                return None, "User not found.", 404
            return user, None, 200
        except Exception as e:
            return None, f"Error retrieving user: {str(e)}", 500
    
    def get_all_users(self):
        """
        Retrieves all User documents from MongoDB.
        """
        try:
            users = User.objects.all()
            return users, None, 200
        except Exception as e:
            return None, f"Error retrieving users: {str(e)}", 500
