from datetime import date, timedelta

from models.agendamento import Agendamento
from models.cliente import Cliente
from models.servico import Servico

from database.connection import db


def seed_clientes():
    if Cliente.query.count() > 0:
        return

    clientes = [
        Cliente(nome="Ana", telefone="11999999901"),
        Cliente(nome="Bruna", telefone="11999999902"),
        Cliente(nome="Carla", telefone="11999999903"),
        Cliente(nome="Daniela", telefone="11999999904"),
        Cliente(nome="Elisa", telefone="11999999905"),
    ]

    db.session.add_all(clientes)
    db.session.commit()


def seed_servicos():
    if Servico.query.count() > 0:
        return

    servicos = [
        Servico(nome="Cabelo", preco=100),
        Servico(nome="Unha", preco=40),
        Servico(nome="Depilação", preco=60),
        Servico(nome="Maquiagem", preco=150),
        Servico(nome="Sobrancelha", preco=35),
    ]

    db.session.add_all(servicos)
    db.session.commit()


def seed_agendamentos():

    if Agendamento.query.count() > 0:
        return

    clientes = Cliente.query.all()
    servicos = Servico.query.all()

    hoje = date.today()

    agendamentos = [
        Agendamento(
            cliente_id=clientes[0].id,
            data=hoje,
            servicos=[servicos[0], servicos[1]],
            valor=servicos[0].preco + servicos[1].preco,
        ),
        Agendamento(
            cliente_id=clientes[1].id,
            data=hoje + timedelta(days=1),
            servicos=[servicos[2]],
            valor=servicos[2].preco,
        ),
        Agendamento(
            cliente_id=clientes[2].id,
            data=hoje + timedelta(days=2),
            servicos=[servicos[3], servicos[4]],
            valor=servicos[3].preco + servicos[4].preco,
        ),
    ]

    db.session.add_all(agendamentos)
    db.session.commit()
