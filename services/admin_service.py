from database.database import get_usage_logs_collection
from datetime import datetime, timedelta, timezone

class AdminService:
    @staticmethod
    def get_general_usage_counts(): # CORRIGIDO: Renomeado para refletir "geral"
        """
        Agrega os logs de uso para contar o número total de ações por tipo de ação.
        """
        usage_logs_collection = get_usage_logs_collection()
        
        # Pipeline de agregação para contar ações por action_type (geral)
        pipeline = [
            {
                "$group": {
                    "_id": "$action_type", # Agrupar apenas por tipo de ação
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "action_type": "$_id", # Renomeia _id para action_type
                    "count": 1
                }
            },
            {
                "$sort": {"action_type": 1} # Ordena por tipo de ação
            }
        ]

        try:
            results = list(usage_logs_collection.aggregate(pipeline))
            # Não há necessidade de formatar data, pois não há campo de data
            return results
        except Exception as e:
            print(f"Erro ao obter contagens gerais de uso: {e}")
            return []
