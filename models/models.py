from datetime import datetime, timezone # Adicionado timezone
# from bson.objectid import ObjectId # Para trabalhar com IDs do MongoDB
from werkzeug.security import generate_password_hash # Para hash de senhas

# Funções auxiliares para criar documentos com IDs e timestamps

def create_user_document(username, password, role="gestor"):
    """Cria um documento para a coleção de usuários."""
    return {
        "username": username,
        "password_hash": generate_password_hash(password),
        "role": role,
        "timestamp_criacao": datetime.now(timezone.utc)
    }

def create_value_exit_document(cod, valor_atual, valor_anterior=None):
    """
    Cria um documento para a coleção de saídas (de valor),
    armazenando o valor atual e o valor anterior.
    """
    return {
        "cod": cod,
        "valor_atual": float(valor_atual),
        "timestamp_registro": datetime.now(timezone.utc)
    }

def create_departure_record_document(nome_do_motorista, placa_do_veiculo, valor_atual_pulled, timestamp_saida=None):
    """
    Cria um documento para a coleção de registros de saída,
    contendo nome do motorista, placa do veículo e timestamp.
    """
    return {
        "nome_do_motorista": nome_do_motorista,
        "placa_do_veiculo": placa_do_veiculo,
        "cod_saida_valor": float(valor_atual_pulled),
        "timestamp_saida": timestamp_saida if timestamp_saida else datetime.now(timezone.utc),
    }
