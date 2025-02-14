from flask import Blueprint, jsonify, request, abort
from application_name.services import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        abort(400, description="Missing registration data.")
    user, error, status = auth_service.register_user(data)
    if error:
        abort(status, description=error)
    return jsonify(user.serialize()), status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        abort(400, description="Missing login data.")
    token, error, status = auth_service.login_user(data)
    if error:
        abort(status, description=error)
    return jsonify({'access_token': token}), status

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_endpoint():
    data = request.get_json()
    if not data or 'email' not in data or 'new_password' not in data:
        abort(400, description="Email and new password are required.")
    user, error, status = auth_service.reset_password(data['email'], data['new_password'])
    if error:
        abort(status, description=error)
    return jsonify(user.serialize()), status

@auth_bp.route('/change-password', methods=['POST'])
def change_password_endpoint():
    data = request.get_json()
    if not data or 'user_id' not in data or 'current_password' not in data or 'new_password' not in data:
        abort(400, description="User id, current password, and new password are required.")
    user, error, status = auth_service.change_password(data['user_id'], data['current_password'], data['new_password'])
    if error:
        abort(status, description=error)
    return jsonify(user.serialize()), status

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password_endpoint():
    data = request.get_json()
    if not data or 'email' not in data:
        abort(400, description="Email is required.")
    response, error, status = auth_service.forgot_password(data['email'])
    if error:
        abort(status, description=error)
    return jsonify(response), status

@auth_bp.route('/verify-email', methods=['GET'])
def verify_email_endpoint():
    token = request.args.get("token")
    if not token:
        abort(400, description="Missing token for email verification.")
    response, error, status = auth_service.verify_email(token)
    if error:
        abort(status, description=error)
    return jsonify(response), status
