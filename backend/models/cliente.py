from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import db


class Cliente(db.Model):
    __tablename__ = "clientes"
    id: Mapped[int] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(unique=True)

    telefone: Mapped[str] = mapped_column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
        }
