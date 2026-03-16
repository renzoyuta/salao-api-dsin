from datetime import datetime, timedelta

from database.connection import db
from models.agendamento import Agendamento
from models.servico import Servico
from sqlalchemy.orm import joinedload


def pode_alterar_data(data_agendamento: str):
    hoje = datetime.now().date()

    limite = data_agendamento - timedelta(days=2)

    return hoje <= limite


def verificar_agendamento_semana(cliente_id: int, data: datetime.date, ignorar_id=None):
    data_inicio = data - timedelta(days=data.weekday())
    data_fim = data_inicio + timedelta(days=6)

    agendamento_existente = Agendamento.query.filter_by(cliente_id=cliente_id).filter(
        Agendamento.data.between(data_inicio, data_fim)
    )

    if ignorar_id:
        agendamento_existente = agendamento_existente.filter(
            Agendamento.id != ignorar_id
        )

    return agendamento_existente.first()


def listar_agendamento():
    agendamentos = Agendamento.query.options(
        joinedload(Agendamento.cliente), joinedload(Agendamento.servicos)
    ).all()

    return [a.to_dict() for a in agendamentos]


def criar_agendamento(dados):
    cliente_id = dados.get("cliente_id")
    data_agendamento = dados.get("data")
    servicos_ids = dados.get("servicos", [])

    if not cliente_id:
        raise ValueError("Informe o id do cliente")

    if not data_agendamento:
        raise ValueError("Informe a data do agendamento")

    if not servicos_ids:
        raise ValueError("Informe ao menos um serviço")

    data_agendamento_formatado = datetime.strptime(data_agendamento, "%Y-%m-%d").date()

    if data_agendamento_formatado < datetime.now().date():
        raise ValueError("A data do agendamento não pode ser no passado")

    agendamento_existente = verificar_agendamento_semana(
        cliente_id, data_agendamento_formatado
    )

    if agendamento_existente:
        raise ValueError(
            f"Cliente já possui agendamento nessa semana. Data Sugerida: {agendamento_existente.data}"
        )

    servicos = Servico.query.filter(Servico.id.in_(servicos_ids)).all()

    valor_total = sum(s.preco for s in servicos)

    agendamento = Agendamento(
        cliente_id=cliente_id,
        data=data_agendamento_formatado,
        servicos=servicos,
        valor=valor_total,
    )

    db.session.add(agendamento)
    db.session.commit()

    return {
        "id": agendamento.id,
        "cliente_id": cliente_id,
        "data": data_agendamento,
        "valor": valor_total,
    }


def atualizar_agendamento(agendamento_id: int, dados, admin=False):
    agendamento = Agendamento.query.get(agendamento_id)

    if not agendamento:
        raise ValueError("Agendamento não encontrado")

    if "data" in dados:
        nova_data = datetime.strptime(dados.get("data"), "%Y-%m-%d").date()

        if nova_data < datetime.now().date():
            raise ValueError("A data do agendamento não pode ser no passado")

        if not admin:
            pode_alterar = pode_alterar_data(nova_data)

            if not pode_alterar:
                raise ValueError("Alteração permitida até 2 dias antes do agendamento")

            agendamento_existente = verificar_agendamento_semana(
                agendamento.cliente_id, nova_data, agendamento_id
            )

            if agendamento_existente:
                raise ValueError(
                    f"Cliente já possui agendamento nessa semana. Data Sugerida: {agendamento_existente.data}"
                )

        agendamento.data = nova_data

    if "servicos" in dados:
        servicos_ids = dados.get("servicos", [])

        if not servicos_ids:
            raise ValueError("Informe ao menos um serviço")

        servicos = Servico.query.filter(Servico.id.in_(servicos_ids)).all()

        agendamento.servicos = servicos

        valor_total = sum(s.preco for s in servicos)

        agendamento.valor = valor_total

    db.session.commit()

    return


def atualizar_status(cliente_id: int, dados):
    agendamento = Agendamento.query.get(cliente_id)

    if not agendamento:
        raise ValueError("Agendamento não encontrado")

    agendamento.status = dados.get("status")

    db.session.commit()

    return
