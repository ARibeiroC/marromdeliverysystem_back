import os
from datetime import timedelta, datetime, timezone # Importar datetime e timezone
import urllib.parse # Importar para codificação de URL

class Config:
    # Chaves secretas para o Flask e JWT
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_muito_segura_padrao')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'sua_chave_secreta_jwt_muito_segura_padrao')


    # Configurações do MongoDB
    # Construindo a URI do MongoDB a partir das variáveis de ambiente
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
