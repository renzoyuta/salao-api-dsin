from database.connection import db
from models.cliente import Cliente


def listar_cliente():
    clientes = Cliente.query.all()

    return [c.to_dict() for c in clientes]


def criar_cliente(dados):
    nome = dados.get("nome")
    telefone = dados.get("telefone")

    nome_existente = Cliente.query.filter_by(nome=nome).first()

    if nome_existente:
        raise ValueError("Cliente já cadastrado")

    if not nome or nome.strip() == "":
        raise ValueError("Nome do cliente é obrigatório")

    if not telefone:
        raise ValueError("Telefone do cliente é obrigatório")

    cliente = Cliente(nome=nome.strip(), telefone=dados.get("telefone"))

    db.session.add(cliente)
    db.session.commit()

    return {"id": cliente.id, "nome": cliente.nome}
