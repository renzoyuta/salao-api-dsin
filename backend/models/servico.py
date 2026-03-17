from database.connection import db
from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column


class Servico(db.Model):
    __tablename__ = "servicos"
    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(unique=True)

    preco: Mapped[float] = mapped_column(Float)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "preco": self.preco}
