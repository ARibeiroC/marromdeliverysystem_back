import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from config.config import Config
from routes.auth_routes import auth_bp
from routes.fleet_routes import fleet_bp
from routes.admin_routes import admin_bp
from database.database import get_users_collection
from models.models import create_user_document
from services.usage_logger_service import UsageLoggerService

from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime, timezone

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)
CORS(app)

# Registra os Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(fleet_bp, url_prefix='/api/v1')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

# Handler para erros de JWT
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({"message": "Token de autenticação ausente ou inválido"}), 401

@jwt.invalid_token_loader
def invalid_token_response(callback):
    return jsonify({"message": "Token de autenticação inválido"}), 401

@jwt.expired_token_loader
def expired_token_response(callback):
    return jsonify({"message": "Token de autenticação expirado"}), 401

@app.route('/')
def home():
    return "Bem-vindo à API de Gestão de Frota!"

@app.cli.command('create-initial-user')
def create_initial_user():
    """
    Cria um usuário superadministrador no banco de dados,
    APENAS se as variáveis de ambiente SUPERADMIN_USERNAME e SUPERADMIN_PASSWORD estiverem definidas.
    Não cria usuários padrão por segurança.
    """
    users_collection = get_users_collection()
    
    # Obtém as credenciais do superadministrador das variáveis de ambiente
    superadmin_username = os.environ.get('SUPERADMIN_USERNAME')
    superadmin_password = os.environ.get('SUPERADMIN_PASSWORD')

    # Verifica se as credenciais do superadministrador foram fornecidas
    if not superadmin_username or not superadmin_password:
        print("Aviso: Variáveis de ambiente 'SUPERADMIN_USERNAME' e/ou 'SUPERADMIN_PASSWORD' não definidas.")
        print("O usuário superadministrador NÃO será criado por segurança.")
        return

    # Verifica se o superadministrador já existe
    if users_collection.find_one({"username": superadmin_username}):
        print(f"Usuário superadmin '{superadmin_username}' já existe.")
    else:
        # Garante que a senha do superadmin seja uma string antes de passar para create_user_document
        if not isinstance(superadmin_password, str):
            print(f"Erro: Senha para '{superadmin_username}' não é uma string válida.")
            print("O usuário superadministrador NÃO será criado.")
            return

        new_superadmin = create_user_document(superadmin_username, superadmin_password, role="superadmin")
        users_collection.insert_one(new_superadmin)
        print(f"Usuário superadmin '{superadmin_username}' criado com sucesso.")


if __name__ == '__main__':
    app.run(debug=True)
