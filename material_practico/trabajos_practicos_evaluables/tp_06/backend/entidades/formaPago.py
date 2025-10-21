# formaPago.py
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from entidades.compra import Compra

class FormaPago(Base):
    __tablename__ = "formas_pago"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    compras: Mapped[List["Compra"]] = relationship(back_populates="forma_pago")
    
#class FormaPago:
#    def __init__(self, nombre: str):
#        self.nombre = nombre

#    def validate(self):
#        if self.nombre not in ("efectivo", "tarjeta"):
#            raise ValueError("Forma de pago inválida")


class Tarjeta(FormaPago):
    def __init__(self, nombre: str, numero: str, vencimiento: str):
        super().__init__(nombre)
        self.numero = numero
        self.vencimiento = vencimiento

    def validate(self):
        super().validate()
        # validaciones de tarjeta...
