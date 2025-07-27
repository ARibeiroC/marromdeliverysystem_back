from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from database.database import get_users_collection # Corrigido para database.database
from datetime import datetime, timezone, timedelta # CORRIGIDO: Importar datetime, timezone, timedelta

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        """
        Autentica um usuário e gera um token JWT.
        Retorna o token de acesso se as credenciais forem válidas, caso contrário, None.
        """
        users_collection = get_users_collection()
        print(f"Tentando autenticar usuário: {username}") # Log de depuração

        user = users_collection.find_one({"username": username})

        if user:
            print(f"Usuário '{username}' encontrado no DB.") # Log de depuração
            # print(f"Senha fornecida (primeiros 5 chars): {password[:5]}...") # Log de depuração
            # print(f"Hash da senha no DB (primeiros 5 chars): {user['password_hash'][:5]}...") # Log de depuração

            if check_password_hash(user["password_hash"], password):
                print(f"Senha para '{username}' corresponde. Autenticação bem-sucedida.") # Log de depuração

                # Calcular expires_delta para a próxima meia-noite
                now = datetime.now(timezone.utc)
                next_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                expires_delta = next_midnight - now

                access_token = create_access_token(
                    identity=str(user["_id"]),
                    expires_delta=expires_delta # CORRIGIDO: Passar o timedelta calculado
                )
                return access_token
            else:
                print(f"Senha para '{username}' NÃO corresponde.") # Log de depuração
        else:
            print(f"Usuário '{username}' NÃO encontrado no DB.") # Log de depuração
        return None
