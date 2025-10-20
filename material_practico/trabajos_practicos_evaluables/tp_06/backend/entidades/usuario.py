from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base
from typing import List
from entidades.compra import Compra 

class Usuario(Base):
    tablename = "usuarios"

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
