from dataclasses import dataclass
from typing import List
from datetime import date
from entidades.entrada import Entrada
from entidades.formaPago import FormaPago
from entidades.usuario import Usuario   


class Compra:
    def __init__(self, fecha: date, cantidad_entradas: int, entradas: List[Entrada], formaPago: FormaPago, usuario: Usuario, monto_total: float = 0):
        self.fecha = fecha
        self.cantidad_entradas = cantidad_entradas
        self.entradas = entradas or []
        self.monto_total = monto_total
        self.formaPago = formaPago
        self.usuario = usuario
        self.mercado_pago_redirect_url = None  # URL de redirección a Mercado Pago (si aplica)


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
        }
        # Aquí se enviaría la confirmación, por ejemplo, a un servicio de mensajería
        return True

