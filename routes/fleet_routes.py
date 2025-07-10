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
    """
    data = request.get_json()
    motorista_id = data.get('motorista_id')
    veiculo_id = data.get('veiculo_id')
    observacoes = data.get('observacoes')
    timestamp_saida_str = data.get('timestamp_saida')

    if not motorista_id or not veiculo_id:
        return jsonify({"message": "ID do motorista e do veículo são obrigatórios"}), 400

    timestamp_saida = None
    if timestamp_saida_str:
        try:
            timestamp_saida = datetime.fromisoformat(timestamp_saida_str)
        except ValueError:
            return jsonify({"message": "Formato de data e hora inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)."}), 400

    response, status_code = FleetService.register_departure(motorista_id, veiculo_id, observacoes, timestamp_saida)
    return jsonify(response), status_code

@fleet_bp.route('/veiculos/<string:veiculo_id>/saidas_semanais', methods=['GET'])
@jwt_required() # Protegida: requer autenticação
def get_vehicle_weekly_departures(veiculo_id):
    """
    Rota protegida para obter o número de saídas semanais de um veículo específico.
    """
    data_str = request.args.get('data')
    data_referencia = datetime.utcnow() # Padrão para a semana atual
    if data_str:
        try:
            data_referencia = datetime.strptime(data_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    weekly_count = FleetService.count_weekly_departures(veiculo_id, data_referencia)
    return jsonify({
        "veiculo_id": veiculo_id,
        "saidas_semanais": weekly_count
    }), 200

@fleet_bp.route('/frota/saidas_semanais', methods=['GET'])
@jwt_required() # Protegida: requer autenticação
def get_fleet_weekly_departures_route():
    """
    Rota protegida para obter o número de saídas semanais para toda a frota.
    """
    data_str = request.args.get('data')
    data_referencia = datetime.utcnow() # Padrão para a semana atual
    if data_str:
        try:
            data_referencia = datetime.strptime(data_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    fleet_departures = FleetService.get_fleet_weekly_departures(data_referencia)
    return jsonify(fleet_departures), 200

@fleet_bp.route('/veiculos', methods=['POST'])
@jwt_required() # Protegida: requer autenticação
def add_vehicle_route():
    """
    Rota protegida para adicionar um novo veículo.
    """
    data = request.get_json()
    cod = data.get('cod')
    placa = data.get('placa')
    modelo = data.get('modelo')
    ano = data.get('ano')

    if not cod or not placa or not modelo:
        return jsonify({"message": "Código, placa e modelo do veículo são obrigatórios"}), 400

    response, status_code = FleetService.add_vehicle(cod, placa, modelo, ano)
    return jsonify(response), status_code

@fleet_bp.route('/motoristas', methods=['POST'])
@jwt_required() # Protegida: requer autenticação
def add_driver_route():
    """
    Rota protegida para adicionar um novo motorista.
    """
    data = request.get_json()
    cod = data.get('cod')
    nome_completo = data.get('nome_completo')
    numero_cnh = data.get('numero_cnh')

    if not cod or not nome_completo or not numero_cnh:
        return jsonify({"message": "Código, nome completo e número da CNH do motorista são obrigatórios"}), 400

    response, status_code = FleetService.add_driver(cod, nome_completo, numero_cnh)
    return jsonify(response), status_code

@fleet_bp.route('/saidas_valor', methods=['POST'])
@jwt_required() # Protegida: requer autenticação
def add_value_exit_route():
    """
    Rota protegida para registrar um novo valor de saída.
    """
    data = request.get_json()
    cod = data.get('cod')
    valor_saida = data.get('valor_saida')

    if not cod or valor_saida is None:
        return jsonify({"message": "Código e valor da saída são obrigatórios"}), 400
    if not isinstance(valor_saida, (int, float)):
        return jsonify({"message": "Valor da saída deve ser um número"}), 400

    response, status_code = FleetService.add_value_exit(cod, valor_saida)
    return jsonify(response), status_code

@fleet_bp.route('/saidas_valor/total', methods=['GET'])
@jwt_required() # Protegida: requer autenticação
def get_total_value_exits_route():
    """
    Rota protegida para obter a somatória dos valores de saída em um período.
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

    total_value = FleetService.get_total_value_exits_by_period(start_date, end_date)
    return jsonify({"total_valor_saidas": total_value}), 200

@fleet_bp.route('/teste', methods=['GET']) # AGORA ESTÁ CORRETO: methods=['GET']
def test_res():
    return jsonify({'msg': 'requisição get funcionando'})
