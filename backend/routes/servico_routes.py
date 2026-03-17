from flask import Blueprint, request
from services.servico_service import (
    atualizar_servico,
    criar_servico,
    deletar_servico,
    listar_servicos,
)
from utils.api_response import api_response

servico_bp = Blueprint("servico", __name__, url_prefix="/servicos")


@servico_bp.route("", methods=["GET"])
def listar():
    servicos = listar_servicos()

    return api_response(200, "Serviços encontrados", servicos)


@servico_bp.route("", methods=["POST"])
def criar():
    dados = request.json
    try:
        servico = criar_servico(dados)
        return api_response(201, "Serviço criado", servico)
    except ValueError as e:
        return api_response(400, str(e))


@servico_bp.route("/<int:servico_id>", methods=["PUT"])
def atualizar(servico_id):
    dados = request.json
    try:
        servico = atualizar_servico(servico_id, dados)
        return api_response(200, "Serviço atualizado", servico)
    except ValueError as e:
        return api_response(400, str(e))


@servico_bp.route("/<int:servico_id>", methods=["DELETE"])
def deletar(servico_id):
    try:
        deletar_servico(servico_id)
        return api_response(200, "Serviço deletado")
    except ValueError as e:
        return api_response(400, str(e))
