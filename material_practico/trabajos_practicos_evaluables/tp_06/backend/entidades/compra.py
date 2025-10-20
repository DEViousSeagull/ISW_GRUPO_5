from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING
from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.base import Base

if TYPE_CHECKING:
    # Solo para hints; NO se ejecuta en runtime, evita ciclo
    from entidades.entrada import Entrada
    from entidades.formaPago import FormaPago
    from entidades.usuario import Usuario

#class Compra:
#    def __init__(self, fecha: date, cantidad_entradas: int, entradas: List[Entrada], formaPago: FormaPago, usuario: Usuario, monto_total: float = 0):
#        self.fecha = fecha
#        self.cantidad_entradas = cantidad_entradas
#        self.entradas = entradas or []
#        self.monto_total = monto_total
#        self.formaPago = formaPago
#        self.usuario = usuario
#        self.mercado_pago_redirect_url = None  # URL de redirección a Mercado Pago (si aplica)

class Compra(Base):
    __tablename__ = "compras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    cantidad_entradas: Mapped[int] = mapped_column(Integer, nullable=False)
    monto_total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    forma_pago_id: Mapped[int] = mapped_column(ForeignKey("formas_pago.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    mercado_pago_redirect_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("cantidad_entradas BETWEEN 1 AND 10", name="ck_compras_cantidad_1_10"),
    )

    # Relación 1─* con Entrada
    entradas: Mapped[list["Entrada"]] = relationship(
        back_populates="compra",
        cascade="all, delete-orphan"
    )
    usuario: Mapped["Usuario"] = relationship(back_populates="compras")
    forma_pago: Mapped["FormaPago"] = relationship(back_populates="compras")

    def cantidad_entradas_validas(self):
        if self.cantidad_entradas > 10:
            raise ValueError("Cantidad inválida; máximo 10")

    def validar_cantidad_entradas_coincide(self):
        """Valida que self.cantidad_entradas coincida con len(self.entradas)."""
        if self.cantidad_entradas != len(self.entradas):
            raise ValueError(
                f"Cantidad inválida: el atributo cantidad_entradas={self.cantidad_entradas} no coincide con la cantidad de entradas asignadas a la compra ({len(self.entradas)})"
            )
        return True

    def validar_fecha(self):
        """Valida que la fecha de la compra no sea menor a la fecha actual, que no coincida con un día festivo (mes/día) y que no sea lunes."""
        dias_festivos_md = {(1, 1), (12, 25)}  # (mes, día): Año Nuevo, Navidad (cualquier año)
        if self.fecha < date.today():
            raise ValueError("La fecha de la compra no puede ser menor a la fecha actual.")
        if (self.fecha.month, self.fecha.day) in dias_festivos_md:
            raise ValueError("La fecha de la compra no puede coincidir con un día festivo.")
        if self.fecha.weekday() == 0:  # 0 = lunes
            raise ValueError("La fecha de la compra no puede caer en lunes.")
        return True
    
    def validar_formaPago(self):
        self.formaPago.validate()
        return self.formaPago.nombre

    def obtener_redirect_pago(self, gateway):
        # solo se usa si la forma necesita redirección (tarjeta)
        if self.formaPago.nombre != "tarjeta":
            return None
        if gateway is None:
            raise TypeError("Gateway no proporcionado para forma de pago con redirección")
        self.mercado_pago_redirect_url = gateway.generate_redirect(self)
        return self.mercado_pago_redirect_url

    def validar_cantidad_entradas(self):
        """Valida que cantidad_entradas sea un entero (no float, Decimal ni bool)."""
        if not isinstance(self.cantidad_entradas, int) or self.cantidad_entradas < 0:
            raise ValueError("La cantidad de entradas debe ser un número entero sin decimales y mayor o igual a 0.")
        return True

    def enviar_confirmacion_email(self):
        datos = {
            "fecha": self.fecha,
            "cantidad_entradas": self.cantidad_entradas,
            "monto_total": self.monto_total,
            "formaPago": self.formaPago.nombre,
            "Destinatario": {
                "nombre": self.usuario.nombre,
                "apellido": self.usuario.apellido,
                "email": self.usuario.email
            }
        }
        # Aquí se enviaría la confirmación, por ejemplo, a un servicio de mensajería
        return True


    def calcular_monto_total(self):
        total = 0.0
        for entrada in self.entradas or []:
            precio = entrada.calcular_precio()
            total += float(precio)
        self.monto_total = total
        return self.monto_total

