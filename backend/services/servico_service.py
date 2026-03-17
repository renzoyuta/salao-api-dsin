from database.connection import db
from models.servico import Servico


def listar_servicos():
    servicos = Servico.query.all()

    return [s.to_dict() for s in servicos]


def criar_servico(dados):
    nome = dados.get("nome")
    preco = dados.get("preco")

    if not nome or nome.strip() == "":
        raise ValueError("Nome do serviço é obrigatório")

    if not preco or preco <= 0:
        raise ValueError("Preço deve ser maior que zero")

    servico_existente = Servico.query.filter_by(nome=nome).first()
    if servico_existente:
        raise ValueError("Serviço já cadastrado")

    servico = Servico(nome=nome.strip(), preco=preco)
    db.session.add(servico)
    db.session.commit()

    return servico.to_dict()


def atualizar_servico(servico_id, dados):
    servico = Servico.query.get(servico_id)

    if not servico:
        raise ValueError("Serviço não encontrado")

    if "nome" in dados:
        nome = dados.get("nome").strip()
        if not nome:
            raise ValueError("Nome não pode ser vazio")

        nome_existente = Servico.query.filter(Servico.nome == nome).first()
        if nome_existente:
            raise ValueError("Já existe um serviço com esse nome")
        servico.nome = nome

    if "preco" in dados:
        preco = dados.get("preco")
        if preco <= 0:
            raise ValueError("Preço deve ser maior que zero")
        servico.preco = preco

    db.session.commit()
    return servico.to_dict()


def deletar_servico(servico_id):
    servico = Servico.query.get(servico_id)
    if not servico:
        raise ValueError("Serviço não encontrado")

    db.session.delete(servico)
    db.session.commit()

    return
