from dataclasses import dataclass
from typing import List
from datetime import date
from entidades.entrada import Entrada


class Compra:
    def __init__(self, fecha: date,  entradas: List[Entrada], monto_total: float = 0):
        self.fecha = fecha
        self._entradas = list(entradas or [])
        self.monto_total = monto_total


    @property
    def cantidad_entradas(self) -> int:
        n = len(self._entradas)
        if  n > 10:
            # Mensaje esperado por el test adjunto
            raise ValueError("Cantidad inválida; máximo 10")
        return n


    