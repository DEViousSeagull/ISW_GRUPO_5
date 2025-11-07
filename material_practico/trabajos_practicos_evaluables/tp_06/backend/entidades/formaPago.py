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
    

    def validar_atributos(self) -> None:
        errores = []

        # nombre: obligatorio, str no vacío
        if not hasattr(self, "nombre"):
            errores.append("falta el atributo 'nombre'")
        else:
            nombre = getattr(self, "nombre")
            if not isinstance(nombre, str):
                errores.append("'nombre' debe ser str")
            elif not nombre.strip():
                errores.append("'nombre' no puede estar vacío")

        # id: obligatorio, debe existir, no ser None y ser int
        if not hasattr(self, "id"):
            errores.append("falta el atributo 'id'")
        else:
            id_val = getattr(self, "id")
            if id_val is None:
                errores.append("'id' no puede ser None")
            elif not isinstance(id_val, int):
                errores.append("'id' debe ser int")
            elif id_val < 1:
                errores.append("'id' debe ser >= 1")

        if errores:
            raise ValueError("; ".join(errores))

class Tarjeta(FormaPago):
    def __init__(self, nombre: str, numero: str, vencimiento: str):
        super().__init__(nombre)
        self.numero = numero
        self.vencimiento = vencimiento

    def validate(self):
        super().validate()
        # validaciones de tarjeta...

