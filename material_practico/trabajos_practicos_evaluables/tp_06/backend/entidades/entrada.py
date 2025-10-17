from entidades.tipoEntrada import TipoEntrada
class Entrada:
    def __init__(self,tipo_Entrada: TipoEntrada, id: int, edad: int, precio: float):
        self.tipo_Entrada = tipo_Entrada
        self.id = id
        self.edad = edad
        self.precio = precio

        if not isinstance(self.edad, int) or self.edad < 0:
            raise ValueError("La edad es inválida; debe ser un entero")

    def calcular_precio(self):
        if self.tipo_Entrada.nombre == "VIP":
            self.precio = 10000
        if 3 < self.edad < 10 or self.edad > 60:
            self.precio = self.precio / 2
        elif self.edad < 3:
            self.precio = 0
    

        