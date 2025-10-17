from dataclasses import dataclass
from typing import List
from datetime import date
from entidades.entrada import Entrada
from entidades.formaPago import FormaPago


class Compra:
    def __init__(self, fecha: date, cantidad_entradas: int, entradas: List[Entrada], formaPago: FormaPago, monto_total: float = 0):
        self.fecha = fecha
        self.cantidad_entradas = cantidad_entradas
        self.entradas = entradas or []
        self.monto_total = monto_total
        self.formaPago = formaPago


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
    
    
    
