from sqlalchemy import Column, Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import db
from models.cliente import Cliente
from models.servico import Servico

agendamento_servicos = db.Table(
    "agendamento_servicos",
    db.metadata,
    Column("agendamento_id", ForeignKey("agendamentos.id")),
    Column("servico_id", ForeignKey("servicos.id")),
)


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(primary_key=True)

    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))

    data: Mapped[Date] = mapped_column(Date)

    status: Mapped[str] = mapped_column(String, default="Agendado")

    valor: Mapped[float] = mapped_column(Float)

    cliente: Mapped["Cliente"] = relationship("Cliente")

    servicos: Mapped[list["Servico"]] = relationship(secondary="agendamento_servicos")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente.id,
            "cliente": self.cliente.nome,
            "data": str(self.data),
            "status": self.status,
            "valor": self.valor,
            "servicos": [s.nome for s in self.servicos],
        }
