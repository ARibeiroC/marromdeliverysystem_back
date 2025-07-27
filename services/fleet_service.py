from datetime import datetime, timezone
from bson.objectid import ObjectId
from database.database import (
    get_departure_records_collection,
    get_value_exits_collection
)
from models.models import (
    create_user_document,
    create_departure_record_document,
    create_value_exit_document
)


class FleetService:
    FIXED_COD_SAIDA_VALOR = "SAIDA_PADRAO" # <--- ALtere este valor para o código fixo desejado

    @staticmethod
    def register_departure(nome_do_motorista, placa_do_veiculo, timestamp_saida=None):
        """
        Registra uma nova saída de veículo, puxando o valor_atual de um documento de Saida fixo.
        """
        departure_records_collection = get_departure_records_collection()
        value_exits_collection = get_value_exits_collection()

        try:
            # 1. Puxa o documento de Saida usando o código fixo definido na classe
            saida_doc = value_exits_collection.find_one({"cod": FleetService.FIXED_COD_SAIDA_VALOR})
            if not saida_doc:
                # Se o documento de Saida fixo não for encontrado, isso é um erro de configuração
                return {"error": f"Documento de Saída com código fixo '{FleetService.FIXED_COD_SAIDA_VALOR}' não encontrado. Por favor, configure-o no DB."}, 500

            valor_atual_pulled = saida_doc.get("valor_atual")

            # 2. Cria o registro de saída com o valor puxado E o cod_saida_valor fixo
            new_record = create_departure_record_document(
                nome_do_motorista, placa_do_veiculo, FleetService.FIXED_COD_SAIDA_VALOR, valor_atual_pulled, timestamp_saida
            )
            result = departure_records_collection.insert_one(new_record)
            return {"message": "Registro de saída criado com sucesso", "id": str(result.inserted_id)}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def add_value_exit(cod, valor_atual):
        """
        Registra um novo valor de saída (documento Saida).
        Se um registro com o mesmo 'cod' já existir, ele será atualizado.
        """
        value_exits_collection = get_value_exits_collection()
        try:
            existing_record = value_exits_collection.find_one({"cod": cod})

            if existing_record:
                update_result = value_exits_collection.update_one(
                    {"cod": cod},
                    {"$set": create_value_exit_document(cod, valor_atual)}
                )
                if update_result.modified_count > 0:
                    return {"message": "Saída de valor atualizada com sucesso", "cod": cod}, 200
                else:
                    return {"message": "Nenhuma alteração feita na saída de valor", "cod": cod}, 200
            else:
                new_value_exit = create_value_exit_document(cod, valor_atual)
                result = value_exits_collection.insert_one(new_value_exit)
                return {"message": "Saída de valor registrada com sucesso", "id": str(result.inserted_id)}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_departure_records_by_period(start_date, end_date):
        """
        Retorna todos os registros de saída dentro de um período especificado.
        """
        departure_records_collection = get_departure_records_collection()
        try:
            records = list(departure_records_collection.find({
                "timestamp_saida": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }))
            for record in records:
                record['_id'] = str(record['_id'])
            return records
        except Exception as e:
            print(f"Erro ao buscar registros de saída por período: {e}")
            return []

    @staticmethod
    def get_total_departure_records():
        """
        Retorna o número total de registros de saída na coleção.
        """
        departure_records_collection = get_departure_records_collection()
        try:
            return departure_records_collection.count_documents({}) # Conta todos os documentos
        except Exception as e:
            print(f"Erro ao contar o total de registros de saída: {e}")
            return 0
