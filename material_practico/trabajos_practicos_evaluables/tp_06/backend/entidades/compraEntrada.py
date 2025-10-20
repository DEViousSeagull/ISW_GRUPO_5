from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base
from typing import List
from entidades.compra import Compra


class CompraEntrada(Base):
    """
    Asociación Compra <-> Entrada con columna adicional precio_aplicado (snapshot).
    PK compuesta (compra_id, entrada_id).
    """
    tablename = "compra_entradas"

    compra_id: Mapped[int] = mapped_column(ForeignKey("compras.id", ondelete="CASCADE"), primary_key=True)
    entrada_id: Mapped[int] = mapped_column(ForeignKey("entradas.id", ondelete="RESTRICT"), primary_key=True)
    precio_aplicado: Mapped[float] = mapped_column(Float, nullable=False)

    table_args = (
        CheckConstraint("precio_aplicado >= 0", name="ck_compra_entradas_precio_nonneg"),
    )

    compra: Mapped["Compra"] = relationship(back_populates="items")
    entrada: Mapped["Entrada"] = relationship(back_populates="compra_items")