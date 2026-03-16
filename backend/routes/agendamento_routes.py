from datetime import datetime

from flask import Blueprint, request
from models.agendamento import Agendamento
from services.agendamento_service import (
    atualizar_agendamento,
    atualizar_status,
    criar_agendamento,
    listar_agendamento,
)
from services.relatorio_service import desempenho_semanal
from sqlalchemy.orm import joinedload
from utils.api_response import api_response

agendamento_bp = Blueprint("agendamento", __name__, url_prefix="/agendamentos")


@agendamento_bp.route("/", methods=["GET"])
def listar():
    agendamentos = listar_agendamento()

    return api_response(200, "Agendamentos encontrados", agendamentos)


@agendamento_bp.route("/", methods=["POST"])
def criar():
    dados = request.json

    try:
        resultado = criar_agendamento(dados)

        return api_response(
            201,
            "Agendamento criado",
            resultado,
        )
    except ValueError as e:
        return api_response(400, str(e))


@agendamento_bp.route("/<int:agendamento_id>", methods=["PUT"])
def atualizar(agendamento_id):
    dados = request.json

    autenticacao = dados.pop("admin", False)

    try:
        atualizar_agendamento(agendamento_id, dados, autenticacao)

        return api_response(200, "Agendamento atualizado", dados)

    except ValueError as e:
        return api_response(400, str(e))


@agendamento_bp.route("/<int:cliente_id>/status", methods=["PUT"])
def alterar_status(cliente_id: int):
    dados = request.json

    atualizar_status(cliente_id, dados)

    return api_response(200, "Status atualizado", dados)


@agendamento_bp.route("/historico", methods=["GET"])
def buscar_historico():
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    if not data_inicio or not data_fim:
        return api_response(400, "Informe a data inicial e data final")

    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
    data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

    if data_inicio > data_fim:
        return api_response(400, "Data inicial não pode ser maior que data final")

    agendamentos = (
        Agendamento.query.options(
            joinedload(Agendamento.cliente), joinedload(Agendamento.servicos)
        )
        .filter(Agendamento.data.between(data_inicio, data_fim))
        .all()
    )

    resultado = [a.to_dict() for a in agendamentos]

    return api_response(200, "Histórico encontrado", resultado)


@agendamento_bp.route("/relatorio-semanal", methods=["GET"])
def relatorio_semanal():
    ano = request.args.get("ano", type=int)
    semana = request.args.get("semana", type=int)

    if not ano or not semana:
        return api_response(400, "Ano e Semana são obrigatórios")

    dados = desempenho_semanal(ano, semana)

    return api_response(200, "Relatório semanal", dados)
