import os
from datetime import timedelta
import urllib.parse

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_muito_segura_padrao')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'sua_chave_secreta_jwt_muito_segura_padrao')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) # Token expira em 1 hora

    MONGO_USER = os.environ.get('USER')
    MONGO_PASS = os.environ.get('PASS')
    MONGO_PORT = os.environ.get('PORT')
    MONGO_DATABASE = os.environ.get('DATABASE')
    MONGO_HOST = os.environ.get('MONGODB') # Assumindo que MONGODB contém o host/cluster

    if all([MONGO_USER, MONGO_PASS, MONGO_PORT, MONGO_DATABASE, MONGO_HOST]):
        # Codifica o nome de usuário e a senha para a URI
        encoded_user = urllib.parse.quote_plus(MONGO_USER)
        encoded_pass = urllib.parse.quote_plus(MONGO_PASS)
        MONGO_URI = f"mongodb+srv://{encoded_user}:{encoded_pass}@{MONGO_HOST}/{MONGO_DATABASE}?retryWrites=true&w=majority"
    else:
        # Fallback para URI local se as variáveis de ambiente não estiverem completas
        MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/fleet_management_db')