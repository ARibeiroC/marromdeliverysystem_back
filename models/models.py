from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

# Funções auxiliares para criar documentos com IDs e timestamps

def create_user_document(username, password, role="gestor"):
    """Cria um documento para a coleção de usuários."""
    return {
        "username": username,
        "password_hash": generate_password_hash(password),
        "role": role,
        "timestamp_criacao": datetime.now(timezone.utc)
    }

def create_value_exit_document(cod, valor_atual):
    """
    Cria um documento para a coleção de saídas (de valor),
    armazenando apenas o valor atual.
    """
    return {
        "cod": cod,
        "valor_atual": float(valor_atual),
        "timestamp_registro": datetime.now(timezone.utc)
    }

def create_departure_record_document(nome_do_motorista, placa_do_veiculo, cod_saida_valor, valor_atual_pulled, timestamp_saida=None):
    """
    Cria um documento para a coleção de registros de saída,
    contendo nome do motorista, placa do veículo, o código de saída de valor,
    e o valor atual de saída puxado do documento de Saida.
    """
    return {
        "nome_do_motorista": nome_do_motorista,
        "placa_do_veiculo": placa_do_veiculo,
        "cod_saida_valor": cod_saida_valor,
        "valor_atual": float(valor_atual_pulled),
        "timestamp_saida": timestamp_saida if timestamp_saida else datetime.now(timezone.utc),
    }


def create_usage_log_document(action_type, details=None, user_id=None, ip_address=None):
    """
    Cria um documento para a coleção de logs de uso do sistema.
    action_type: Tipo da ação (ex: 'login_sucesso', 'registro_saida', 'filtro_aplicado').
    details: Detalhes adicionais sobre a ação (opcional).
    user_id: ID do usuário que realizou a ação (se autenticado).
    ip_address: Endereço IP de onde a ação foi realizada.
    """
    return {
        "timestamp": datetime.now(timezone.utc),
        "action_type": action_type,
        "details": details,
        "user_id": user_id,
        "ip_address": ip_address
    }
