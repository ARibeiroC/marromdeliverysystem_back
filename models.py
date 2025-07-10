from datetime import datetime
from bson.objectid import ObjectId # Para trabalhar com IDs do MongoDB
from werkzeug.security import generate_password_hash # Para hash de senhas

# Funções auxiliares para criar documentos com IDs e timestamps

def create_user_document(username, password, role="gestor"):
    """Cria um documento para a coleção de usuários."""
    return {
        "username": username,
        "password_hash": generate_password_hash(password),
        "role": role,
        "timestamp_criacao": datetime.utcnow()
    }

def create_vehicle_document(cod, placa, modelo, ano=None, ativo=True):
    """Cria um documento para a coleção de veículos."""
    return {
        "cod": cod,
        "placa": placa,
        "modelo": modelo,
        "ano": ano,
        "timestamp_criacao": datetime.utcnow(),
        "ativo": ativo
    }

def create_driver_document(cod, nome_completo, numero_cnh):
    """Cria um documento para a coleção de motoristas."""
    return {
        "cod": cod,
        "nome_completo": nome_completo,
        "numero_cnh": numero_cnh,
        "timestamp_criacao": datetime.utcnow()
    }

def create_value_exit_document(cod, valor_saida):
    """Cria um documento para a coleção de saídas (de valor)."""
    return {
        "cod": cod,
        "valor_saida": float(valor_saida),
        "timestamp_registro": datetime.utcnow()
    }

def create_departure_record_document(motorista_id, veiculo_id, observacoes=None, timestamp_saida=None):
    """Cria um documento para a coleção de registros de saída."""
    return {
        "motorista_id": ObjectId(motorista_id), # Converte para ObjectId
        "veiculo_id": ObjectId(veiculo_id),     # Converte para ObjectId
        "timestamp_saida": timestamp_saida if timestamp_saida else datetime.utcnow(),
        "observacoes": observacoes
    }
