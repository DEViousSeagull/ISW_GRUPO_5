from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base
from entidades.tipoEntrada import TipoEntrada
from entidades.compra import Compra

if TYPE_CHECKING:
   
    from entidades.compra import Compra
    from entidades.tipoEntrada import TipoEntrada



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
        if self.tipo_entrada_id == 1:
            self.precio_unitario = 10000
        else:
            self.precio_unitario = 5000

        if 3 <= self.edad < 10 or self.edad > 60:
            self.precio_unitario = self.precio_unitario / 2
        elif self.edad < 3:
            self.precio_unitario = 0
        return self.precio_unitario
    

    def validar_atributos(self) -> None:
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
        if getattr(self, "tipo_entrada", None) is None :
            errores.append("tipo_entrada/tipo_entrada_id ausente")
        else:
            if not isinstance(self.tipo_entrada, TipoEntrada):
                errores.append("tipo_entrada debe ser TipoEntrada")
        if getattr(self, "tipo_entrada_id", None) is None:
            errores.append("tipo_entrada/tipo_entrada_id ausente")
        else:
            if not isinstance(self.tipo_entrada_id, int):
                errores.append("tipo_entrada_id debe ser int")
            elif self.tipo_entrada_id < 1:
                errores.append("tipo_entrada_id debe ser >= 1")

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
        if getattr(self, "id", None) is None:
            errores.append("id ausente")
        else:
            if not isinstance(self.id, int):
                errores.append("id debe ser int")
            elif self.id < 0:
                errores.append("id debe ser >= 0")
        if getattr(self, "compra_id", None) is None:
            errores.append("compra_id ausente") 
        else:
            if not isinstance(self.compra_id, int):
                errores.append("compra_id debe ser int")
            elif self.compra_id < 0:
                errores.append("compra_id debe ser >= 0")
        if getattr(self, "compra", None) is None:
            errores.append("compra ausente")
        else:
            if not isinstance(self.compra, Compra):
                errores.append("compra debe ser Compra")

        if errores:
            raise ValueError("Entrada inválida: " + "; ".join(errores))

   