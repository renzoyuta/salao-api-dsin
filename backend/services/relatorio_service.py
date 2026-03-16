from datetime import datetime, timedelta

from sqlalchemy import func

from database.connection import db
from models.agendamento import Agendamento, agendamento_servicos
from models.servico import Servico


def desempenho_semanal(ano: int, semana: int):
    inicio_semana = datetime.fromisocalendar(ano, semana, 1)
    fim_semana = inicio_semana + timedelta(days=6)

    resultado = (
        db.session.query(
            func.count(Agendamento.id).label("agendamento_total"),
            func.sum(Agendamento.valor).label("faturamento_total"),
        )
        .filter(Agendamento.data.between(inicio_semana, fim_semana))
        .first()
    )

    servicos_semana = (
        db.session.query(Servico.nome, func.count(Servico.id).label("quantidade"))
        .join(agendamento_servicos)
        .join(Agendamento)
        .filter(Agendamento.data.between(inicio_semana, fim_semana))
        .group_by(Servico.nome)
        .order_by(func.count(Servico.id).desc())
    ).all()

    servicos_formatados = [
        {"servico": s.nome, "quantidade": s.quantidade} for s in servicos_semana
    ]

    faturamento_total = resultado.faturamento_total or 0
    agendamento_total = resultado.agendamento_total or 0

    ticket_medio = round(
        faturamento_total / agendamento_total if agendamento_total > 0 else 0, 2
    )

    return {
        "semana": semana,
        "ano": ano,
        "periodo": {
            "inicio": inicio_semana.date().isoformat(),
            "fim": fim_semana.date().isoformat(),
        },
        "agendamentos_total": agendamento_total,
        "faturamento_total": faturamento_total,
        "ticket_medio": ticket_medio,
        "servicos_realizados": servicos_formatados,
    }
