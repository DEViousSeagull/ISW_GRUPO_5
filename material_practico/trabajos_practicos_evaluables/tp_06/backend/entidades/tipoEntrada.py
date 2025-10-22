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

        if errores:
            raise ValueError("; ".join(errores))

