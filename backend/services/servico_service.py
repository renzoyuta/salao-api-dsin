from models.servico import Servico


def listar_servicos():
    servicos = Servico.query.all()

    return [
        {
            "id": s.id,
            "nome": s.nome,
            "preco": s.preco,
        }
        for s in servicos
    ]
