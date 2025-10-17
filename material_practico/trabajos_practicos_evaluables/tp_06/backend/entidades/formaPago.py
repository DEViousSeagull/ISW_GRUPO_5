# formaPago.py
class FormaPago:
    def __init__(self, nombre: str):
        self.nombre = nombre

    def validate(self):
        if self.nombre not in ("efectivo", "tarjeta"):
            raise ValueError("Forma de pago inválida")


class Tarjeta(FormaPago):
    def __init__(self, nombre: str, numero: str, vencimiento: str):
        super().__init__(nombre)
        self.numero = numero
        self.vencimiento = vencimiento

    def validate(self):
        super().validate()
        # validaciones de tarjeta...
