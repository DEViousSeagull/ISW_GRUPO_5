from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base

if TYPE_CHECKING:
    # Solo hints, sin ejecutar el import en runtime
    from entidades.compra import Compra
    from entidades.tipoEntrada import TipoEntrada

#class Entrada:
 #   def __init__(self,tipo_Entrada: TipoEntrada, id: int, edad: int, precio: float):
#        self.tipo_Entrada = tipo_Entrada
#        self.id = id
#        self.edad = edad
#        self.precio = precio

#        if not isinstance(self.edad, int) or self.edad < 0 or isinstance(self.edad, str):
#            raise ValueError("La edad es inválida; debe ser un entero")

class Entrada(Base):
    __tablename__ = "entradas"

    

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_entrada_id: Mapped[int] = mapped_column(
        ForeignKey("tipos_entrada.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    # FK a Compra (cada entrada pertenece a UNA compra)
    compra_id: Mapped[int] = mapped_column(
        ForeignKey("compras.id", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("edad >= 0", name="ck_entradas_edad_nonneg"),
        CheckConstraint("precio_unitario >= 0", name="ck_entradas_precio_nonneg"),
    )

    # Relaciones
    compra: Mapped["Compra"] = relationship(back_populates="entradas")
    tipo_entrada: Mapped["TipoEntrada"] = relationship(back_populates="entradas")

    def calcular_precio(self):
        if self.tipo_entrada.nombre == "VIP":
            self.precio_unitario = 10000
        if 3 < self.edad < 10 or self.edad > 60:
            self.precio_unitario = self.precio_unitario / 2
        elif self.edad < 3:
            self.precio_unitario = 0
        return self.precio_unitario
    

    def validar_Atributos(self) -> None:
        errores = []

        # edad
        if getattr(self, "edad", None) is None:
            errores.append("edad ausente")
        else:
            if not isinstance(self.edad, int):
                errores.append("edad debe ser un entero")
            elif self.edad < 0:
                errores.append("edad debe ser >= 0")

        # tipo de entrada (puede estar por relación o por id)
        if getattr(self, "tipo_entrada", None) is None and getattr(self, "tipo_entrada_id", None) is None:
            errores.append("tipo_entrada/tipo_entrada_id ausente")

        # precio_unitario
        if getattr(self, "precio_unitario", None) is None:
            errores.append("precio_unitario ausente")
        else:
            try:
                val = float(self.precio_unitario)
                if val < 0:
                    errores.append("precio_unitario debe ser >= 0")
            except (TypeError, ValueError):
                errores.append("precio_unitario debe ser numérico")

        if errores:
            raise ValueError("Entrada inválida: " + "; ".join(errores))

    # Adjuntar el método a la clase Entrada (se puede llamar como instancia.validar())