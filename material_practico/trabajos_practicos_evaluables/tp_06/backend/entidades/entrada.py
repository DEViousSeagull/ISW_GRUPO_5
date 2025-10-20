from entidades.tipoEntrada import TipoEntrada
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base
from typing import List
from entidades.compraEntrada import CompraEntrada
#class Entrada:
 #   def __init__(self,tipo_Entrada: TipoEntrada, id: int, edad: int, precio: float):
#        self.tipo_Entrada = tipo_Entrada
#        self.id = id
#        self.edad = edad
#        self.precio = precio

#        if not isinstance(self.edad, int) or self.edad < 0 or isinstance(self.edad, str):
#            raise ValueError("La edad es inválida; debe ser un entero")

class Entrada(Base):
    tablename = "entradas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_pase_id: Mapped[int] = mapped_column(ForeignKey("tipos_pase.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    table_args = (
        CheckConstraint("edad >= 0", name="ck_entradas_edad_nonneg"),
        CheckConstraint("precio_unitario >= 0", name="ck_entradas_precio_nonneg"),
    )

    tipo_pase: Mapped["TipoEntrada"] = relationship(back_populates="entradas")
    compra_items: Mapped[List["CompraEntrada"]] = relationship(back_populates="entrada")
    
    def calcular_precio(self):
        if self.tipo_pase.nombre == "VIP":
            self.precio_unitario = 10000
        if 3 < self.edad < 10 or self.edad > 60:
            self.precio_unitario = self.precio_unitario / 2
        elif self.edad < 3:
            self.precio_unitario = 0
        return self.precio_unitario
    

        