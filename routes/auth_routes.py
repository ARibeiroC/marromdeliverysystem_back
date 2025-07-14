from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.auth_service import AuthService
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para login de usuário e obtenção de token JWT.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Nome de usuário e senha são obrigatórios"}), 400

    access_token = AuthService.authenticate_user(username, password)

    if access_token:
        return jsonify(access_token=generate_password_hash(access_token)), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401