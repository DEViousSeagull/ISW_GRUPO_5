from entidades.tipoEntrada import TipoEntrada
class Entrada:
    def __init__(self,tipo_Entrada: TipoEntrada, id: int, edad: int, precio: float):
        self.tipo_Entrada = tipo_Entrada
        self.id = id
        self.edad = edad
        self.precio = precio