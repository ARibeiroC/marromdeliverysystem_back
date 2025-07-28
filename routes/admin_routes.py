from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.admin_service import AdminService
from services.auth_service import AuthService

admin_bp = Blueprint('admin', __name__)

def superadmin_required():
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") == "superadmin":
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Acesso não autorizado: Requer papel de superadministrador"}), 403
        return decorator
    return wrapper

@admin_bp.route('/usage_counts/general', methods=['GET'])
@superadmin_required() # Protegido: requer papel de superadministrador
def get_general_usage_counts_route():
    """
    Rota protegida para superadministradores obterem a contagem geral de uso do sistema por tipo de ação.
    """
    try:
        general_counts = AdminService.get_general_usage_counts()
        return jsonify(general_counts), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao obter contagens gerais de uso: {str(e)}"}), 500
