from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from entidades.compra import Compra

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    compras: Mapped[List["Compra"]] = relationship(back_populates="usuario") 

# # Clase antigua sin Base (comentada porque se usa el modelo SQLAlchemy arriba)
# class Usuario:
#     def __init__(self, nombre: str, apellido: str, email: str, password: str):
#         self.nombre = nombre
#         self.apellido = apellido
#         self.email = email
#         self.password = password


    def validar_Atributos(self) -> None:
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

        # apellido: obligatorio, str no vacío
        if not hasattr(self, "apellido"):
            errores.append("falta el atributo 'apellido'")
        else:
            apellido = getattr(self, "apellido")
            if not isinstance(apellido, str):
                errores.append("'apellido' debe ser str")
            elif not apellido.strip():
                errores.append("'apellido' no puede estar vacío")

        # email: obligatorio, str no vacío
        if not hasattr(self, "email"):
            errores.append("falta el atributo 'email'")
        else:
            email = getattr(self, "email")
            if not isinstance(email, str):
                errores.append("'email' debe ser str")
            elif not email.strip():
                errores.append("'email' no puede estar vacío")
            elif "@" not in email:
                errores.append("'email' debe contener '@' válido")

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