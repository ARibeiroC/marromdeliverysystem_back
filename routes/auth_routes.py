from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para login de usuário e obtenção de token JWT.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    password = password if password is not None else ""

    if not username or not password:
        return jsonify({"message": "Nome de usuário e senha são obrigatórios"}), 400

    access_token = AuthService.authenticate_user(username, password)

    print(access_token) # Mantenha para depuração, se quiser ver o token no console do backend
    
    if access_token:
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401
