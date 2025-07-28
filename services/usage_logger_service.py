from database.database import get_usage_logs_collection
from models.models import create_usage_log_document
from flask import request # Para obter o IP do cliente e contexto da requisição
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request # Para obter o ID do usuário logado

class UsageLoggerService:
    @staticmethod
    def log_action(action_type, details=None):
        """
        Registra uma ação de uso do sistema na coleção de logs.
        Obtém automaticamente o user_id (se logado) e o IP do cliente.
        """
        usage_logs_collection = get_usage_logs_collection()
        user_id = None
        ip_address = None

        # Tenta obter o user_id do token JWT (se houver e for válido)
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            if current_user_id:
                user_id = current_user_id
        except Exception:
            # Não faz nada se não houver token ou for inválido, user_id permanece None
            pass

        # Obtém o endereço IP do cliente
        # Em produção, você pode precisar de request.headers.get('X-Forwarded-For')
        ip_address = request.remote_addr

        log_document = create_usage_log_document(
            action_type=action_type,
            details=details,
            user_id=user_id,
            ip_address=ip_address
        )
        try:
            usage_logs_collection.insert_one(log_document)
            # print(f"Log de uso registrado: {action_type} por {user_id or 'Anônimo'} de {ip_address}") # Para depuração
        except Exception as e:
            print(f"Erro ao registrar log de uso: {e}")
