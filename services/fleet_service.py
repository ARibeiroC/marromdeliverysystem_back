from datetime import datetime
from bson.objectid import ObjectId
from database import (
    get_departure_records_collection,
    get_vehicles_collection,
    get_drivers_collection,
    get_value_exits_collection
)
from models import (
    create_departure_record_document,
    create_vehicle_document,
    create_driver_document,
    create_value_exit_document
)
from utils.date_utils import get_week_start_end

class FleetService:
    @staticmethod
    def register_departure(motorista_id, veiculo_id, observacoes=None, timestamp_saida=None):
        """
        Registra uma nova saída de veículo.
        """
        departure_records_collection = get_departure_records_collection()
        try:
            # Verifica se motorista e veículo existem
            if not get_drivers_collection().find_one({"_id": ObjectId(motorista_id)}):
                return {"error": "Motorista não encontrado"}, 404
            if not get_vehicles_collection().find_one({"_id": ObjectId(veiculo_id)}):
                return {"error": "Veículo não encontrado"}, 404

            new_record = create_departure_record_document(
                motorista_id, veiculo_id, observacoes, timestamp_saida
            )
            result = departure_records_collection.insert_one(new_record)
            return {"message": "Registro de saída criado com sucesso", "id": str(result.inserted_id)}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def count_weekly_departures(veiculo_id, data_referencia):
        """
        Conta o número de dias distintos em que um veículo saiu na semana de trabalho.
        """
        departure_records_collection = get_departure_records_collection()
        try:
            start_of_week, end_of_week = get_week_start_end(data_referencia)

            # Busca todos os registros de saída para o veículo dentro do período da semana
            records = departure_records_collection.find({
                "veiculo_id": ObjectId(veiculo_id),
                "timestamp_saida": {
                    "$gte": start_of_week,
                    "$lte": end_of_week
                }
            })

            # Usa um conjunto para armazenar os dias da semana distintos
            distinct_days = set()
            for record in records:
                # Adiciona o dia da semana (0=Seg, 1=Ter, ..., 4=Sex) ao conjunto
                # Apenas consideramos dias de segunda a sexta (0 a 4)
                if record["timestamp_saida"].weekday() < 5:
                    distinct_days.add(record["timestamp_saida"].date())

            return len(distinct_days)
        except Exception as e:
            print(f"Erro ao contar saídas semanais: {e}")
            return 0 # Retorna 0 em caso de erro

    @staticmethod
    def get_fleet_weekly_departures(data_referencia):
        """
        Obtém o número de saídas semanais para cada veículo da frota.
        """
        vehicles_collection = get_vehicles_collection()
        all_vehicles = vehicles_collection.find({"ativo": True})
        fleet_departures = []

        for vehicle in all_vehicles:
            veiculo_id = str(vehicle["_id"])
            weekly_count = FleetService.count_weekly_departures(veiculo_id, data_referencia)
            fleet_departures.append({
                "veiculo_id": veiculo_id,
                "cod": vehicle.get("cod"),
                "placa": vehicle.get("placa"),
                "modelo": vehicle.get("modelo"),
                "saidas_semanais": weekly_count
            })
        return fleet_departures

    @staticmethod
    def add_vehicle(cod, placa, modelo, ano=None):
        """Adiciona um novo veículo."""
        vehicles_collection = get_vehicles_collection()
        if vehicles_collection.find_one({"$or": [{"cod": cod}, {"placa": placa}]}):
            return {"error": "Veículo com este código ou placa já existe"}, 409
        new_vehicle = create_vehicle_document(cod, placa, modelo, ano)
        result = vehicles_collection.insert_one(new_vehicle)
        return {"message": "Veículo adicionado com sucesso", "id": str(result.inserted_id)}, 201

    @staticmethod
    def add_driver(cod, nome_completo, numero_cnh):
        """Adiciona um novo motorista."""
        drivers_collection = get_drivers_collection()
        if drivers_collection.find_one({"$or": [{"cod": cod}, {"numero_cnh": numero_cnh}]}):
            return {"error": "Motorista com este código ou CNH já existe"}, 409
        new_driver = create_driver_document(cod, nome_completo, numero_cnh)
        result = drivers_collection.insert_one(new_driver)
        return {"message": "Motorista adicionado com sucesso", "id": str(result.inserted_id)}, 201

    @staticmethod
    def add_value_exit(cod, valor_saida):
        """Registra um novo valor de saída."""
        value_exits_collection = get_value_exits_collection()
        if value_exits_collection.find_one({"cod": cod}):
            return {"error": "Saída de valor com este código já existe"}, 409
        new_value_exit = create_value_exit_document(cod, valor_saida)
        result = value_exits_collection.insert_one(new_value_exit)
        return {"message": "Saída de valor registrada com sucesso", "id": str(result.inserted_id)}, 201

    @staticmethod
    def get_total_value_exits_by_period(start_date, end_date):
        """
        Calcula a somatória dos valores de saída em um período.
        """
        value_exits_collection = get_value_exits_collection()
        try:
            records = value_exits_collection.find({
                "timestamp_registro": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            })
            total_value = sum(record.get("valor_saida", 0) for record in records)
            return total_value
        except Exception as e:
            print(f"Erro ao calcular somatória de saídas de valor: {e}")
            return 0.0
