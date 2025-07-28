from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from database.database import get_users_collection
from datetime import datetime, timezone, timedelta
from services.usage_logger_service import UsageLoggerService
from bson.objectid import ObjectId # NOVO: Importar ObjectId

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        """
        Autentica um usuário e gera um token JWT.
        Retorna o token de acesso se as credenciais forem válidas, caso contrário, None.
        """
        users_collection = get_users_collection()
        print(f"Tentando autenticar usuário: {username}")

        user = users_collection.find_one({"username": username})

        if user:
            print(f"Usuário '{username}' encontrado no DB.")
            # Verifica se o usuário autenticado NÃO é um superadministrador antes de logar
            # is_superadmin_user é avaliado corretamente agora
            is_superadmin_user = AuthService.is_superadmin(str(user["_id"]))

            if check_password_hash(user["password_hash"], password):
                print(f"Senha para '{username}' corresponde. Autenticação bem-sucedida.")

                now = datetime.now(timezone.utc)
                next_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                expires_delta = next_midnight - now

                access_token = create_access_token(
                    identity=str(user["_id"]),
                    expires_delta=expires_delta,
                    additional_claims={"role": user.get("role", "user")}
                )
                # SÓ LOGA SE NÃO FOR SUPERADMIN
                if not is_superadmin_user:
                    UsageLoggerService.log_action(
                        action_type="login_sucesso",
                        details={"username": username, "role": user.get("role", "user")}
                    )
                return access_token
            else:
                print(f"Senha para '{username}' NÃO corresponde.")
                # SÓ LOGA SE NÃO FOR SUPERADMIN (para tentativas falhas também)
                if not is_superadmin_user:
                    UsageLoggerService.log_action(
                        action_type="login_falha",
                        details={"username": username, "reason": "credenciais_invalidas"}
                    )
        else:
            print(f"Usuário '{username}' NÃO encontrado no DB.")
            # Loga falha para usuário inexistente, pois não sabemos se seria superadmin
            UsageLoggerService.log_action(
                action_type="login_falha",
                details={"username": username, "reason": "usuario_nao_encontrado"}
            )
        return None

    @staticmethod
    def get_user_role(user_id):
        """
        Retorna o papel de um usuário pelo seu ID.
        """
        users_collection = get_users_collection()
        try:
            # CORRIGIDO: Converte user_id para ObjectId antes de buscar no MongoDB
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            return user.get("role", "user") if user else None
        except Exception as e:
            # Loga o erro se houver problema na conversão ou busca
            print(f"Erro ao buscar papel do usuário {user_id}: {e}")
            return None # Retorna None em caso de erro ou se o usuário não for encontrado

    @staticmethod
    def is_superadmin(user_id):
        """
        Verifica se um usuário tem o papel de superadministrador.
        """
        return AuthService.get_user_role(user_id) == "superadmin"
