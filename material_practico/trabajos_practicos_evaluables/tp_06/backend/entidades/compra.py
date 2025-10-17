from dataclasses import dataclass
from typing import List
from datetime import date
from entidades.entrada import Entrada


class Compra:
    def __init__(self, fecha: date, cantidad_entradas: int, entradas: List[Entrada], monto_total: float = 0):
        self.fecha = fecha
        self.cantidad_entradas = cantidad_entradas
        self.entradas = entradas or []
        self.monto_total = monto_total

    def cantidad_entradas_validas(self):
        if self.cantidad_entradas > 10:
            raise ValueError("Cantidad inválida; máximo 10")
       

    