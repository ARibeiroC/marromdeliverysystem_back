from pymongo import MongoClient
from config import Config

# Inicializa o cliente MongoDB
client = MongoClient(Config.MONGO_URI)
db = client.get_database() # Obtém o banco de dados especificado na MONGO_URI

# Funções auxiliares para acesso às coleções
def get_users_collection():
    return db.usuarios

def get_vehicles_collection():
    return db.veiculos

def get_drivers_collection():
    return db.motoristas

def get_value_exits_collection():
    return db.saidas

def get_departure_records_collection():
    return db.registros_saida
