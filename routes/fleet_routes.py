from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.fleet_service import FleetService
from datetime import datetime

fleet_bp = Blueprint('fleet', __name__)

@fleet_bp.route('/registros_saida', methods=['POST'])
def register_departure_public():
    """
    Rota pública para registrar uma saída de veículo.
    Acessível por motoristas sem autenticação.
    Espera 'nome_do_motorista' e 'placa_do_veiculo'.
    O 'cod_saida_valor' será fixo no backend.
    """
    data = request.get_json()
    nome_do_motorista = data.get('nome_do_motorista')
    placa_do_veiculo = data.get('placa_do_veiculo')
    # REMOVIDO: cod_saida_valor não é mais recebido da requisição
    timestamp_saida_str = data.get('timestamp_saida')

    if not nome_do_motorista or not placa_do_veiculo: # CORRIGIDO: Validação sem cod_saida_valor
        return jsonify({"message": "Nome do motorista e placa do veículo são obrigatórios"}), 400

    timestamp_saida = None
    if timestamp_saida_str:
        try:
            timestamp_saida = datetime.fromisoformat(timestamp_saida_str)
        except ValueError:
            return jsonify({"message": "Formato de data e hora inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)."}), 400

    # CORRIGIDO: Chamada ao serviço sem cod_saida_valor
    response, status_code = FleetService.register_departure(
        nome_do_motorista, placa_do_veiculo, timestamp_saida
    )
    return jsonify(response), status_code

@fleet_bp.route('/saidas_valor', methods=['POST'])
@jwt_required() # Protegida: requer autenticação
def add_value_exit_route():
    """
    Rota protegida para registrar um novo valor de saída (documento Saida).
    Espera 'cod' e 'valor_atual'.
    """
    data = request.get_json()
    cod = data.get('cod')
    valor_atual = data.get('valor_atual')

    if not cod or valor_atual is None:
        return jsonify({"message": "Código e valor atual são obrigatórios"}), 400
    if not isinstance(valor_atual, (int, float)):
        return jsonify({"message": "Valor atual deve ser um número"}), 400

    response, status_code = FleetService.add_value_exit(cod, valor_atual)
    return jsonify(response), status_code

@fleet_bp.route('/registros_saida/periodo', methods=['GET'])
@jwt_required() # Protegida: requer autenticação
def get_departure_records_by_period_route():
    """
    Rota protegida para obter todos os registros de saída em um período especificado.
    Espera os parâmetros de query 'start_date' e 'end_date' no formato YYYY-MM-DD.
    Exemplo de requisição: /api/v1/registros_saida/periodo?start_date=2024-06-01&end_date=2024-06-30
    """
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if not start_date_str or not end_date_str:
        return jsonify({"message": "Datas de início e fim são obrigatórias (YYYY-MM-DD)."}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    print(f"Buscando registros entre {start_date} e {end_date}")
    records = FleetService.get_departure_records_by_period(start_date, end_date)
    return jsonify(records), 200
