import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import auth_bp
from routes.fleet_routes import fleet_bp
from database import get_users_collection # Importar para criar usuário inicial
from models import create_user_document # Importar para criar usuário inicial
from werkzeug.security import generate_password_hash # Importar para criar usuário inicial
from dotenv import load_dotenv # Importar para carregar variáveis de ambiente
from flask_cors import CORS # Importar Flask-CORS

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a instância do Flask aqui, no nível superior do módulo
# Isso permite que o Gunicorn a encontre.
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa Flask-JWT-Extended
jwt = JWTManager(app)

# Inicializa Flask-CORS
CORS(app) # Permite CORS para todas as rotas e origens (apenas para desenvolvimento)

# Registra os Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(fleet_bp, url_prefix='/api/v1')

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

# Rota de teste
@app.route('/')
def home():
    return jsonify({'msg': "Bem-vindo à API de Gestão de Frota!"})

# Função para criar um usuário gestor inicial (apenas para setup/teste)
@app.cli.command('create-initial-user')
def create_initial_user():
    """Cria um usuário gestor inicial no banco de dados."""
    users_collection = get_users_collection()
    username = os.environ.get('INITIAL_ADMIN_USERNAME', 'admin')
    password = os.environ.get('INITIAL_ADMIN_PASSWORD', 'adminpass')

    if users_collection.find_one({"username": username}):
        print(f"Usuário '{username}' já existe.")
    else:
        new_user = create_user_document(username, password, role="gestor")
        users_collection.insert_one(new_user)
        print(f"Usuário gestor '{username}' criado com sucesso.")

# Remova o bloco if __name__ == '__main__': se você estiver usando Gunicorn para rodar
# ou mantenha-o apenas para testes locais com `python app.py`
if __name__ == '__main__':
    app.run(debug=True)
