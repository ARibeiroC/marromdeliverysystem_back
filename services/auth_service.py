from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from database import get_users_collection

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        """
        Autentica um usuário e gera um token JWT.
        Retorna o token de acesso se as credenciais forem válidas, caso contrário, None.
        """
        users_collection = get_users_collection()
        user = users_collection.find_one({"username": username})

        if user and check_password_hash(user["password_hash"], password):
            # Se a autenticação for bem-sucedida, cria um token de acesso
            access_token = create_access_token(identity=str(user["_id"]))
            return access_token
        return None
