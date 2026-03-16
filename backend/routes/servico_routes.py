from flask import Blueprint

from services.servico_service import listar_servicos
from utils.api_response import api_response

servico_bp = Blueprint("servico", __name__, url_prefix="/servicos")


@servico_bp.route("/", methods=["GET"])
def listar():
    servicos = listar_servicos()

    return api_response(200, "Serviços encontrados", servicos)
