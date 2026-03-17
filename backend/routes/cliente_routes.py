from flask import Blueprint, request
from services.cliente_service import criar_cliente, listar_cliente
from utils.api_response import api_response

cliente_bp = Blueprint("cliente", __name__, url_prefix="/clientes")


@cliente_bp.route("", methods=["GET"])
def listar():
    clientes = listar_cliente()

    return api_response(200, "Clientes encontrados", clientes)


@cliente_bp.route("", methods=["POST"])
def criar():
    dados = request.json

    try:
        cliente = criar_cliente(dados)

        return api_response(201, "Cliente criado", cliente)

    except ValueError as e:
        return api_response(400, str(e))
