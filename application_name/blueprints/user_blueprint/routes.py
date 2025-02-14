from flask import Blueprint, request, jsonify, abort
from application_name.services import AuthService, UserService
from application_name.models import User

user_bp = Blueprint('user', __name__)
# Use AuthService for creating users and UserService for updating/deleting.
auth_service = AuthService()
user_service = UserService()

@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        abort(400, description="Missing user data.")
    user, error, status = auth_service.register_user(data)
    if error:
        abort(status, description=error)
    return jsonify(user.serialize()), status

@user_bp.route('/all', methods=['GET'])
def get_all_users():
    users_queryset = user_service.get_all_users()
    print(users_queryset)
    if len(users_queryset[0]) == 0:
        return jsonify({'message': 'No users found'}), 404
    user_list = [user.serialize() for user in users_queryset[0]]
    return jsonify({'users': user_list}), 200

@user_bp.route('/<user_id>', methods=['PUT'])
def update_existing_user(user_id):
    data = request.get_json()
    if not data:
        abort(400, description="Missing user data for update.")
    user, error, status = user_service.update_user(user_id, data)
    if error:
        abort(status, description=error)
    return jsonify(user.serialize()), status

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_existing_user(user_id):
    user, error, status = user_service.delete_user(user_id)
    if error:
        abort(status, description=error)
    return jsonify({'message': 'User deleted successfully'}), status
