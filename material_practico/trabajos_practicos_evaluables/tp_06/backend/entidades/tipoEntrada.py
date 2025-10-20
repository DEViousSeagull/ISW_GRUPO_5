from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from entidades.entrada import Entrada

class TipoEntrada(Base):
    __tablename__ = "tipos_entrada"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    entradas: Mapped[List["Entrada"]] = relationship(back_populates="tipo_entrada")


#class TipoEntrada:
#    def __init__(self, nombre: str):
#        self.nombre = nombre